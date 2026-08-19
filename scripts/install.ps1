[CmdletBinding()]
param(
    [string]$Destination = $(
        if ($env:CODEX_SKILLS_DIR) { $env:CODEX_SKILLS_DIR }
        else { Join-Path $HOME ".agents/skills" }
    ),
    [switch]$Copy
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$skillsRoot = Join-Path $repoRoot "skills"
$destinationRoot = [IO.Path]::GetFullPath($Destination)

if (-not (Test-Path -LiteralPath $skillsRoot -PathType Container)) {
    throw "Skills root not found: $skillsRoot"
}

New-Item -ItemType Directory -Force -Path $destinationRoot | Out-Null

$seen = @{}
$installed = 0
$existing = 0
$skipped = 0

Get-ChildItem -LiteralPath $skillsRoot -Filter "SKILL.md" -File -Recurse |
    Sort-Object FullName |
    ForEach-Object {
        $skillFile = $_
        $skillDir = $skillFile.Directory.FullName
        $nameLine = Get-Content -LiteralPath $skillFile.FullName -TotalCount 30 |
            Where-Object { $_ -match '^name:\s*' } |
            Select-Object -First 1

        if (-not $nameLine) {
            throw "Missing frontmatter name: $($skillFile.FullName)"
        }

        $name = ($nameLine -replace '^name:\s*', '').Trim('"', "'")
        if ($name -notmatch '^[a-z0-9][a-z0-9-]{0,63}$') {
            throw "Invalid skill name '$name' in $($skillFile.FullName)"
        }
        if ($seen.ContainsKey($name)) {
            throw "Duplicate skill name '$name': $skillDir and $($seen[$name])"
        }
        $seen[$name] = $skillDir

        $target = Join-Path $destinationRoot $name
        if (Test-Path -LiteralPath $target) {
            $item = Get-Item -LiteralPath $target -Force
            $resolvedTarget = $null
            if ($item.LinkType) {
                try { $resolvedTarget = [IO.Path]::GetFullPath([string]$item.Target) } catch {}
            }

            if ($resolvedTarget -and $resolvedTarget -eq $skillDir) {
                Write-Host "EXISTS $name -> $skillDir"
                $existing++
            } else {
                Write-Warning "SKIP ${name}: destination already exists and is not this repository link: $target"
                $skipped++
            }
            return
        }

        if ($Copy) {
            Copy-Item -LiteralPath $skillDir -Destination $target -Recurse
            Write-Host "COPIED $name -> $target"
        } elseif ($env:OS -eq 'Windows_NT') {
            New-Item -ItemType Junction -Path $target -Target $skillDir | Out-Null
            Write-Host "LINKED $name -> $skillDir"
        } else {
            New-Item -ItemType SymbolicLink -Path $target -Target $skillDir | Out-Null
            Write-Host "LINKED $name -> $skillDir"
        }
        $installed++
    }

Write-Host "Skills discovered: $($seen.Count)"
Write-Host "Installed: $installed; already linked: $existing; skipped conflicts: $skipped"

if ($skipped -gt 0) {
    exit 2
}
