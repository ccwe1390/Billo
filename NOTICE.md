# Third-party notices

BillScan ships these third-party files unchanged under app/static/. Each
license text is in the repo next to the files.

| Component | Where | License | License file |
|---|---|---|---|
| Web Awesome CSS (Fonticons; files kept, no page loads them since 2026-10-17) | app/static/vendor/webawesome/ | MIT | app/static/vendor/webawesome/LICENSE.md |
| Font Awesome Free SVGs embedded in Web Awesome's native.css | app/static/vendor/webawesome/native.css | per fontawesome.com/license/free (attribution comments kept in the file; terms not re-read) | - |
| IBM Plex Sans, Sans Arabic, Sans Devanagari | app/static/fonts/ | SIL Open Font License 1.1 | app/static/fonts/OFL-*.txt |
| Phosphor icons | app/static/icons/ | MIT | app/static/icons/LICENSE-phosphor.txt |
| qrcode-generator 2.0.4 (Kazuhiko Arase) | app/static/vendor/qrcode-generator/qrcode.js | MIT | app/static/vendor/qrcode-generator/LICENSE |
| Atkinson Hyperlegible (Braille Institute of America) | app/static/fonts/atkinson-hyperlegible-*.woff2 | SIL Open Font License 1.1 | app/static/fonts/OFL-atkinson-hyperlegible.txt |

The project's own license is not chosen yet (Evan's decision).

qrcode-generator: dist/qrcode.js from cdn.jsdelivr.net (npm qrcode-generator@2.0.4),
56,694 bytes, sha256 79ec86f82856005b1c887905cfccfcfbec3821ca61c7fd5a952faa5f778f791c,
equal to jsDelivr's published hash (checked 2026-10-17). The npm package ships no
LICENSE file, so LICENSE (MIT, 1,071 bytes, sha256
3a850fa5f08101db6f40676c2786e10bd2cd5fff7b12ffdf1e0c434d4e49d90c) is from the
project's GitHub repo (master branch). Downloaded with Evan's approval.

Atkinson Hyperlegible: 4 woff2 files (latin and latin-ext, weights 400 and 700) from
cdn.jsdelivr.net, npm @fontsource/atkinson-hyperlegible@5.3.0, plus its LICENSE.
Each file's sha256 equals jsDelivr's published hash (checked 2026-10-17):
- latin-400: 17,208 bytes, d64ba838ef5472bba248620ec4fd8b5aa7cf0db2908e0bb230600caf279ba7bc
- latin-700: 17,524 bytes, 140e2bd25a7315c8a062508391426b0d8c3297400c947b8d847be28f73a199f0
- latin-ext-400: 9,384 bytes, 61eeb0eb8b881a84d069e67be1723f5b353b0b9b866ad8e7ad9dba66cdc4dabd
- latin-ext-700: 9,372 bytes, 840ced16f975d8abc2594b436d0206649e0c2a7327e36750ff849d3d37c3c02e
- LICENSE (OFL-atkinson-hyperlegible.txt): jsDelivr hash 4TfK7vL/fAT7+HB4rQnPPcuoo6WKSqTi85nULFC8Sxg= (base64)
Downloaded with Evan's approval.

Design credit: the colour tokens, type scale and component patterns of the UI
(dark theme, Atkinson Hyperlegible, option buttons, field-state surfaces, the
percent headline) are adapted from Dipayan's React frontend on the
feature/frontend branch (PR #1), ported to the vanilla app on 2026-10-17.
