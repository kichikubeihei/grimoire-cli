# Grimoire Algorithmica: Summon Arcane Familiar (Windows PowerShell Installer)
$ErrorActionPreference = "Stop"

$FamiliarDir = "$HOME\.grimoire"
if (-not (Test-Path $FamiliarDir)) {
    New-Item -ItemType Directory -Path $FamiliarDir -Force | Out-Null
}

Write-Host "================================================================" -ForegroundColor Magenta
Write-Host " 🧙‍♂️ GRIMOIRE ALGORITHMICA // THE ARCANE FAMILIAR (WINDOWS)" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Magenta

$ScriptPath = "$FamiliarDir\familiar.py"
Write-Host "[*] Inscribing Arcane Familiar into $ScriptPath..." -ForegroundColor Gray
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/kichikubeihei/grimoire-cli/main/grimoire-familiar.py" -OutFile $ScriptPath

$PythonCmd = if (Get-Command "python" -ErrorAction SilentlyContinue) { "python" } elseif (Get-Command "python3" -ErrorAction SilentlyContinue) { "python3" } else { $null }

if (-not $PythonCmd) {
    Write-Host "[!] Error: Python 3.8+ is required to awaken the Familiar." -ForegroundColor Red
    exit 1
}

Write-Host "[*] Awakening Familiar on your local GPU/CPU..." -ForegroundColor Green
& $PythonCmd $ScriptPath $args
