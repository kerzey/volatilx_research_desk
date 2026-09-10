# Launch the research desk with credentials loaded, from PowerShell.
# PowerShell talks to the native Claude Code .exe over a real console, so no winpty is needed.
#
#   .\scripts\start_desk.ps1            normal desk session
#   .\scripts\start_desk.ps1 -Admin     maintenance session (enforcement code writable)
param([switch]$Admin)

$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')

if (-not (Test-Path '.env.research')) {
    Write-Error "no .env.research in $(Get-Location) - see README Step 3"
}

# Parse KEY=VALUE lines; ignore comments and blanks. Values are not unquoted beyond
# stripping one matching pair of surrounding quotes.
foreach ($line in Get-Content '.env.research') {
    $t = $line.Trim()
    if ($t -eq '' -or $t.StartsWith('#')) { continue }
    $i = $t.IndexOf('=')
    if ($i -lt 1) { continue }
    $k = $t.Substring(0, $i).Trim()
    $v = $t.Substring($i + 1).Trim()
    if ($v.Length -ge 2 -and (($v.StartsWith('"') -and $v.EndsWith('"')) -or ($v.StartsWith("'") -and $v.EndsWith("'")))) {
        $v = $v.Substring(1, $v.Length - 2)
    }
    Set-Item -Path "env:$k" -Value $v
}

if (-not $env:RESEARCH_DB_URL) { Write-Error 'RESEARCH_DB_URL not set after reading .env.research' }

if ($Admin) {
    $env:DESK_ADMIN = '1'
    Write-Host 'DESK_ADMIN=1 - enforcement code is writable this session.' -ForegroundColor Yellow
}

claude @args
