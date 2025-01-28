@echo off
cd /d %~dp0
python scale.py %*

:: Check if the script is being run interactively
if "%1"=="__nopause" goto :EOF

pause
