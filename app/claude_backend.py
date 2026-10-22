"""Claude (Anthropic API) calls for ai_client. Used when AI_PROVIDER is unset or "claude".

Config (env): ANTHROPIC_API_KEY, BILLO_CLAUDE_MODEL (default claude-opus-5-5),
BILLO_CLAUDE_EFFORT (default low: reading a bill and rewriting short facts need little reasoning).
Nothing here writes to disk or logs request/response bodies.
"""
import base64
import functools
import os

DEFAULT_MODEL = "claude-opus-5-5"
# Models that take the server-side refusal fallback ("default" routes by refusal category).
FALLBACK_MODELS = ("claude-fable-5-1", "claude-opus-5-5", "claude-opus-5", "claude-sonnet-5-5")


@functools.lru_cache(maxsize=1)
def _client():
    import anthropic
    # under the app's 45 s wait, so an abandoned call ends; no retries for the same reason
    return anthropic.Anthropic(timeout=40.0, max_retries=0)


def ask(prompt, image=None, max_tokens=1500):
    """One user turn -> the reply text. `image` is (bytes, mime) or None.

    `max_tokens` is the room the answer needs; thinking gets its own room on top.
    """
    content = []
    if image is not None:
        data, mime = image
        content.append({"type": "image", "source": {
            "type": "base64", "media_type": mime, "data": base64.standard_b64encode(data).decode("ascii")}})
    content.append({"type": "text", "text": prompt})
    model = os.environ.get("BILLO_CLAUDE_MODEL", DEFAULT_MODEL)
    kwargs = {}
    if model in FALLBACK_MODELS:
        kwargs = {"betas": ["server-side-fallback-2026-07-01"], "fallbacks": "default"}
    response = _client().beta.messages.create(
        model=model,
        max_tokens=max_tokens + 4000,
        output_config={"effort": os.environ.get("BILLO_CLAUDE_EFFORT", "low")},
        messages=[{"role": "user", "content": content}],
        **kwargs)
    if response.stop_reason != "end_turn":  # refusal or max_tokens: the caller falls back
        raise RuntimeError("model output incomplete: %s" % response.stop_reason)
    return "".join(b.text for b in response.content if b.type == "text")
