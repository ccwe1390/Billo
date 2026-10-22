"""Plain-assert tests for the Claude provider (app/claude_backend.py via app/ai_client.py).
Run from repo root: py tests/test_claude_backend.py   (the Anthropic client is replaced; no network or key)"""
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.pop("FAKE_AI", None)
os.environ.pop("FAKE_OCI", None)
os.environ.pop("AI_PROVIDER", None)  # default provider is claude
os.environ.pop("BILLO_CLAUDE_MODEL", None)
os.environ.pop("BILLO_CLAUDE_EFFORT", None)

from app import ai_client, claude_backend  # noqa: E402

calls = []
reply = {"text": "", "stop": "end_turn"}


def fake_create(**kwargs):
    calls.append(kwargs)
    return SimpleNamespace(stop_reason=reply["stop"],
                           content=[SimpleNamespace(type="thinking", thinking=""),
                                    SimpleNamespace(type="text", text=reply["text"])])


claude_backend._client = lambda: SimpleNamespace(beta=SimpleNamespace(messages=SimpleNamespace(create=fake_create)))

assert ai_client.provider() == "claude"
assert ai_client.translator_name("hi") == "claude" and ai_client.translator_name("es") == "claude"

# bill photo: image block first, then the prompt; default model with the refusal fallback
reply["text"] = '```json\n{"hospital_name": "Vanderbilt University Medical Center", "amount_due": 4812.40}\n```'
out = ai_client.extract_bill(b"\x89PNG\r\n\x1a\nxx", "image/png")
assert out == {"hospital_name": "Vanderbilt University Medical Center", "amount_due": 4812.40}
c = calls[-1]
assert c["model"] == "claude-opus-5-5" and c["fallbacks"] == "default"
assert c["betas"] == ["server-side-fallback-2026-07-01"]
assert c["output_config"] == {"effort": "low"} and "temperature" not in c and "thinking" not in c
blocks = c["messages"][0]["content"]
assert blocks[0]["type"] == "image" and blocks[0]["source"]["media_type"] == "image/png"
assert blocks[1] == {"type": "text", "text": ai_client.EXTRACT_PROMPT}

# EOB prompt carries the visit date
reply["text"] = '{"not_eob": true}'
assert ai_client.extract_eob(b"\xff\xd8\xffxx", "image/jpeg", "2026-09-12") == {"not_eob": True}
assert "a visit on 2026-09-12." in calls[-1]["messages"][0]["content"][1]["text"]

# a model without the server-side fallback gets no fallbacks parameter
os.environ["BILLO_CLAUDE_MODEL"] = "claude-haiku-5-5"
reply["text"] = "Hola"
assert ai_client.phrase("Hello", "es") == "Hola"
assert calls[-1]["model"] == "claude-haiku-5-5" and "fallbacks" not in calls[-1] and "betas" not in calls[-1]
assert len(calls[-1]["messages"][0]["content"]) == 1  # text only
os.environ.pop("BILLO_CLAUDE_MODEL")

# translate_many goes to Claude with numbers and the hospital name masked, then restored
reply["text"] = "Monto para {0}: ${1}"
hosp = "Vanderbilt University Medical Center"
assert ai_client.translate_many(["Amount for %s: $4,812.40" % hosp], "es", keep=[hosp]) == \
    ["Monto para %s: $4,812.40" % hosp]
sent = calls[-1]["messages"][0]["content"][0]["text"]
assert "4,812.40" not in sent and hosp not in sent and "{0}" in sent and "Spanish" in sent

# refusal or a cut-off answer raises, so the app falls back to its English template
reply["stop"] = "refusal"
try:
    ai_client.phrase("Hello", "es")
    raise AssertionError("expected a failure")
except RuntimeError as e:
    assert "refusal" in str(e)
reply["stop"] = "end_turn"

# AI_PROVIDER=oci keeps the TNHacks26 labels
os.environ["AI_PROVIDER"] = "oci"
assert ai_client.translator_name("hi") == "command_a" and ai_client.translator_name("es") == "oci_language"
os.environ.pop("AI_PROVIDER")

# FAKE_AI and the older FAKE_OCI both skip the network
for flag in ("FAKE_AI", "FAKE_OCI"):
    os.environ[flag] = "1"
    n = len(calls)
    assert ai_client.translate_many(["Due $1.00"], "es") == ["[ES draft] Due $1.00"] and len(calls) == n
    os.environ.pop(flag)

print("ALL PASS")
