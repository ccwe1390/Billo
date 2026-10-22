#!/bin/bash
# Runs ON the VM: https-only-remote.sh (Evan 2026-10-18 ~12:31 CDT: "only support https").
# Every http:// request gets a 308 to the same https:// URL (308 keeps POST a POST), except the
# Let's Encrypt HTTP-01 challenge path, which the certificate renewal still needs on :80.
# configtest before a graceful reload; any failed check removes the file and reloads again.
# Undo by hand: sudo rm /etc/httpd/conf.d/billo-https-only.conf && sudo apachectl graceful
set -u
IP=207.211.181.174
F=/etc/httpd/conf.d/billo-https-only.conf
undo() { echo "FAILED: $* - undoing"; sudo rm -f $F; sudo apachectl graceful; sleep 2; echo "http after undo: $(curl -s -o /dev/null -w '%{http_code}' -m 5 http://127.0.0.1/)"; exit 1; }
sudo tee $F >/dev/null <<'EOF'
# http -> https for everything but the ACME challenge (server context only covers :80; the
# *:443 vhost does not inherit these rules, and the HTTPS guard keeps it from looping anyway).
RewriteEngine On
RewriteCond %{HTTPS} !=on
RewriteCond %{REQUEST_URI} !^/\.well-known/acme-challenge/
RewriteRule ^ https://207.211.181.174%{REQUEST_URI} [R=308,L]
EOF
sudo apachectl configtest || undo "configtest"
sudo apachectl graceful; sleep 2
r=$(curl -s -o /dev/null -w '%{http_code} %{redirect_url}' -m 5 "http://127.0.0.1/stats?x=1"); echo "http /stats?x=1 -> $r"
[ "$r" = "308 https://207.211.181.174/stats?x=1" ] || undo "http redirect"
echo probe-ok | sudo tee /var/www/acme/.well-known/acme-challenge/probe >/dev/null
p=$(curl -s -m 5 http://127.0.0.1/.well-known/acme-challenge/probe); sudo rm -f /var/www/acme/.well-known/acme-challenge/probe
echo "acme probe over http: $p"; [ "$p" = probe-ok ] || undo "acme path"
for u in / /stats /app.js; do
  c=$(curl -s -o /dev/null -w '%{http_code}' -m 10 --connect-to $IP:443:127.0.0.1:443 https://$IP$u); echo "https $u -> $c"
  [ "$c" = 200 ] || undo "https $u"
done
echo "HTTPS-ONLY OK"
