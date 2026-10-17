"""Spike: read a bill image with OCI Generative AI (Cohere Command A Vision) and print strict JSON.

Run on a machine with the OCI Python SDK and an API-key config (~/.oci/config),
e.g. the starter-kit VM:

    python3 extract_bill.py ../synthetic-bill/bill-01.png \
        --compartment <compartment OCID> --model <model id from the console>

Class names verified against oracle/oci-python-sdk source on 2026-10-17
(CohereChatRequestV2, CohereUserMessageV2, CohereTextContentV2,
CohereImageContentV2, CohereImageUrlV2, CohereResponseJsonFormat).
"""
import argparse
import base64
import json
import mimetypes
import sys
import time

import oci
from oci.generative_ai_inference import GenerativeAiInferenceClient
from oci.generative_ai_inference import models as m

ENDPOINT = "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com"
PROMPT = (
    "Read this hospital bill. Return only JSON with keys hospital_name, statement_date, "
    "account_number, amount_due, date_of_service, insurance_status. Use null for anything "
    "you cannot read clearly. Do not guess."
)


def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode("ascii"))


def extract(client, compartment, model, image_path):
    request = m.CohereChatRequestV2(
        messages=[m.CohereUserMessageV2(content=[
            m.CohereTextContentV2(text=PROMPT),
            m.CohereImageContentV2(image_url=m.CohereImageUrlV2(url=data_uri(image_path))),
        ])],
        max_tokens=600,
        temperature=0,
        response_format=m.CohereResponseJsonFormat(),
    )
    detail = m.ChatDetails(
        compartment_id=compartment,
        serving_mode=m.OnDemandServingMode(model_id=model),
        chat_request=request,
    )
    response = client.chat(detail)
    parts = response.data.chat_response.message.content or []
    return "".join(getattr(p, "text", "") or "" for p in parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--compartment", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--profile", default="DEFAULT")
    args = ap.parse_args()

    config = oci.config.from_file("~/.oci/config", args.profile)
    client = GenerativeAiInferenceClient(config=config, service_endpoint=ENDPOINT,
                                         retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10, 120))
    t0 = time.time()
    text = extract(client, args.compartment, args.model, args.image)
    elapsed = time.time() - t0
    print(text)
    try:
        json.loads(text)
        print("valid JSON; %.1f s" % elapsed, file=sys.stderr)
    except ValueError:
        print("NOT valid JSON; %.1f s" % elapsed, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
