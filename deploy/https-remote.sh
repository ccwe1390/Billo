#!/bin/bash
# Runs ON the VM: https-remote.sh. Adds HTTPS (Let's Encrypt IP certificate) next to the
# unchanged :80 site. Every Apache change is configtest-ed before a graceful reload; a
# failing stage removes its own file(s) and stops. After every reload, http://127.0.0.1/
# must still answer 200, or the stage is undone and httpd restarted.
set -u
IP=207.211.181.174
CERT=billscan-ip
CONF=/etc/httpd/conf.d
step() { echo; echo "== $*"; }
http_ok() { for i in 1 2 3 4 5; do c=$(curl -s -o /dev/null -w '%{http_code}' -m 5 http://127.0.0.1/); [ "$c" = 200 ] && return 0; sleep 1; done; echo "http://127.0.0.1/ answered $c"; return 1; }
reload_or_undo() {  # $@ = files to remove if the reload fails
  if ! sudo apachectl configtest; then echo "configtest FAILED - undoing"; sudo rm -f "$@"; sudo apachectl configtest; exit 1; fi
  sudo apachectl graceful
  if ! http_ok; then echo "port 80 broken after reload - undoing"; sudo rm -f "$@"; sudo systemctl restart httpd; http_ok && echo "port 80 restored"; exit 1; fi
  echo "reload ok, http 200"
}

step "A. mod_ssl"
if ! rpm -q mod_ssl >/dev/null; then
  sudo dnf install -y -q mod_ssl || { echo "dnf install mod_ssl FAILED"; exit 1; }
  # EL9 makes the default self-signed localhost cert in httpd-init.service; graceful does not run it
  [ -f /etc/pki/tls/certs/localhost.crt ] || sudo systemctl start httpd-init.service
  if ! sudo apachectl configtest; then echo "configtest FAILED after mod_ssl - removing it"; sudo dnf remove -y -q mod_ssl; sudo apachectl configtest; exit 1; fi
  sudo apachectl graceful
  http_ok || { echo "port 80 broken after mod_ssl - removing it"; sudo dnf remove -y -q mod_ssl; sudo systemctl restart httpd; exit 1; }
fi
rpm -q mod_ssl

step "B. certbot in /opt/certbot"
if [ ! -x /opt/certbot/bin/certbot ]; then
  sudo /usr/bin/python3.12 -m venv /opt/certbot && sudo /opt/certbot/bin/pip install -q 'certbot==5.8.0' || { echo "certbot install FAILED"; exit 1; }
fi
/opt/certbot/bin/certbot --version
/opt/certbot/bin/certbot --help all | grep -q -- '--ip-address' || { echo "certbot has no --ip-address"; exit 1; }
/opt/certbot/bin/certbot --help all | grep -q -- '--preferred-profile' || { echo "certbot has no --preferred-profile"; exit 1; }

step "C. serve /.well-known/acme-challenge/ from Apache (loads before billo.conf)"
sudo mkdir -p /var/www/acme/.well-known/acme-challenge
sudo tee $CONF/billo-acme.conf >/dev/null <<'EOF'
# Let's Encrypt HTTP-01 challenge files are served by Apache itself, not proxied to the app.
ProxyPass /.well-known/acme-challenge/ !
Alias /.well-known/acme-challenge/ /var/www/acme/.well-known/acme-challenge/
<Directory /var/www/acme/.well-known/acme-challenge>
    Require all granted
</Directory>
EOF
reload_or_undo $CONF/billo-acme.conf
echo probe-ok | sudo tee /var/www/acme/.well-known/acme-challenge/probe >/dev/null
p=$(curl -s -m 5 http://127.0.0.1/.well-known/acme-challenge/probe); sudo rm -f /var/www/acme/.well-known/acme-challenge/probe
[ "$p" = probe-ok ] || { echo "challenge path not served (got: $p)"; exit 1; }
echo "challenge path served"

step "D. certificate (IP, shortlived profile, no email)"
if [ ! -f /etc/letsencrypt/live/$CERT/fullchain.pem ]; then
  sudo /opt/certbot/bin/certbot certonly --webroot -w /var/www/acme --cert-name $CERT \
    --ip-address $IP --preferred-profile shortlived \
    --agree-tos --register-unsafely-without-email --non-interactive || { echo "certbot FAILED - http unchanged"; exit 1; }
fi
sudo restorecon -R /etc/letsencrypt 2>/dev/null
sudo openssl x509 -in /etc/letsencrypt/live/$CERT/fullchain.pem -noout -subject -ext subjectAltName -enddate

step "E. HTTPS site on 443 (same proxy as :80; no redirect, no HSTS)"
sudo tee $CONF/billo-ssl.conf >/dev/null <<EOF
# HTTPS for the same app: Apache :443 -> uvicorn 127.0.0.1:8000. Cert: certbot lineage $CERT.
<VirtualHost *:443>
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
reload_or_undo $CONF/billo-ssl.conf
c=$(curl -s -o /dev/null -w '%{http_code}' -m 10 --connect-to $IP:443:127.0.0.1:443 https://$IP/)
echo "https://$IP/ (certificate verified by curl): $c"
[ "$c" = 200 ] || { echo "HTTPS check FAILED - removing the 443 site"; sudo rm -f $CONF/billo-ssl.conf; sudo apachectl graceful; http_ok; exit 1; }
echo "HTTPS DONE"
