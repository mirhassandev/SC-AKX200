REM SC-AKX200 Control Panel VBScript Launcher
REM This script runs the batch file without showing any console window

Set objShell = CreateObject("WScript.Shell")
objShell.Run "SC-AKX200.bat", 0, False
