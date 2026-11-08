# One-time: gh auth login -h github.com -p https -w
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$gh = $env:GH_EXE
if (-not $gh -or -not (Test-Path $gh)) {
    $ghZip = "$env:TEMP\gh_cli.zip"
    $ghDir = "$env:TEMP\gh_cli"
    if (-not (Test-Path $ghZip)) {
        curl.exe -fsSL -o $ghZip "https://github.com/cli/cli/releases/download/v2.63.2/gh_2.63.2_windows_amd64.zip"
    }
    if (-not (Test-Path "$ghDir\bin\gh.exe")) {
        Expand-Archive -Path $ghZip -DestinationPath $ghDir -Force
    }
    $gh = (Get-ChildItem -Path $ghDir -Recurse -Filter gh.exe | Select-Object -First 1).FullName
}

& $gh auth status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Войдите в GitHub (откроется браузер)..."
    & $gh auth login -h github.com -p https -w
}

$repoName = "stepik-course"
& $gh repo create $repoName --public --source=. --remote=origin --push
Write-Host "Готово. URL:"
& $gh repo view --web -w 2>$null
& $gh repo view --json url -q ".url"
