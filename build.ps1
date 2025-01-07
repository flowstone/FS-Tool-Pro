# Build.ps1 for cleanFS-Tool-Pro

# Default option is to run build, like a Makefile
param(
    [string]$Task = "build"
)

$buildFSToolPro = {
    Write-Host "正在打包FS-Tool-Pro..."
    python -m nuitka --show-progress --assume-yes-for-downloads app.py
}

$cleanFSToolPro = {
    Write-Host "Cleaning..."
    Remove-Item -Recurse -Force app.exe, ./app.build/, ./app.dist/, ./app.onefile-build/ ,/build/ ,/dist/ ,FS-Tool-Pro.spec
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