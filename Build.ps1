# Build.ps1 for cleanFSToolPro

# Default option is to run build, like a Makefile
param(
    [string]$Task = "build"
)

$buildFSToolPro = {
    Write-Host "Building FSToolPro..."
    python -m nuitka --show-progress --assume-yes-for-downloads FSToolPro.py
}

$cleanFSToolPro = {
    Write-Host "Cleaning..."
    Remove-Item -Recurse -Force FSToolPro.exe, ./FSToolPro.build/, ./FSToolPro.dist/, ./FSToolPro.onefile-build/
}

switch ($Task.ToLower()) {
    "build" {
        & $buildFSToolPro
        break
    }
    "clean" {
        & $cleanFSToolPro
        break
    }
    default {
        Write-Host "Unknown task: $Task" -ForegroundColor Red
        Write-Host "Available tasks: build, clean"
        break
    }
}