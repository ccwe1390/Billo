"""Number lock: every number in generated text must match the engine's numbers.

Pure functions, no I/O. Arabic-Indic and Devanagari digits are normalized to
ASCII first, so an Arabic or Hindi translation that shows the same amounts passes.
"""
import re

# Arabic-Indic (U+0660-0669) and Eastern Arabic-Indic (U+06F0-06F9) digits,
# plus the Arabic thousands (U+066C) and decimal (U+066B) separators.
_TRANS = {}
for _i in range(10):
    _TRANS[0x0660 + _i] = str(_i)
    _TRANS[0x06F0 + _i] = str(_i)
    _TRANS[0x0966 + _i] = str(_i)  # Devanagari digits (Hindi)
_TRANS[0x066C] = ","
_TRANS[0x066B] = "."

# A number: digits, optionally joined by , . / - to more digits
# ("4,812.40", "2026-10-01", "10/01/2026"). A separator not followed by a
# digit (sentence-ending period) is not part of the number.
_NUM = re.compile(r"\d+(?:[,./-]\d+)*")


def normalize(text):
    return text.translate(_TRANS)


def extract_numbers(text):
    """Return the numbers in `text` as ASCII strings, in order of appearance."""
    return _NUM.findall(normalize(text))


def check(text, locked_numbers):
    """Compare numbers in `text` with `locked_numbers`.

    Returns (ok, missing, unexpected):
      missing    - locked numbers that do not appear in the text
      unexpected - numbers in the text that are not locked
    ok is True only when both lists are empty.
    """
    locked = [normalize(str(n)) for n in locked_numbers]
    found = set(extract_numbers(text))
    missing = sorted({n for n in locked if n not in found})
    unexpected = sorted(n for n in found if n not in set(locked))
    return (not missing and not unexpected, missing, unexpected)
