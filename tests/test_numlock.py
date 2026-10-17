"""Plain-assert tests for app/numlock.py. Run: py tests/test_numlock.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import numlock  # noqa: E402

# extraction
assert numlock.extract_numbers("Pay $4,812.40 by 2026-10-01.") == ["4,812.40", "2026-10-01"]
assert numlock.extract_numbers("Total is 115.") == ["115"]          # trailing period is not part of it
assert numlock.extract_numbers("10/01/2026 and 3-4") == ["10/01/2026", "3-4"]
assert numlock.extract_numbers("no digits here") == []
assert numlock.extract_numbers("Nov 5, 2026") == ["5", "2026"]       # ", " (with space) splits

# Arabic-Indic digits normalize to ASCII (incl. Arabic separators)
assert numlock.extract_numbers("١١٥") == ["115"]
assert numlock.extract_numbers("٣٣٬٠٠٠") == ["33,000"]
assert numlock.extract_numbers("۴۸۱۲٫۴۰") == ["4812.40"]

# Devanagari digits normalize to ASCII
dev = "४,८१२.४०"  # 4,812.40
assert numlock.extract_numbers(dev) == ["4,812.40"]
assert numlock.check(dev, ["4,812.40"])[0]

# fullwidth digits normalize to ASCII
assert numlock.extract_numbers("１１５") == ["115"]

# check: all match
ok, missing, unexpected = numlock.check("Your income is 115% of the limit; 4 people; $38,000.", ["115", "4", "38,000"])
assert ok and missing == [] and unexpected == []

# check: Arabic string with Arabic-Indic digits matches ASCII locked numbers
ar = "دخلك ١١٥٪ من الحد، ٣٨٬٠٠٠ دولار، ٤ أشخاص"
ok, missing, unexpected = numlock.check(ar, ["115", "38,000", "4"])
assert ok, (missing, unexpected)

# check: a changed number is both missing and unexpected
ok, missing, unexpected = numlock.check("Income $38,500 for 4 people", ["38,000", "4"])
assert not ok and missing == ["38,000"] and unexpected == ["38,500"]

# check: an invented extra number is unexpected
ok, missing, unexpected = numlock.check("115 and 99", ["115"])
assert not ok and missing == [] and unexpected == ["99"]

# check: a dropped number is missing
ok, missing, unexpected = numlock.check("only 115", ["115", "4"])
assert not ok and missing == ["4"] and unexpected == []

# check: no numbers at all is ok only if nothing is locked
assert numlock.check("hello", [])[0]
assert not numlock.check("hello", ["1"])[0]

# check: a number only in `allowed` may appear (not unexpected) and is not required (not missing)
ok, missing, unexpected = numlock.check("115 and 240", ["115"], allowed=["240", "100"])
assert ok and missing == [] and unexpected == []
ok, missing, unexpected = numlock.check("115", ["115"], allowed=["240"])
assert ok and missing == [] and unexpected == []
ok, missing, unexpected = numlock.check("115 and 99", ["115"], allowed=["240"])
assert not ok and unexpected == ["99"]

print("ALL PASS")
