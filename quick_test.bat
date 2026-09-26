@echo off
echo.
echo ============================================================
echo          YouTube Downloader - Quick Test
echo ============================================================
echo.

REM Test Python
echo [1/2] Testing Python...
python --version
if errorlevel 1 (
    echo [FAIL] Python not found
    pause
    exit /b 1
)
echo.

REM Test downloader script
echo [2/2] Testing downloader script...
python "%~dp0downloader.py" --version 2>nul
if errorlevel 1 (
    echo [OK] Downloader script is ready
)

echo.
echo ============================================================
echo All tests passed! You can now use download.bat
echo ============================================================
echo.

pause
