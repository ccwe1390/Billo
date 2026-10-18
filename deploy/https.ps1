# PowerShell 5.1: .\https.ps1   - copies https-remote.sh to the VM and runs it (HTTPS next to the unchanged :80 site).
$key = Join-Path $HOME '.ssh\HackTN26.pem'
$vm = 'opc@207.211.181.174'
scp -i $key (Join-Path $PSScriptRoot 'https-remote.sh') "${vm}:~/"
if ($LASTEXITCODE -ne 0) { Write-Host 'scp failed'; exit 1 }
ssh -i $key $vm 'bash ~/https-remote.sh'
if ($LASTEXITCODE -ne 0) { Write-Host "HTTPS SETUP STOPPED (exit $LASTEXITCODE) - read the lines above; http on port 80 is checked after every step"; exit 1 }
