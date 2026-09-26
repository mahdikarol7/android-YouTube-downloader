# YouTube Downloader - 480p Edition

A simple and practical downloader for YouTube videos at 480p quality

## Features

- ✅ Download videos at 480p quality
- ✅ Real-time progress display with percentage, speed, and ETA
- ✅ Visual progress bar during download
- ✅ Saves to organized folders automatically
- ✅ Complete error handling system
- ✅ Supports all YouTube URL formats
- ✅ Shows video info before downloading
- ✅ Simple and user-friendly interface

## Prerequisites

1. **Python 3.7+**
   - Download from: https://www.python.org
   - Make sure to check "Add Python to PATH" during installation

2. **yt-dlp**
   - Auto-installed when running the downloader
   - Or install manually: `pip install yt-dlp`

3. **ffmpeg** (optional but recommended)
   - For merging audio and video
   - Download from: https://ffmpeg.org

## How to Use

### Method 1: Run Batch File (Recommended)

1. Double-click `download.bat`
2. Enter YouTube URL when prompted
3. Watch the progress bar update in real-time

### Method 2: Command Line

```bash
python downloader.py "YouTube_URL"
```

### Method 3: Drag and Drop

Drag a YouTube URL onto `download.bat`

## Progress Display

During download, you'll see a real-time progress bar:

```
  [████████████████░░░░░░░░░░░░░░░░░░░░░░░░]  45.2% | Size: 123.45MiB | Speed: 2.50MiB/s | ETA: 00:45 | Elapsed: 01:23
```

- **Percentage**: How much has been downloaded (0-100%)
- **Size**: Total file size
- **Speed**: Current download speed
- **ETA**: Estimated time remaining
- **Elapsed**: Time since download started
- **Progress Bar**: Visual indicator [████░░░░]

## Folder Structure

```
youtube downloader/
├── downloader.py          # Main Python script
├── download.bat           # Windows batch file
├── README.md              # This guide
├── test_setup.bat         # System test file
├── quick_test.bat         # Quick test file
└── downloads/             # Download folder (auto-created)
    └── Video_Title_Date/
        └── Video_Title.mp4
```

## Error Handling

The downloader includes comprehensive error handling for:

- ❌ Invalid URLs
- ❌ Videos that are deleted or private
- ❌ Network connection issues
- ❌ Missing yt-dlp or ffmpeg
- ❌ Download failures
- ⚠️  Quality-related warnings

## Tips

- Videos are saved in the `downloads` folder
- Each download gets its own folder
- Filenames are automatically sanitized
- Press `Ctrl+C` to cancel a download

## Troubleshooting

### If Python doesn't work:
- Make sure Python is installed
- Verify Python is in your system PATH
- Try running `python --version`

### If yt-dlp doesn't work:
- Run `pip install --upgrade yt-dlp`
- Reinstall Python

### If video has no audio:
- Install ffmpeg
- Download from https://ffmpeg.org

## License

This software is free and open source.
