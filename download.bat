@echo off
setlocal enabledelayedexpansion

REM ========================================
REM  YouTube Downloader - 480p Edition
REM ========================================

title YouTube Downloader - 480p

echo.
echo ============================================================
echo           YouTube Downloader - 480p Edition
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if yt-dlp is installed
yt-dlp --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] yt-dlp is not installed. Installing now...
    echo.
    pip install yt-dlp
    if errorlevel 1 (
        echo [ERROR] Failed to install yt-dlp
        echo Please run this command manually:
        echo pip install yt-dlp
        echo.
        pause
        exit /b 1
    )
    echo [OK] yt-dlp installed successfully
    echo.
)

:START_LOOP
echo.
echo ============================================================
echo  Enter YouTube link (or type 'exit' to quit):
echo ============================================================
set /p URL="> "

REM Check if user wants to exit
if /i "%URL%"=="exit" goto :END
if /i "%URL%"=="quit" goto :END
if /i "%URL%"=="q" goto :END

if "%URL%"=="" (
    echo [ERROR] No URL provided!
    goto :START_LOOP
)

REM Run Python script
echo.
echo Starting download...
echo.
python "%~dp0downloader.py" "%URL%"

REM Check result
if errorlevel 1 (
    echo.
    echo [FAILED] Download was not successful
) else (
    echo.
    echo [SUCCESS] Download completed successfully!
)

echo.
echo ============================================================
echo  Download finished! Enter another link or type 'exit' to quit
echo ============================================================

goto :START_LOOP

:END
echo.
echo ============================================================
echo  Thank you for using YouTube Downloader!
echo ============================================================
echo.

pause
