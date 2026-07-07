# PowerShell Commands for R

This document provides PowerShell examples for working with R. For most tasks, prefer using the bundled scripts in `r-code` skill instead.

## Running R Code

To execute arbitrary R code:

```powershell
& "C:\Program Files\R\R-4.5.2\bin\Rscript.exe" -e "[code to call]"
```

**Note**: The `scripts/run_r.ps1` script in the r-code skill automatically locates installed R versions and is preferred over hardcoding paths.

## Common Tasks

### Test Package
```powershell
& "C:\Program Files\R\R-4.5.2\bin\Rscript.exe" -e "devtools::test()"
```

### Document Package
```powershell
& "C:\Program Files\R\R-4.5.2\bin\Rscript.exe" -e "devtools::document()"
```

### Run R CMD Check
```powershell
& "C:\Program Files\R\R-4.5.2\bin\Rscript.exe" -e "devtools::check()"
```

## Formatting with Air

```powershell
& 'C:\Users\pbulsink\.local\bin\air.exe' format .
```

For a specific file:
```powershell
& 'C:\Users\pbulsink\.local\bin\air.exe' format path\to\file.R
```