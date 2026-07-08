# PowerShell Commands for R

This document provides PowerShell examples for working with R. For most tasks, prefer using the bundled scripts in `r-code` skill instead.

## Running R Code

To execute arbitrary R code, use the bundled script:

```powershell
& "$PSScriptRoot/../../scripts/run_r.ps1" -e "[code to call]"
```

This automatically locates the installed R version and is preferred over hardcoding paths.

### Direct Rscript (fallback)

If the bundled script is unavailable, locate R dynamically:

```powershell
$rPaths = @(
    "C:\Program Files\R\R-4*\bin\Rscript.exe"
)
$rScript = Get-ChildItem $rPaths -ErrorAction SilentlyContinue | Select-Object -First 1
if ($rScript) { & $rScript.FullName -e "[code to call]" }
```

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