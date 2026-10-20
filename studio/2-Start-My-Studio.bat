@echo off
REM 2-Start-My-Studio.bat
REM Double-click me every time you want to work. I open your My-Studio folder
REM and start Claude Code inside it, so Claude reads your handbook (CLAUDE.md).
REM 3- and 4- call me with an extra word (--continue or --resume).

REM Use the My-Studio folder next to me; if you moved it to your user folder, use that one.
set "STUDIO=%~dp0My-Studio"
if not exist "%STUDIO%\CLAUDE.md" set "STUDIO=%USERPROFILE%\My-Studio"
if not exist "%STUDIO%\CLAUDE.md" (
  echo.
  echo  I cannot find your My-Studio folder.
  echo  Put it next to this file, or in %USERPROFILE%\My-Studio, and try again.
  echo.
  pause
  exit /b 1
)

REM Find Claude: the normal command, or the place the official installer puts it.
set "CLAUDE=claude"
where claude >nul 2>&1 || set "CLAUDE=%USERPROFILE%\.local\bin\claude.exe"
if not "%CLAUDE%"=="claude" if not exist "%CLAUDE%" (
  echo.
  echo  Claude Code is not installed yet. Double-click 1-Install-Claude.bat first.
  echo.
  pause
  exit /b 1
)

REM Let Claude read the Master Prompts in the kit's prompts folder (if it is there).
set "EXTRA="
for %%I in ("%~dp0..\prompts") do set "PROMPTS=%%~fI"
if exist "%PROMPTS%" set EXTRA=--add-dir "%PROMPTS%"

cd /d "%STUDIO%"
echo.
echo  Opening your studio in %STUDIO%
echo  Type to Claude in plain words. Press Esc to stop it. Type /exit to leave.
echo.
"%CLAUDE%" %EXTRA% %*
pause
