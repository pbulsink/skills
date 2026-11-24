# Run R code using Rscript

# Try to find R installation
$rPaths = @(
    "C:\Program Files\R\R-4.6.1\bin\Rscript.exe"
)

$rScript = $null
foreach ($path in $Paths) {
    if (Test-Path $path) {
        $rScript = $path
        break
    }
}

if (-not $rScript) {
    Write-Error "R not found. Please install R or update script paths."
    exit 1
}

# Execute the provided command
& $rScript @args