# Fetches third-party Agent Skills into skills/<skill-name>/ (pruned).
# Run from repo root: powershell -File scripts/vendor-external-skills.ps1

$ErrorActionPreference = "Stop"

function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$GitArguments)
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & git @GitArguments 2>&1 | ForEach-Object { Write-Host $_ }
    $code = $LASTEXITCODE
    $ErrorActionPreference = $prev
    if ($code -ne 0) { throw "git $($GitArguments -join ' ') failed (exit $code)" }
}

$RepoRoot = Split-Path $PSScriptRoot -Parent
if (-not (Test-Path (Join-Path $RepoRoot "AGENTS.md"))) {
    throw "Run from ai_base_doc repo (AGENTS.md not found at $RepoRoot)"
}

$SkillsRoot = Join-Path $RepoRoot "skills"
$Temp = Join-Path $env:TEMP "ai_base_doc_skill_vendor"

$PruneFileNames = @(
    "LICENSE.txt", "LICENSE", "SOURCE.md", "CREATION-LOG.md",
    "find-polluter.sh", "condition-based-waiting-example.ts"
)
$PrunePatterns = @("test-pressure-*.md", "test-academic.md")

function Remove-PrunedFiles {
    param([string]$Dir)
    foreach ($name in $PruneFileNames) {
        $p = Join-Path $Dir $name
        if (Test-Path $p) { Remove-Item $p -Force }
    }
    foreach ($pat in $PrunePatterns) {
        Get-ChildItem -Path $Dir -Filter $pat -File -ErrorAction SilentlyContinue |
            Remove-Item -Force
    }
}

function Install-Skill {
    param(
        [string]$Src,
        [string]$SkillName
    )
    if (-not (Test-Path $Src)) {
        throw "Missing skill path: $Src"
    }
    $dest = Join-Path $SkillsRoot $SkillName
    if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
    New-Item -ItemType Directory -Path $dest -Force | Out-Null
    Copy-Item -Path (Join-Path $Src "*") -Destination $dest -Recurse -Force
    Remove-PrunedFiles -Dir $dest
    Get-ChildItem -Path $dest -Recurse -File | ForEach-Object {
        foreach ($name in $PruneFileNames) {
            if ($_.Name -eq $name) { Remove-Item $_.FullName -Force }
        }
    }
    $skillMd = Join-Path $dest "SKILL.md"
    if (Test-Path $skillMd) {
        $text = Get-Content $skillMd -Raw
        $text = $text -replace '(?m)^license:.*\r?\n', ''
        Set-Content -Path $skillMd -Value $text.TrimEnd() -Encoding utf8 -NoNewline
        Add-Content -Path $skillMd -Value "`n" -Encoding utf8
    }
    Write-Host "OK skills/$SkillName"
}

Write-Host "Skills root: $SkillsRoot"
if (Test-Path $Temp) { Remove-Item $Temp -Recurse -Force }
New-Item -ItemType Directory -Path $Temp -Force | Out-Null

$sp = Join-Path $Temp "superpowers"
Invoke-Git clone --depth 1 https://github.com/obra/superpowers.git $sp
foreach ($name in @(
        "verification-before-completion",
        "systematic-debugging",
        "requesting-code-review",
        "test-driven-development"
    )) {
    Install-Skill -Src (Join-Path $sp "skills\$name") -SkillName $name
}

$anth = Join-Path $Temp "anthropics-skills"
Invoke-Git clone --depth 1 --filter=blob:none --sparse https://github.com/anthropics/skills.git $anth
Push-Location $anth
Invoke-Git sparse-checkout set skills/webapp-testing
Pop-Location
Install-Skill -Src (Join-Path $anth "skills\webapp-testing") -SkillName "webapp-testing"

$ac = Join-Path $Temp "awesome-copilot"
Invoke-Git clone --depth 1 --filter=blob:none --sparse https://github.com/github/awesome-copilot.git $ac
Push-Location $ac
Invoke-Git sparse-checkout set skills/security-review skills/acquire-codebase-knowledge skills/refactor-plan skills/openapi-to-application-code skills/postgresql-code-review
Pop-Location
foreach ($name in @(
        "security-review",
        "acquire-codebase-knowledge",
        "refactor-plan",
        "openapi-to-application-code",
        "postgresql-code-review"
    )) {
    Install-Skill -Src (Join-Path $ac "skills\$name") -SkillName $name
}

$dib = Join-Path $Temp "cursor-skills"
Invoke-Git clone --depth 1 https://github.com/DIBmaster/cursor-skills.git $dib
Install-Skill -Src (Join-Path $dib "skills\pre-deploy-checklist") -SkillName "pre-deploy-checklist"

$vendorDir = Join-Path $SkillsRoot "vendor"
if (Test-Path $vendorDir) {
    Remove-Item $vendorDir -Recurse -Force
    Write-Host "Removed skills/vendor/"
}

Remove-Item $Temp -Recurse -Force
Write-Host "Done. Catalog: skills/SOURCES.md"
