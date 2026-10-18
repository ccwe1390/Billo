#!/bin/bash
# Runs ON the VM: https-name-remote.sh (Evan 2026-10-18 ~12:40 CDT: billow.duckdns.org).
# Adds https://billow.duckdns.org/ next to the IP site: a Let's Encrypt certificate for the name
# (webroot; the :80 ACME path is still served) and a second *:443 vhost with ServerName.
# The file is bill-to-help-tls-name.conf so it sorts AFTER bill-to-help-ssl.conf: the first *:443
# vhost answers requests with no matching name, and that must stay the IP site.
# http redirect keeps the name: billow.duckdns.org -> https://billow.duckdns.org, else -> the IP
# (never %{HTTP_HOST} blindly: that would be an open redirect to any Host header).
set -u
IP=207.211.181.174
NAME=billow.duckdns.org
CERT=billow-duckdns
CONF=/etc/httpd/conf.d
V=$CONF/bill-to-help-tls-name.conf
R=$CONF/bill-to-help-https-only.conf
sudo cp $R /tmp/https-only.bak
undo() { echo "FAILED: $* - undoing"; sudo rm -f $V; sudo cp /tmp/https-only.bak $R; sudo apachectl graceful; sleep 2
  echo "after undo: https IP $(curl -s -o /dev/null -w '%{http_code}' -m 10 --connect-to $IP:443:127.0.0.1:443 https://$IP/)"; exit 1; }

echo "== DNS"; d=$(getent ahostsv4 $NAME | awk '{print $1; exit}'); echo "$NAME -> $d"; [ "$d" = $IP ] || { echo "DNS not pointing here"; exit 1; }

echo "== certificate"
if [ ! -f /etc/letsencrypt/live/$CERT/fullchain.pem ]; then
  sudo /opt/certbot/bin/certbot certonly --webroot -w /var/www/acme --cert-name $CERT -d $NAME \
    --agree-tos --register-unsafely-without-email --non-interactive || { echo "certbot FAILED - nothing changed"; exit 1; }
fi
sudo restorecon -R /etc/letsencrypt 2>/dev/null
sudo openssl x509 -in /etc/letsencrypt/live/$CERT/fullchain.pem -noout -subject -enddate

echo "== vhost + redirect"
sudo tee $V >/dev/null <<EOF
# https://$NAME/ : same proxy as the IP site; certificate lineage $CERT.
<VirtualHost *:443>
    ServerName $NAME
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/$CERT/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/$CERT/privkey.pem
    ProxyPreserveHost On
    ProxyPass /.well-known/acme-challenge/ !
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
    LimitRequestBody 10485760
</VirtualHost>
EOF
sudo tee $R >/dev/null <<'EOF'
# http -> https for everything but the ACME challenge (server context only covers :80; the
# *:443 vhosts do not inherit these rules, and the HTTPS guard keeps them from looping anyway).
# billow.duckdns.org keeps its name; any other Host goes to the IP (no open redirect).
RewriteEngine On
RewriteCond %{HTTPS} !=on
RewriteCond %{REQUEST_URI} !^/\.well-known/acme-challenge/
RewriteCond %{HTTP_HOST} ^billow\.duckdns\.org(:80)?$ [NC]
RewriteRule ^ https://billow.duckdns.org%{REQUEST_URI} [R=308,L]
RewriteCond %{HTTPS} !=on
RewriteCond %{REQUEST_URI} !^/\.well-known/acme-challenge/
RewriteRule ^ https://207.211.181.174%{REQUEST_URI} [R=308,L]
EOF
sudo apachectl configtest || undo configtest
sudo apachectl graceful; sleep 2

echo "== checks"
for u in / /stats /app.js; do
  a=$(curl -s -o /dev/null -w '%{http_code}' -m 10 --connect-to $NAME:443:127.0.0.1:443 https://$NAME$u); echo "https $NAME$u -> $a"; [ "$a" = 200 ] || undo "name $u"
  b=$(curl -s -o /dev/null -w '%{http_code}' -m 10 --connect-to $IP:443:127.0.0.1:443 https://$IP$u); echo "https $IP$u -> $b"; [ "$b" = 200 ] || undo "ip $u"
done
r1=$(curl -s -o /dev/null -w '%{http_code} %{redirect_url}' -m 5 -H "Host: $NAME" "http://127.0.0.1/stats?x=1"); echo "http name -> $r1"
[ "$r1" = "308 https://$NAME/stats?x=1" ] || undo "name redirect"
r2=$(curl -s -o /dev/null -w '%{http_code} %{redirect_url}' -m 5 "http://127.0.0.1/stats?x=1"); echo "http ip -> $r2"
[ "$r2" = "308 https://$IP/stats?x=1" ] || undo "ip redirect"
r3=$(curl -s -o /dev/null -w '%{http_code} %{redirect_url}' -m 5 -H "Host: evil.example" "http://127.0.0.1/"); echo "http other host -> $r3"
[ "$r3" = "308 https://$IP/" ] || undo "other host redirect"
echo probe-ok | sudo tee /var/www/acme/.well-known/acme-challenge/probe >/dev/null
p=$(curl -s -m 5 http://127.0.0.1/.well-known/acme-challenge/probe); sudo rm -f /var/www/acme/.well-known/acme-challenge/probe
echo "acme probe: $p"; [ "$p" = probe-ok ] || undo "acme path"
echo "NAME OK"
