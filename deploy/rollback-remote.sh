#!/bin/bash
# Runs ON the VM: rollback-remote.sh <commit-that-was-deployed>. Restores the backup taken before it.
set -e
C="$1"
test -f ~/backup-before-$C.tar
rm -rf /opt/bill-to-help/app
tar -xf ~/backup-before-$C.tar -C /opt/bill-to-help
sudo systemctl restart bill-to-help
for i in 1 2 3 4 5 6 7 8 9 10; do curl -fsS -o /dev/null http://127.0.0.1:8000/stats && break; sleep 1; done
systemctl is-active --quiet bill-to-help || { echo "FAILED: service not active after rollback"; exit 1; }
curl -fsS -o /dev/null http://127.0.0.1:8000/stats || { echo "FAILED: /stats does not answer after rollback"; exit 1; }
echo "ROLLED BACK (restored backup-before-$C)"
