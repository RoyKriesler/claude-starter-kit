# run-job.ps1 - runner wrapper for Lazy Obsidian Method recurring jobs.
# Invoked by Windows Task Scheduler. Calls claude CLI with the matching template.
#
# Usage:
#   .\run-job.ps1 -Job daily-ingest
#   .\run-job.ps1 -Job nightly-review
#   .\run-job.ps1 -Job weekly-vault

[CmdletBinding()]
param(
  [Parameter(Mandatory)]
  [ValidateSet("daily-ingest", "nightly-review", "weekly-vault")]
  [string]$Job
)

$ErrorActionPreference = "Stop"

$VaultRoot   = Join-Path $env:USERPROFILE "ObsidianVault"
$Template    = Join-Path $VaultRoot "00_Index\Templates\$Job.md"
$Today       = Get-Date -Format "yyyy-MM-dd"

$LogSubdir = switch ($Job) {
  "daily-ingest"    { "ingest" }
  "nightly-review"  { "reviews\nightly" }
  "weekly-vault"    { "reviews\weekly" }
}

$LogDir  = Join-Path $VaultRoot "00_Index\Logs\$LogSubdir"
$RawLog  = Join-Path $LogDir "${Today}_${Job}_runner.log"

if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

if (-not (Test-Path $Template)) {
  "ERROR: template not found: $Template" | Out-File -FilePath $RawLog -Encoding utf8
  exit 1
}

$Prompt = @"
Today is $Today. Read the spec at $Template and execute every step in order.
Vault root: $VaultRoot.
Write your job log to the path the spec specifies. Do not skip steps.
"@

"=== $Job runner started $(Get-Date -Format o) ===" | Out-File -FilePath $RawLog -Encoding utf8

$Claude = (Get-Command claude -ErrorAction Stop).Source
& $Claude `
  -p $Prompt `
  --add-dir $VaultRoot `
  --permission-mode acceptEdits `
  --model sonnet `
  --max-budget-usd 2 `
  --output-format text `
  2>&1 | Out-File -FilePath $RawLog -Append -Encoding utf8

"=== exit code: $LASTEXITCODE - finished $(Get-Date -Format o) ===" | Out-File -FilePath $RawLog -Append -Encoding utf8
exit $LASTEXITCODE
