# Third-party notices

BillScan ships these third-party files unchanged under app/static/. Each
license text is in the repo next to the files.

| Component | Where | License | License file |
|---|---|---|---|
| Web Awesome CSS (Fonticons) | app/static/vendor/webawesome/ | MIT | app/static/vendor/webawesome/LICENSE.md |
| Font Awesome Free SVGs embedded in Web Awesome's native.css | app/static/vendor/webawesome/native.css | per fontawesome.com/license/free (attribution comments kept in the file; terms not re-read) | - |
| IBM Plex Sans, Sans Arabic, Sans Devanagari | app/static/fonts/ | SIL Open Font License 1.1 | app/static/fonts/OFL-*.txt |
| Phosphor icons | app/static/icons/ | MIT | app/static/icons/LICENSE-phosphor.txt |
| qrcode-generator 2.0.4 (Kazuhiko Arase) | app/static/vendor/qrcode-generator/qrcode.js | MIT | app/static/vendor/qrcode-generator/LICENSE |

The project's own license is not chosen yet (Evan's decision).

qrcode-generator: dist/qrcode.js from cdn.jsdelivr.net (npm qrcode-generator@2.0.4),
56,694 bytes, sha256 79ec86f82856005b1c887905cfccfcfbec3821ca61c7fd5a952faa5f778f791c,
equal to jsDelivr's published hash (checked 2026-10-17). The npm package ships no
LICENSE file, so LICENSE (MIT, 1,071 bytes, sha256
3a850fa5f08101db6f40676c2786e10bd2cd5fff7b12ffdf1e0c434d4e49d90c) is from the
project's GitHub repo (master branch). Downloaded with Evan's approval.
