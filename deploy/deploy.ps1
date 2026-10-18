# PowerShell 5.1: .\deploy.ps1 -Commit cc3c333        (deploy)
#                  .\deploy.ps1 -Commit cc3c333 -Rollback  (restore the backup taken before it)
#                  .\deploy.ps1 -Commit cc3c333 -Watch     (print the remote log again, e.g. after a dropped connection)
#                  .\deploy.ps1 -Commit cc3c333 -Rollback -Watch  (same, for the rollback log)
# The archive goes through a file and scp, never a PowerShell pipe (5.1 pipes corrupt binary data).
# The remote script runs under nohup with its output in ~/deploy-<c>.log (~/rollback-<c>.log), so a dropped ssh does not kill it.
# Exit codes: 0 done, 1 failed, 2 network dropped (remote step keeps running; use -Watch), 3 -Watch found no result yet.
param([Parameter(Mandatory = $true)][string]$Commit, [switch]$Rollback, [switch]$Watch)
$key = Join-Path $HOME '.ssh\HackTN26.pem'
$vm = 'opc@207.211.181.174'
$sshOpts = @('-o', 'ConnectTimeout=10', '-o', 'ServerAliveInterval=5', '-o', 'ServerAliveCountMax=3', '-o', 'BatchMode=yes')
if ($Rollback) { $what = 'rollback' } else { $what = 'deploy' }
$log = "~/$what-$Commit.log"

# Copies files to the VM home dir; up to 3 tries, 10 s apart. Returns $true or $false.
function Send-ToVm([string[]]$Files) {
    for ($try = 1; $try -le 3; $try++) {
        scp -i $key @sshOpts @Files "${vm}:~/" | Out-Host
        if ($LASTEXITCODE -eq 0) { return $true }
        Write-Host "scp failed (try $try of 3, exit $LASTEXITCODE)"
        if ($try -lt 3) { Start-Sleep -Seconds 10 }
    }
    return $false
}

# Runs one command on the VM, prints its output, sets $script:rc (ssh exit code) and $script:out (text).
function Invoke-Vm([string]$Cmd) {
    $lines = @(ssh -i $key @sshOpts $vm $Cmd)
    $script:rc = $LASTEXITCODE
    $lines | ForEach-Object { Write-Host $_ }
    $script:out = $lines -join "`n"
}

if ($Watch) {
    Invoke-Vm "cat $log"
    if ($script:rc -eq 255) { Write-Host 'NETWORK DROPPED - the remote step keeps running; re-run with -Watch'; exit 2 }
    if ($script:rc -ne 0) { Write-Host "no log $log on the VM (exit $script:rc) - the remote step never started"; exit 1 }
    if ($script:out -match '(?m)^(DEPLOYED |ROLLED BACK)') { exit 0 }
    if ($script:out -match 'FAILED') { exit 1 }
    Write-Host 'NO RESULT YET - the remote step may still be running; re-run with -Watch'
    exit 3
}

if ($Rollback) {
    $files = @((Join-Path $PSScriptRoot 'rollback-remote.sh'))
    $remote = 'nohup bash ~/rollback-remote.sh {0} > ~/rollback-{0}.log 2>&1; rc=$?; cat ~/rollback-{0}.log; exit $rc' -f $Commit
} else {
    $tar = Join-Path $env:TEMP "deploy-$Commit.tar"
    git -C 'C:\ClaudeCode\TNHacks27' archive -o $tar $Commit app
    if ($LASTEXITCODE -ne 0) { Write-Host 'git archive failed'; exit 1 }
    $files = @($tar, (Join-Path $PSScriptRoot 'deploy-remote.sh'))
    $remote = 'nohup bash ~/deploy-remote.sh {0} > ~/deploy-{0}.log 2>&1; rc=$?; cat ~/deploy-{0}.log; exit $rc' -f $Commit
}
if (-not (Send-ToVm $files)) { Write-Host 'scp failed'; exit 1 }
Invoke-Vm $remote
if ($script:rc -eq 255) { Write-Host 'NETWORK DROPPED - the remote step keeps running; re-run with -Watch'; exit 2 }
if ($script:rc -ne 0) { Write-Host "REMOTE $($what.ToUpper()) FAILED (exit $script:rc) - read the lines above"; exit 1 }
exit 0
