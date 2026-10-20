# start-ai.ps1 - starts your AI engine room. Called by start-ai.bat. Everything stays on 127.0.0.1; keys are never printed.
param([string]$Mode = "auto")   # auto | kobold | no-kobold
$ErrorActionPreference = "Continue"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogDir = Join-Path $Here "logs"; New-Item -ItemType Directory -Force $LogDir | Out-Null
$Log = Join-Path $LogDir ("{0:yyyyMMdd}.log" -f (Get-Date))
function Log($m) { $l = "{0:HH:mm:ss} {1}" -f (Get-Date), $m; Add-Content -Path $Log -Value $l; Write-Host $l }
function PortUp($p) { [bool](Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue) }
function FreeRamGB { [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 1) }

Log "=== AI engine room (mode: $Mode) ==="

# 0. Configuration (created from the example on first run)
$CfgPath = Join-Path $Here "config.json"
if (-not (Test-Path $CfgPath)) {
  Copy-Item (Join-Path $Here "config.example.json") $CfgPath
  Log "Created config.json from the example. Edit it, then run this again."
}
$Cfg = Get-Content $CfgPath -Raw -Encoding UTF8 | ConvertFrom-Json
$L = $Cfg.launcher
$OmniUrl = [Uri]$Cfg.omniroute_url
$OmniPort = $OmniUrl.Port
$RouterPort = [int]$Cfg.router_port
$DataDir = if ($L.omniroute_data_dir) { $L.omniroute_data_dir } else { Join-Path $env:USERPROFILE ".omniroute" }
$Keep = if ($L.backups_keep) { [int]$L.backups_keep } else { 7 }
$MinRam = if ($L.min_free_ram_gb) { [double]$L.min_free_ram_gb } else { 4.5 }

$Py = Get-Command python -ErrorAction SilentlyContinue
if (-not $Py) { Log "Python 3 was not found. Install it from python.org and run this again."; exit 1 }

# 1. OmniRoute up (only if it is installed)
if (-not (PortUp $OmniPort)) {
  $cmd = if ($L.omniroute_command) { $L.omniroute_command } else { "omniroute" }
  if (Get-Command $cmd -ErrorAction SilentlyContinue) {
    Start-Process $cmd -WindowStyle Hidden; Log "OmniRoute was not running: started it (waiting 20 s)"; Start-Sleep 20
  } else { Log "OmniRoute is not installed or not on PATH (see README, step 1)." }
}
Log ("OmniRoute ${OmniPort}: " + $(if (PortUp $OmniPort) { "OK" } else { "not responding" }))

# 2. Router
if (-not (PortUp $RouterPort)) {
  Start-Process python -ArgumentList "`"$Here\router.py`"" -WindowStyle Hidden; Start-Sleep 3; Log "Router started"
}
Log ("Router ${RouterPort}: " + $(if (PortUp $RouterPort) { "OK" } else { "not responding" }))

# 3. Optional local model (KoboldCPP), only if there is enough free RAM
$ram = FreeRamGB
$kPort = if ($L.kobold_port) { [int]$L.kobold_port } else { 5001 }
$want = ($Mode -eq "kobold") -or ($Mode -eq "auto" -and $ram -ge $MinRam)
if ($Mode -eq "no-kobold") { Log "Local model: skipped by option" }
elseif (-not $L.kobold_exe -or -not $L.kobold_model) { Log "Local model: not configured (optional)" }
elseif (PortUp $kPort) { Log "Local model: already running" }
elseif ($want -and (Test-Path $L.kobold_exe) -and (Test-Path $L.kobold_model)) {
  Start-Process $L.kobold_exe -ArgumentList '--model', "`"$($L.kobold_model)`"", '--usevulkan', '--gpulayers', '99', '--contextsize', '4096', '--port', "$kPort", '--host', '127.0.0.1', '--skiplauncher', '--quiet' -WindowStyle Hidden
  Log "Local model started (free RAM $ram GB; loading takes 1-2 minutes)"
} else { Log "Local model not started (free RAM $ram GB, needs $MinRam GB; or files missing). Force with: start-ai.bat kobold" }

# 4. Dated backup of OmniRoute's database (keeps the last $Keep)
$db = Join-Path $DataDir "storage.sqlite"
if (Test-Path $db) {
  $bk = Join-Path $DataDir "backups"; New-Item -ItemType Directory -Force $bk | Out-Null
  $today = Join-Path $bk ("storage-{0:yyyyMMdd}.sqlite" -f (Get-Date))
  if (-not (Test-Path $today)) {
    python -c "import sqlite3,sys; s=sqlite3.connect(sys.argv[1]); d=sqlite3.connect(sys.argv[2]); s.backup(d); d.close(); s.close()" $db $today
    Get-ChildItem $bk -Filter "storage-*.sqlite" | Sort-Object Name -Descending | Select-Object -Skip $Keep | Remove-Item -Confirm:$false
    Log "Backup saved: $today (last $Keep kept)"
  } else { Log "Backup for today already exists" }
} else { Log "No OmniRoute database found at $db (skipping backup; set launcher.omniroute_data_dir if it lives elsewhere)" }

# 5. Real test call through the fallback chain
try {
  $r = python (Join-Path $Here "llm.py") "Reply with only: OK" 2>$null
  Log ("Test call (pool/text): " + $(if ($r -match "OK") { "OK" } else { "unexpected reply or no engine answered: $r" }))
} catch { Log "Test call failed: $_" }

Log "Ready. To delegate a task: python `"$Here\llm.py`" `"instruction`" [file]. Log: $Log"
