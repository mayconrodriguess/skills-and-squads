param(
    [string]$Root = "."
)

$folders = @(
    ".agents",
    ".agents/skills",
    ".agents/workflows",
    "app_build",
    "production_artifacts",
    "scripts",
    "references",
    "assets"
)

foreach ($folder in $folders) {
    $path = Join-Path $Root $folder
    if (-not (Test-Path -LiteralPath $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
}

Write-Output "Project structure verified."
