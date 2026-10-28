param(
    [Parameter(Mandatory=$true)][string]$Mod,
    [ValidateSet('Debug','Release')][string]$Configuration = 'Release',
    [string]$GameDir = $env:SOD_GAME_DIR
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if ($Mod -notmatch '^(characters|features)/[a-z][a-z0-9-]*$') { throw 'Pass -Mod characters/<slug> or features/<slug>.' }
$folder = Join-Path (Join-Path $root 'mods') $Mod
$manifestPath = Join-Path $folder 'mod.project.json'
if (-not (Test-Path $manifestPath)) { throw "Unknown mod: $Mod" }
if ([string]::IsNullOrWhiteSpace($GameDir)) { throw 'Set SOD_GAME_DIR or pass -GameDir pointing to your installed Shape of Dreams folder.' }
if (-not (Test-Path (Join-Path $GameDir 'Shape of Dreams_Data/Managed/Dew.Core.dll'))) { throw "Dew.Core.dll not found under $GameDir" }
$manifest = Get-Content -Raw $manifestPath | ConvertFrom-Json
python (Join-Path $root 'tools/validate.py')
if ($LASTEXITCODE -ne 0) { throw 'Manifest validation failed' }
$csproj = Join-Path $folder $manifest.project
& dotnet build $csproj -c $Configuration "-p:GameDir=$GameDir"
if ($LASTEXITCODE -ne 0) { throw 'dotnet build failed' }
python (Join-Path $root 'tools/package.py') --mod $Mod --configuration $Configuration
if ($LASTEXITCODE -ne 0) { throw 'Packaging failed' }
