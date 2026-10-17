"""All OCI calls live here. FAKE_OCI=1 returns fixed data with no network or credentials.

Config (env): OCI_COMPARTMENT_ID, OCI_VISION_MODEL_ID, OCI_TEXT_MODEL_ID,
OCI_AUTH (instance_principal on the OCI VM; otherwise ~/.oci/config),
OCI_PROFILE (default DEFAULT), OCI_LANGUAGE_ENDPOINT (optional override).
Nothing here writes to disk or logs request/response bodies.
"""
import base64
import functools
import json
import os
import re

from app import numlock

GENAI_ENDPOINT = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"

EXTRACT_PROMPT = (
    "Read this hospital bill. Return only JSON with keys hospital_name, statement_date, "
    "account_number, amount_due, date_of_service, insurance_status. Use null for anything "
    "you cannot read clearly. Do not guess."
)

LANGUAGE_NAMES = {"en": "English", "es": "Spanish", "ar": "Arabic", "zh-CN": "Simplified Chinese",
                  "zh-TW": "Traditional Chinese", "vi": "Vietnamese", "fr": "French", "ko": "Korean",
                  "ru": "Russian", "de": "German", "hi": "Hindi"}


def is_fake():
    return os.environ.get("FAKE_OCI") == "1"


def _env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError("%s is not set" % name)
    return value


@functools.lru_cache(maxsize=1)
def _auth():
    """Client auth kwargs. OCI_AUTH=instance_principal: the VM authenticates as itself
    (dynamic group + policy), so no key is stored on the server. Otherwise the API key
    in ~/.oci/config (laptop). Cached: the signer refreshes its own token."""
    import oci
    if os.environ.get("OCI_AUTH") == "instance_principal":
        signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
        return {"config": {"region": signer.region}, "signer": signer}
    return {"config": oci.config.from_file("~/.oci/config", os.environ.get("OCI_PROFILE", "DEFAULT"))}


def _genai_client():
    import oci
    from oci.generative_ai_inference import GenerativeAiInferenceClient
    return GenerativeAiInferenceClient(
        service_endpoint=GENAI_ENDPOINT, **_auth(),
        retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10, 120))


def _chat(model_id, content_parts, json_mode):
    from oci.generative_ai_inference import models as m
    kwargs = {}
    if json_mode:
        kwargs["response_format"] = m.CohereResponseJsonFormat()
    request = m.CohereChatRequestV2(
        messages=[m.CohereUserMessageV2(content=content_parts)],
        max_tokens=600, temperature=0, **kwargs)
    detail = m.ChatDetails(
        compartment_id=_env("OCI_COMPARTMENT_ID"),
        serving_mode=m.OnDemandServingMode(model_id=model_id),
        chat_request=request)
    response = _genai_client().chat(detail)
    parts = response.data.chat_response.message.content or []
    return "".join(getattr(p, "text", "") or "" for p in parts)


def parse_json_object(text):
    """Model text -> JSON. Command A Vision wraps its JSON in a ```json fence even in
    JSON mode (seen live 2026-10-17), so fall back to the outermost {...}."""
    try:
        return json.loads(text)
    except ValueError:
        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end < start:
            raise
        return json.loads(text[start:end + 1])


def extract_bill(image_bytes, mime):
    """Bill image -> the model's raw JSON as a dict (keys per EXTRACT_PROMPT)."""
    if is_fake():
        # The fields printed on spikes/synthetic-bill/bill-01.
        return {
            "hospital_name": "Cumberland General Hospital (SYNTHETIC)",
            "statement_date": "10/01/2026",
            "account_number": "CGH-00482913",
            "amount_due": 4812.40,
            "date_of_service": "09/12/2026",
            "insurance_status": "None on file (self-pay)",
        }
    from oci.generative_ai_inference import models as m
    uri = "data:%s;base64,%s" % (mime, base64.b64encode(image_bytes).decode("ascii"))
    text = _chat(_env("OCI_VISION_MODEL_ID"), [
        m.CohereTextContentV2(text=EXTRACT_PROMPT),
        m.CohereImageContentV2(image_url=m.CohereImageUrlV2(url=uri)),
    ], json_mode=True)
    data = parse_json_object(text)
    if not isinstance(data, dict):
        raise ValueError("model did not return a JSON object")
    return data


