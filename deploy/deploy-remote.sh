#!/bin/bash
# Runs ON the VM: deploy-remote.sh <commit>. Backup, stage, import-check, swap, restart.
# Stops at the first failure; before the swap nothing live has changed.
set -e
C="$1"
test -n "$C"
tar -cf ~/backup-before-$C.tar -C /opt/bill-to-help app
echo "backup: $(ls -la ~/backup-before-$C.tar | awk '{print $5, $9}')"
rm -rf ~/stage-$C && mkdir ~/stage-$C && tar -xf ~/deploy-$C.tar -C ~/stage-$C
cd ~/stage-$C && FAKE_OCI=1 /opt/bill-to-help/.venv/bin/python -c "import app.main; print('import check: ok')"
rm -rf /opt/bill-to-help/app.old
mv /opt/bill-to-help/app /opt/bill-to-help/app.old
mv ~/stage-$C/app /opt/bill-to-help/app
sudo systemctl restart bill-to-help
sleep 3
echo "service: $(systemctl is-active bill-to-help)"
echo "uvicorn processes: $(pgrep -fc 'uvicorn app.main:app')"
echo "DEPLOYED $C"
