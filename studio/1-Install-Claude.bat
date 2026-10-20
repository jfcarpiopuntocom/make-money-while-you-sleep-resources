@echo off
REM 1-Install-Claude.bat
REM Double-click me once. I run the official Claude Code installer from Anthropic
REM (the same command shown at https://code.claude.com/docs/en/setup).
REM No administrator rights needed. Nothing else on your computer is changed.

echo.
echo  Hello! I am going to install Claude Code, your AI assistant.
echo  This uses the official installer from Anthropic.
echo  It can take a few minutes and may show no progress. That is normal.
echo.
pause

powershell -NoProfile -Command "irm https://claude.ai/install.ps1 | iex"

echo.
echo  Done. Next step: close this window and double-click 2-Start-My-Studio.bat
echo  The first time, Claude will ask you to log in with your Claude account.
echo.
echo  If you saw red error text, copy it, open claude.ai in your browser,
echo  and paste it there with: "I was installing Claude Code and got this error."
echo.
pause
