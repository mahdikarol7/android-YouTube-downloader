# File Size Display Feature

## What's New

Now shows estimated file size for each quality option before downloading, helping you choose the right quality and save internet data!

## Before (No File Sizes):
```
Select Video Quality:
  1. 360p  (Small file, faster download)
  2. 480p  (Recommended)
  3. 720p  (HD quality)
  4. 1080p (Full HD)
```

## After (With File Sizes):
```
Select Video Quality:
  1. 360p  - ~5.4MB   (Small file, faster download)
  2. 480p  - ~9.4MB   (Recommended)
  3. 720p  - ~16.8MB  (HD quality)
  4. 1080p - ~29.0MB  (Full HD)
```

## Example Session

```
============================================================
  YouTube Downloader
============================================================

Enter YouTube link (or type 'exit' to quit):
> https://www.youtube.com/watch?v=abc123

[OK] URL is valid

Fetching video info...

  Title: Amazing Video Tutorial
  Channel: Creator Name
  Duration: 15:30

============================================================
  Select Video Quality:
============================================================
  1. 360p  - ~15.2MB  (Small file, faster download)
  2. 480p  - ~25.8MB  (Recommended)
  3. 720p  - ~52.3MB  (HD quality)
  4. 1080p - ~98.5MB  (Full HD)
============================================================
  Default: 2 (480p)
============================================================

  Enter choice (1-4) or press Enter for default: 1

  Selected: 360p (~15.2MB)

  Starting download...
  [##########..............]  35.2% | Size: 5.35MB

  [SUCCESS] Download completed!
```

## Benefits

✅ **Data Saving**: Know exact file size before downloading
✅ **Informed Choice**: Compare quality vs file size
✅ **Storage Planning**: Know how much space you need
✅ **Bandwidth Friendly**: Perfect for limited data plans
✅ **Quick Decisions**: See all options at a glance

## File Size Examples

| Quality | Typical Size | Best For |
|---------|--------------|----------|
| 360p | 5-20 MB | Mobile, slow internet |
| 480p | 10-40 MB | Balanced choice |
| 720p | 20-80 MB | HD viewing |
| 1080p | 40-150 MB | Full HD, big screens |

**Note**: Actual sizes vary based on video duration and content complexity

## How It Works

### Size Detection:
1. Fetches all available video formats
2. Finds best format for each quality level
3. Extracts file size information
4. Formats to human-readable (MB/GB)

### Smart Matching:
- Finds closest match to target quality
- Accounts for ±50 pixel tolerance
- Prioritizes H.264 codec formats

### Size Calculation:
```python
def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
```

## YouTube Shorts

- **No quality selection** needed
- **No file size display** (auto original quality)
- Shows video info only

## Files Modified

- `downloader.py`
  - Added `format_size()` method
  - Added `get_quality_sizes()` method
  - Updated quality selection to display sizes
  - Removed duplicate video info fetch

## Test Results

```
Testing file size detection:

  360p: ~5.4MB
  480p: ~9.4MB
  720p: ~16.8MB
  1080p: ~29.0MB

[OK] File size detection working!
```

## Tips

1. **Check sizes first**: Compare before choosing
2. **360p saves data**: Great for mobile/on-the-go
3. **480p balanced**: Good quality with reasonable size
4. **720p+ for WiFi**: Use HD when on fast connection
5. **1080p for large screens**: Best for TV/monitor viewing
