@echo off
setlocal ENABLEDELAYEDEXPANSION

:: Get the path of the directory where this script resides
set "scriptDir=%~dp0"
set "outputFile=%scriptDir%composited.png"

:: Check if at least one argument was passed
if "%~1"=="" (
    echo Error: No image files provided.
    echo Usage: composite_images.bat image1.png image2.jpg ...
    pause
    exit /b 1
)

:: Build a list of input files
set "inputFiles="
:loop
if "%~1"=="" goto process
set "inputFiles=!inputFiles! "%~1""
shift
goto loop

:process
:: Compose images horizontally using ImageMagick v7
magick %inputFiles% +append "!outputFile!"

if errorlevel 1 (
    echo Failed to composite images.
) else (
    echo Composited image saved as: "!outputFile!"
)

endlocal
