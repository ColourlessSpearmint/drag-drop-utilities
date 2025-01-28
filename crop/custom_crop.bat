@echo off
cd /d %~dp0
set /p width=Enter desired width: 
set /p height=Enter desired height: 
set /p position=Enter position (top-left, center-center, etc.): 
python crop.py %* --custom %width% %height% %position%

:: Check if the script is being run interactively
if "%1"=="__nopause" goto :EOF

pause
