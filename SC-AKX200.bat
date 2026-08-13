@echo off
REM SC-AKX200 Control Panel Launcher
REM Silently check and install dependencies, then launch the app

cd /d "%~dp0"

REM Run silent dependency installer using pythonw (no console window)
if exist pythonw.exe (
    start /b pythonw.exe install_deps.py
) else (
    REM Fallback if pythonw not available
    python.exe install_deps.py >nul 2>&1
)

REM Launch the main app
python.exe panasonic_akx200_control.py
