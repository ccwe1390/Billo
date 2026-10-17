"""All OCI calls live here. FAKE_OCI=1 returns fixed data with no network or credentials.

Config (env): OCI_COMPARTMENT_ID, OCI_VISION_MODEL_ID, OCI_TEXT_MODEL_ID,
OCI_PROFILE (default DEFAULT), OCI_LANGUAGE_ENDPOINT (optional override).
Nothing here writes to disk or logs request/response bodies.
"""
import base64
import json
import os

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


def _config():
    import oci
    return oci.config.from_file("~/.oci/config", os.environ.get("OCI_PROFILE", "DEFAULT"))


def _genai_client():
    import oci
    from oci.generative_ai_inference import GenerativeAiInferenceClient
    return GenerativeAiInferenceClient(
        config=_config(), service_endpoint=GENAI_ENDPOINT,
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


def translate_many(texts, target_lang):
    """Translate English texts with OCI Language. Returns a list in the same order.

    UNTESTED against the live service (SDK shapes read from the installed oci
    2.188.0 package: AIServiceLanguageClient.batch_language_translation).
    """
    if is_fake():
        return ["[%s draft] %s" % (target_lang.upper(), t) for t in texts]
    from oci.ai_language import AIServiceLanguageClient
    from oci.ai_language import models as m
    import oci
    kwargs = {}
    if os.environ.get("OCI_LANGUAGE_ENDPOINT"):
        kwargs["service_endpoint"] = os.environ["OCI_LANGUAGE_ENDPOINT"]
    client = AIServiceLanguageClient(config=_config(), retry_strategy=oci.retry.NoneRetryStrategy(), **kwargs)
    details = m.BatchLanguageTranslationDetails(
        compartment_id=_env("OCI_COMPARTMENT_ID"),
        target_language_code=target_lang,
        documents=[m.TextDocument(key=str(i), text=t, language_code="en") for i, t in enumerate(texts)])
    result = client.batch_language_translation(details).data
    if result.errors:
        raise RuntimeError("translation returned %d document error(s)" % len(result.errors))
    by_key = {d.key: d.translated_text for d in result.documents}
    return [by_key[str(i)] for i in range(len(texts))]


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
