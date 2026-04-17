param(
    [Parameter(Mandatory = $true)]
    [string]$Title,
    [string]$Root = "."
)

$adrDir = Join-Path $Root "production_artifacts/ADRs"
if (-not (Test-Path -LiteralPath $adrDir)) {
    New-Item -ItemType Directory -Path $adrDir -Force | Out-Null
}

$existing = Get-ChildItem -LiteralPath $adrDir -File -Filter "ADR-*.md" -ErrorAction SilentlyContinue
$numbers = @($existing | ForEach-Object {
    if ($_.BaseName -match "^ADR-(\\d{4})") { [int]$matches[1] }
})
$next = if ($numbers.Count -gt 0) { ($numbers | Measure-Object -Maximum).Maximum + 1 } else { 1 }
$slug = ($Title.ToLower() -replace "[^a-z0-9]+", "-").Trim("-")
$fileName = "ADR-{0:D4}-{1}.md" -f $next, $slug
$path = Join-Path $adrDir $fileName

$content = @"
# ADR-$("{0:D4}" -f $next): $Title

## Status
Proposed

## Context

## Decision

## Consequences

## Follow-up
"@

Set-Content -LiteralPath $path -Value $content -Encoding UTF8
Write-Output $path
