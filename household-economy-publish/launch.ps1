param([switch]$NoBrowser,[int]$Port=8501)
$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
$localPython=Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$workspaceRoot=Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$bundledDeps=Join-Path $workspaceRoot 'work\pydeps'
$runtimePython='C:\Program Files\WindowsApps\OpenAI.CodexPrimaryRuntime.v26-1105-1297-0_26.1105.1297.0_x64__3k8sg7r9htsxt\dependencies\python\python.exe'
if (Test-Path -LiteralPath $localPython) {
    $selectedPython=$localPython
    $env:PYTHONPATH=$PSScriptRoot
} elseif ((Test-Path -LiteralPath $runtimePython) -and (Test-Path -LiteralPath (Join-Path $bundledDeps 'streamlit'))) {
    $selectedPython=$runtimePython
    $env:PYTHONPATH=$bundledDeps+';'+$PSScriptRoot
} else {
    throw 'Run setup.ps1 once to install the local environment, then launch again.'
}
$env:PYTHONUTF8='1'
if (-not $NoBrowser) { Start-Process ('http://127.0.0.1:'+ $Port) }
& $selectedPython -m streamlit run app.py --global.developmentMode false --server.headless true --server.address 127.0.0.1 --server.port $Port --browser.gatherUsageStats false
