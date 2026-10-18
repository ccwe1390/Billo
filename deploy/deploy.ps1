# PowerShell 5.1: .\deploy.ps1 -Commit cc3c333        (deploy)
#                  .\deploy.ps1 -Commit cc3c333 -Rollback  (restore the backup taken before it)
# The archive goes through a file and scp, never a PowerShell pipe (5.1 pipes corrupt binary data).
param([Parameter(Mandatory = $true)][string]$Commit, [switch]$Rollback)
$key = Join-Path $HOME '.ssh\HackTN26.pem'
$vm = 'opc@207.211.181.174'
if ($Rollback) {
    scp -i $key (Join-Path $PSScriptRoot 'rollback-remote.sh') "${vm}:~/"
    if ($LASTEXITCODE -ne 0) { Write-Host 'scp failed'; exit 1 }
    ssh -i $key $vm "bash ~/rollback-remote.sh $Commit"
    exit $LASTEXITCODE
}
$tar = Join-Path $env:TEMP "deploy-$Commit.tar"
git -C 'C:\ClaudeCode\TNHacks27' archive -o $tar $Commit app
if ($LASTEXITCODE -ne 0) { Write-Host 'git archive failed'; exit 1 }
scp -i $key $tar (Join-Path $PSScriptRoot 'deploy-remote.sh') "${vm}:~/"
if ($LASTEXITCODE -ne 0) { Write-Host 'scp failed'; exit 1 }
ssh -i $key $vm "bash ~/deploy-remote.sh $Commit"
if ($LASTEXITCODE -ne 0) { Write-Host "REMOTE DEPLOY FAILED (exit $LASTEXITCODE) - read the lines above"; exit 1 }
