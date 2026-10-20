@echo off
rem Starts the AI engine room. Options: start-ai.bat [auto ^| kobold ^| no-kobold]
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start-ai.ps1" %*
echo.
pause
