$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
python -m venv .venv
if ($LASTEXITCODE -ne 0) { throw 'Python 3.12 or later is required.' }
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed. See the message above.' }
Write-Host 'Ready. Run Launch Lab.cmd or .\launch.ps1'
