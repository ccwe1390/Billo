#!/bin/bash
# Runs ON the VM: deploy-remote.sh <commit>. Backup, stage, import-check, swap, restart.
# Stops at the first failure; before the swap nothing live has changed. After restart: health check (service active + /stats answers), else FAILED.
set -e
C="$1"
test -n "$C"
tar -cf ~/backup-before-$C.tar -C /opt/bill-to-help app
echo "backup: $(ls -la ~/backup-before-$C.tar | awk '{print $5, $9}')"
rm -rf ~/stage-$C && mkdir ~/stage-$C && tar -xf ~/deploy-$C.tar -C ~/stage-$C
cd ~/stage-$C && FAKE_OCI=1 /opt/bill-to-help/.venv/bin/python -c "import app.main as m; m._rules(); print('import check: ok')"
rm -rf /opt/bill-to-help/app.old
mv /opt/bill-to-help/app /opt/bill-to-help/app.old
mv ~/stage-$C/app /opt/bill-to-help/app
sudo systemctl restart bill-to-help
for i in 1 2 3 4 5 6 7 8 9 10; do curl -fsS -o /dev/null http://127.0.0.1:8000/stats && break; sleep 1; done
systemctl is-active --quiet bill-to-help || { echo "FAILED: service not active - run deploy.ps1 -Commit $C -Rollback"; exit 1; }
curl -fsS -o /dev/null http://127.0.0.1:8000/stats || { echo "FAILED: /stats does not answer - run deploy.ps1 -Commit $C -Rollback"; exit 1; }
echo "uvicorn processes: $(pgrep -fc 'uvicorn app.main:app')"
echo "DEPLOYED $C (service active, /stats 200)"
