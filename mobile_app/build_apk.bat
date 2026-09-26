@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ============================================================
echo   YouTube Downloader - Android APK Builder
echo ============================================================
echo.

echo This script helps you build the Android APK.
echo.
echo Choose your build method:
echo.
echo 1. GitHub Actions (RECOMMENDED - No setup needed!)
echo 2. Google Colab (Free, runs in browser)
echo 3. WSL / Linux (If you have WSL installed)
echo 4. Local Buildozer (Advanced - requires full setup)
echo.

set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo ============================================================
    echo GITHUB ACTIONS METHOD (RECOMMENDED)
    echo ============================================================
    echo.
    echo 1. Push this folder to a GitHub repository
    echo 2. Go to your repo > Actions > "Build APK" workflow
    echo 3. Click "Run workflow"
    echo 4. Download the APK from Artifacts when done
    echo.
    echo No local setup required! Free for public repos.
    echo.
    pause
    goto :eof
)

if "%choice%"=="2" (
    echo.
    echo ============================================================
    echo GOOGLE COLAB METHOD (FREE)
    echo ============================================================
    echo.
    echo 1. Open: https://colab.research.google.com/
    echo 2. Create new notebook
    echo 3. Run these cells one by one:
    echo.
    echo Cell 1: !pip install buildozer
    echo Cell 2: !git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
    echo Cell 3: %cd YOUR_REPO/mobile_app
    echo Cell 4: !apt update && apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
    echo Cell 5: !buildozer -v android debug
    echo Cell 6: from google.colab import files; files.download('/content/YOUR_REPO/mobile_app/bin/*.apk')
    echo.
    pause
    goto :eof
)

if "%choice%"=="3" (
    echo.
    echo ============================================================
    echo WSL / LINUX METHOD
    echo ============================================================
    echo.
    echo Run these commands in your WSL/Linux terminal:
    echo.
    echo cd ~/youtube-downloader/mobile_app
    echo pip install buildozer
    echo sudo apt update && sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
    echo buildozer -v android debug
    echo.
    echo The APK will be in ./bin/ folder
    echo.
    pause
    goto :eof
)

if "%choice%"=="4" (
    echo.
    echo ============================================================
    echo LOCAL BUILDOZER (WINDOWS)
    echo ============================================================
    echo.
    echo WARNING: This requires full buildozer setup on Windows
    echo which is complex. Recommended to use methods 1-3 instead.
    echo.
    echo If you still want to try:
    echo 1. Install Python 3.11+
    echo 2. Install Java JDK 17
    echo 3. pip install buildozer
    echo 4. buildozer -v android debug
    echo.
    echo See: https://buildozer.readthedocs.io/en/latest/installation.html
    echo.
    pause
    goto :eof
)

echo Invalid choice!
pause