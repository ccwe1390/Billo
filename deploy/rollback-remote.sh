#!/bin/bash
# Runs ON the VM: rollback-remote.sh <commit-that-was-deployed>. Restores the backup taken before it.
# The backup is extracted to a temp dir first, then swapped in, so a bad tar never leaves app/ half-deleted.
set -e
C="$1"
test -n "$C"
trap 'echo "FAILED: line $LINENO - rollback did not finish, read the lines above"' ERR
exec 9>~/deploy.lock
flock -n 9 || { echo "FAILED: another deploy or rollback is running"; exit 1; }
test -f ~/backup-before-$C.tar || { echo "FAILED: ~/backup-before-$C.tar is not on the VM"; exit 1; }
rm -rf ~/rollback-stage-$C && mkdir ~/rollback-stage-$C
tar -xf ~/backup-before-$C.tar -C ~/rollback-stage-$C
test -d ~/rollback-stage-$C/app
rm -rf /opt/bill-to-help/app.rolledback
if [ -d /opt/bill-to-help/app ]; then mv /opt/bill-to-help/app /opt/bill-to-help/app.rolledback; fi
mv ~/rollback-stage-$C/app /opt/bill-to-help/app
sudo systemctl restart bill-to-help
for i in 1 2 3 4 5 6 7 8 9 10; do curl -fsS -o /dev/null http://127.0.0.1:8000/stats && break; sleep 1; done
systemctl is-active --quiet bill-to-help || { echo "FAILED: service not active after rollback"; exit 1; }
curl -fsS -o /dev/null http://127.0.0.1:8000/stats || { echo "FAILED: /stats does not answer after rollback"; exit 1; }
echo "ROLLED BACK (restored backup-before-$C)"
