# Running R Code — Terminal/PowerShell Fallback

> **Prefer the live session first.** Posit Assistant has built-in access to your active R/Python console. Run code in that live session using its built-in R tool before reaching for any terminal command. This document is only for when no live session is available (e.g. running outside Positron/RStudio, or a task that needs a fresh isolated process).

When you do need the terminal route, prefer the bundled script over hardcoding paths:

```powershell
& "$PSScriptRoot/../../scripts/run_r.ps1" -e "[code to call]"
```

This automatically locates the installed R version.

### Direct Rscript (fallback)

If the bundled script is unavailable, locate R dynamically:

```powershell
$rPaths = @(
    "C:\Program Files\R\R-4*\bin\Rscript.exe"
)
$rScript = Get-ChildItem $rPaths -ErrorAction SilentlyContinue | Select-Object -First 1
if ($rScript) { & $rScript.FullName -e "[code to call]" }
```

On macOS/Linux the equivalent is simply `Rscript -e "[code to call]"`.

## Common Tasks

### Test Package
```powershell
& "$PSScriptRoot/../../scripts/run_r.ps1" -e "devtools::test()"
```

### Document Package
```powershell
& "$PSScriptRoot/../../scripts/run_r.ps1" -e "devtools::document()"
```

### Run R CMD Check
```powershell
& "$PSScriptRoot/../../scripts/run_r.ps1" -e "devtools::check()"
```

## Formatting with Air

```powershell
& 'air' format .
```

For a specific file:
```powershell
& 'air' format path\to\file.R
```