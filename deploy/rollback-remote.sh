#!/bin/bash
# Runs ON the VM: rollback-remote.sh <commit-that-was-deployed>. Restores the backup taken before it.
set -e
C="$1"
test -f ~/backup-before-$C.tar
rm -rf /opt/bill-to-help/app
tar -xf ~/backup-before-$C.tar -C /opt/bill-to-help
sudo systemctl restart bill-to-help
sleep 3
echo "service: $(systemctl is-active bill-to-help)"
echo "ROLLED BACK (restored backup-before-$C)"
