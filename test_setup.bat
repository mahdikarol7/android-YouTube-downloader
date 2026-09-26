@echo off

echo.
echo ============================================================
echo                    System Test
echo ============================================================
echo.

REM Test Python
echo [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo       [FAIL] Python is not installed
    echo       Solution: Download and install from https://www.python.org
) else (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo       [OK] %%i
)

echo.

REM Test pip
echo [2/4] Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo       [FAIL] pip is not working
) else (
    for /f "tokens=*" %%i in ('pip --version 2^>^&1') do echo       [OK] %%i
)

echo.

REM Test yt-dlp
echo [3/4] Checking yt-dlp...
yt-dlp --version >nul 2>&1
if errorlevel 1 (
    echo       [WARNING] yt-dlp is not installed (will be auto-installed)
) else (
    for /f "tokens=*" %%i in ('yt-dlp --version 2^>^&1') do echo       [OK] Version %%i
)

echo.

REM Test ffmpeg
echo [4/4] Checking ffmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo       [WARNING] ffmpeg is not installed (optional but recommended)
    echo       Solution: https://ffmpeg.org
) else (
    echo       [OK] ffmpeg is installed
)

echo.
echo ============================================================
echo Test completed!
echo ============================================================
echo.

pause
