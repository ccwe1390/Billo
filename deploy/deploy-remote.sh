#!/bin/bash
# Runs ON the VM: deploy-remote.sh <commit>. Backup, stage, import-check, swap, restart.
# Stops at the first failure; before the swap nothing live has changed. After restart: health check (service active + /stats answers), else FAILED.
# Safe to re-run: one deploy at a time (flock), an existing backup is kept, a half-finished swap is repaired from app.old.
set -e
C="$1"
test -n "$C"
trap 'echo "FAILED: line $LINENO - run deploy.ps1 -Commit $C -Rollback"' ERR
exec 9>~/deploy.lock
flock -n 9 || { echo "FAILED: another deploy is running"; exit 1; }
if [ ! -d /opt/bill-to-help/app ] && [ -d /opt/bill-to-help/app.old ]; then
  mv /opt/bill-to-help/app.old /opt/bill-to-help/app
  echo "recovered: app/ was missing, restored app.old"
fi
if [ -f ~/backup-before-$C.tar ]; then
  echo "backup: keeping existing $(ls -la ~/backup-before-$C.tar | awk '{print $5, $9}')"
else
  tar -cf ~/backup-before-$C.tar.part -C /opt/bill-to-help app
  mv ~/backup-before-$C.tar.part ~/backup-before-$C.tar
  echo "backup: $(ls -la ~/backup-before-$C.tar | awk '{print $5, $9}')"
fi
rm -rf ~/stage-$C
mkdir ~/stage-$C
tar -xf ~/deploy-$C.tar -C ~/stage-$C
cd ~/stage-$C && FAKE_OCI=1 /opt/bill-to-help/.venv/bin/python -c "import app.main as m; m._rules(); print('import check: ok')"
test -d /opt/bill-to-help/app
test -d ~/stage-$C/app
rm -rf /opt/bill-to-help/app.old
mv /opt/bill-to-help/app /opt/bill-to-help/app.old
mv ~/stage-$C/app /opt/bill-to-help/app
sudo systemctl restart bill-to-help
for i in 1 2 3 4 5 6 7 8 9 10; do curl -fsS -o /dev/null http://127.0.0.1:8000/stats && break; sleep 1; done
systemctl is-active --quiet bill-to-help || { echo "FAILED: service not active - run deploy.ps1 -Commit $C -Rollback"; exit 1; }
curl -fsS -o /dev/null http://127.0.0.1:8000/stats || { echo "FAILED: /stats does not answer - run deploy.ps1 -Commit $C -Rollback"; exit 1; }
echo "uvicorn processes: $(pgrep -fc 'uvicorn app.main:app')"
echo "DEPLOYED $C (service active, /stats 200)"
