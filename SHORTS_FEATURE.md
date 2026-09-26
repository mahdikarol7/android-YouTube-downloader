# YouTube Shorts vs Long Videos - Quality Feature

## What's New

The downloader now automatically detects YouTube Shorts and downloads them at **original quality**, while long videos are downloaded at **480p**.

## Detection Methods

### 1. URL Pattern Detection
- URLs containing `/shorts/` are detected as Shorts
- Example: `https://www.youtube.com/shorts/abc123`

### 2. Duration Detection
- Videos ≤ 60 seconds are treated as Shorts
- Works even if URL doesn't contain `/shorts/`

## Quality Settings

| Video Type | Quality | Description |
|------------|---------|-------------|
| **YouTube Shorts** | Original | Best available quality (1080p, 720p, etc.) |
| **Long Videos** | 480p | Fixed quality for smaller file size |

## Format Selection

### YouTube Shorts (Original Quality):
```
bestvideo[vcodec~="^(avc|hev)"]
+bestaudio[acodec~="^(mp4a|aac)"]
/bestvideo+bestaudio/best
```

### Long Videos (480p):
```
bestvideo[height<=480][vcodec~="^(avc|hev)"]
+bestaudio[acodec~="^(mp4a|aac)"]
/bestvideo[height<=480]+bestaudio
/best[height<=480]/best
```

## Example Output

### YouTube Short:
```
============================================================
Downloading video at original quality
============================================================

Title: Amazing Short Video
Channel: Creator Name
Duration: 0:30
Type: YouTube Short (downloading at original quality)
Available codecs: avc1, av01, vp9
Preferred codec: H.264 (avc) for better compatibility

Starting download...

[INFO] Shorts detected - downloading at original quality
[download] Destination: Video.f137.mp4
[download] 100% of 25.00MiB in 00:15

[SUCCESS] Download completed!
[QUALITY] Original (1080p)
```

### Long Video:
```
============================================================
Downloading video at 480p quality
============================================================

Title: Tutorial Video
Channel: Educator Channel
Duration: 15:30
Type: Long video (downloading at 480p)
Available codecs: avc1, av01, vp9
Preferred codec: H.264 (avc) for better compatibility

Starting download...

[INFO] Long video - downloading at 480p
[download] Destination: Video.f135.mp4
[download] 100% of 50.00MiB in 00:45

[SUCCESS] Download completed!
[QUALITY] 480p
```

## Test Results

### YouTube Short Test:
```
URL: https://www.youtube.com/shorts/dQw4w9WgXcQ
Is Short: True
Quality: Original (no limit)
Selected: 137+140
Codec: avc1.640028
Height: 1080p  ✓ ORIGINAL QUALITY
```

### Long Video Test:
```
URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Is Short: False
Quality: 480p
Selected: 135+140
Codec: avc1.4d401e
Height: 480p   ✓ LIMITED QUALITY
```

## Benefits

✅ **Shorts at Full Quality**: Enjoy Shorts in their original resolution
✅ **Long Videos Optimized**: Save space with 480p for longer content
✅ **Smart Detection**: Works with both URL patterns and duration
✅ **Automatic**: No manual configuration needed
✅ **Consistent Codec**: Both use H.264 for compatibility

## Use Cases

- **Shorts**: Perfect for watching on mobile, sharing, archiving
- **Long Videos**: Great for tutorials, lectures, save storage space
- **Mixed Playlists**: Handles both types automatically

## Files Modified

- `downloader.py`
  - Added `is_short()` method
  - Updated `download_video()` to detect Shorts
  - Modified format selection based on video type
  - Added video type display in info

## Technical Details

### Detection Logic:
```python
def is_short(self, url, info=None):
    # Method 1: URL pattern
    if '/shorts/' in url:
        return True

    # Method 2: Duration (≤60 seconds)
    if info and info.get('duration'):
        if info['duration'] <= 60:
            return True

    return False
```

### Quality Assignment:
- Shorts: No height limit, best available
- Long videos: `height <= 480`
