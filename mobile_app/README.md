# YouTube Downloader - Mobile App (Kivy)

A simple, clean mobile app for downloading YouTube videos built with Kivy.

## Features

- 🎥 **Download YouTube videos** at multiple qualities (360p, 480p, 720p, 1080p)
- 📱 **Clean, simple mobile UI** - easy to use
- 📋 **Paste from clipboard** button
- 📊 **Real-time progress bar** with percentage
- 📝 **Saves video description** as .txt file automatically
- 🔄 **Auto-retry** with fallback formats on errors
- 📁 **Organized downloads** - each video in its own folder

## Requirements

- Python 3.8+
- Kivy 2.3+
- yt-dlp
- FFmpeg (for audio/video merging)

## Running on Desktop (for testing)

```bash
cd mobile_app
python main.py
```

## Building for Android

### Option 1: Using Buildozer (Linux/macOS/WSL)

```bash
# Install buildozer
pip install buildozer

# Install system dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Build APK
buildozer -v android debug
```

### Option 2: Using GitHub Actions (Recommended - No Linux needed!)

Create `.github/workflows/build.yml`:

```yaml
name: Build APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - name: Install buildozer
      run: pip install buildozer
    - name: Install dependencies
      run: |
        sudo apt update
        sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
    - name: Build APK
      run: buildozer -v android debug
      working-directory: ./mobile_app
    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: YouTubeDownloader-APK
        path: mobile_app/bin/*.apk
```

Then push to GitHub and download the APK from Actions artifacts.

### Option 3: Google Colab (Free, no setup)

1. Open [Google Colab](https://colab.research.google.com/)
2. Run these cells:

```python
# Cell 1: Install buildozer
!pip install buildozer

# Cell 2: Clone your repo or upload files
!git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
%cd YOUR_REPO/mobile_app

# Cell 3: Install system deps
!apt update && apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Cell 4: Build
!buildozer -v android debug

# Cell 5: Download APK
from google.colab import files
files.download('/content/YOUR_REPO/mobile_app/bin/youtubedownloader-1.0.0-armeabi-v7a-debug.apk')
```

## Project Structure

```
mobile_app/
├── main.py              # Main Kivy app
├── buildozer.spec       # Buildozer configuration
└── README.md            # This file
```

## Features in Detail

### Quality Options
| Quality | Best For |
|---------|----------|
| 360p    | Slow connections, saving data |
| 480p    | **Recommended** - balanced quality/size |
| 720p    | HD viewing |
| 1080p   | Full HD, larger files |

### Error Handling
- Automatic retry with fallback formats
- Connection/SSL error recovery
- 403 Forbidden error handling
- yt-dlp auto-update option

### Download Organization
```
Download Folder/
└── Video Title_YYYYMMDD_HHMMSS/
    ├── Video Title.mp4
    └── Video Title_description.txt
```

## Customization

### Change Colors
Edit the `CustomButton` and `QualityButton` classes in `main.py` KV string.

### Add Features
The app uses the same `YouTubeDownloader` class from the desktop version, so all features are available.

## Troubleshooting

### "Module not found" errors
Make sure all dependencies are in `buildozer.spec` requirements.

### Build fails
- Check Java version (need JDK 17)
- Ensure all system dependencies installed
- Try `buildozer android clean` then rebuild

### App crashes on Android
- Check logcat: `adb logcat -s python`
- Ensure permissions in buildozer.spec

## License

Free and open source.