def phrase(facts_en, language):
    """Rewrite the engine's English facts in `language` (Command A, text only).

    The caller number-checks the result and falls back to a template on mismatch.
    """
    if is_fake():
        return facts_en  # English text echoing the numbers
    from oci.generative_ai_inference import models as m
    prompt = (
        "Rewrite the facts below in %s, in simple everyday words, as the same number of lines. "
        "Write every date exactly in YYYY-MM-DD form. Copy every number, percent and dollar "
        "amount EXACTLY as given, using ASCII digits 0-9. Include no phone numbers or email "
        "addresses. Do not add, remove or change any fact. Do not add advice. "
        "Output only the rewritten lines.\n\nFacts:\n%s"
        % (LANGUAGE_NAMES[language], facts_en))
    return _chat(_env("OCI_TEXT_MODEL_ID"), [m.CohereTextContentV2(text=prompt)], json_mode=False).strip()


def protect_numbers(text, keep=()):
    """'Due: $4,812.40' -> ('Due: ${0}', ['4,812.40']). Same number pattern as numlock.

    `keep`: literal strings (e.g. the hospital name) that must not be translated; they
    are swapped for {i} first (longest first), the numbers take the following indices.
    """
    nums = []

    def take(match):
        nums.append(match.group(0))
        return "{%d}" % (len(nums) - 1)
    names = sorted({k for k in keep if k}, key=len, reverse=True)
    if names:
        text = re.sub("|".join(re.escape(k) for k in names), take, text)
        # numbers inside the new {i} placeholders are not numbers to protect
        text = "".join(part if re.fullmatch(r"\{\d+\}", part) else numlock._NUM.sub(take, part)
                       for part in re.split(r"(\{\d+\})", text))
        return text, nums
    return numlock._NUM.sub(take, text), nums


def restore_numbers(text, nums):
    for i, n in enumerate(nums):
        text = text.replace("{%d}" % i, n)
    return text


def translate_many(texts, target_lang, keep=()):
    """Translate English texts with OCI Language. Returns a list in the same order.

    Numbers are swapped for {0}, {1}... before translating and put back after:
    live on 2026-10-17 OCI Language turned "$4,812.40" into "$4.812,40" (es), and
    {n} placeholders survived es/fr/de/ru/ar/zh-CN/ko/vi. A lost placeholder stays
    lost, so the caller's number check rejects that text (fails closed). `keep` strings
    (names) get the same placeholders; the caller checks they survived.
    """
    if is_fake():
        return ["[%s draft] %s" % (target_lang.upper(), t) for t in texts]
    from oci.ai_language import AIServiceLanguageClient
    from oci.ai_language import models as m
    import oci
    protected = [protect_numbers(t, keep) for t in texts]
    kwargs = {}
    if os.environ.get("OCI_LANGUAGE_ENDPOINT"):
        kwargs["service_endpoint"] = os.environ["OCI_LANGUAGE_ENDPOINT"]
    client = AIServiceLanguageClient(**_auth(), retry_strategy=oci.retry.NoneRetryStrategy(), **kwargs)
    details = m.BatchLanguageTranslationDetails(
        compartment_id=_env("OCI_COMPARTMENT_ID"),
        target_language_code=target_lang,
        documents=[m.TextDocument(key=str(i), text=masked, language_code="en")
                   for i, (masked, _) in enumerate(protected)])
    result = client.batch_language_translation(details).data
    if result.errors:
        raise RuntimeError("translation returned %d document error(s)" % len(result.errors))
    by_key = {d.key: d.translated_text for d in result.documents}
    return [restore_numbers(by_key[str(i)], nums) for i, (_, nums) in enumerate(protected)]


def translate_genai_many(texts, target_lang):
    """Translate English texts with Command A only. Returns a list in the same order.

    Used where OCI Language has no support (Hindi). NOT back-checked.
    """
    if is_fake():
        return ["[%s draft] %s" % (target_lang.upper(), t) for t in texts]
    from oci.generative_ai_inference import models as m
    out = []
    for text in texts:
        prompt = (
            "Translate the text below into %s. Copy every number, date, account number and dollar "
            "amount EXACTLY, using ASCII digits 0-9. Keep the line breaks. Output only the translation."
            "\n\nText:\n%s" % (LANGUAGE_NAMES[target_lang], text))
        out.append(_chat(_env("OCI_TEXT_MODEL_ID"), [m.CohereTextContentV2(text=prompt)], json_mode=False).strip())
    return out


def translate(text, target_lang):
    return translate_many([text], target_lang)[0]
