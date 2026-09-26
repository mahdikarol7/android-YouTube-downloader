# Download Size & Status Fix

## Problem Fixed

**Issue 1: Wrong file size estimate**
- Before: Showed only video size (51.1MB for 360p)
- After: Shows total size including audio (75.4MB for 360p)

**Issue 2: Confusing download status**
- Before: Just showed file names (f134.mp4, f140.m4a)
- After: Shows "Downloading: VIDEO" then "Downloading: AUDIO"

## Why Videos Download Twice

YouTube stores video and audio as **separate files**:
- Video track (f134.mp4, f135.mp4, etc.)
- Audio track (f140.m4a, f141.m4a)

**yt-dlp downloads both, then merges them into one MP4 file.**

This is normal and ensures best quality.

## Size Calculation Fixed

### Before (Wrong):
```python
# Only counted video size
video_size = 51.1MB
displayed_size = video_size  # 51.1MB - WRONG!
```

### After (Correct):
```python
# Counts video + audio combined
video_size = 51.1MB
audio_size = 24.3MB
total_size = video_size + audio_size  # 75.4MB - CORRECT!
```

## Example: 360p Download

### Size Breakdown:
```
Video track: 51.1MB
Audio track: 24.3MB
─────────────────
Total:       75.4MB
```

### Quality Menu (Now Correct):
```
1. 360p  - ~75.4MB   (was ~51.1MB - now includes audio)
2. 480p  - ~116.9MB  (was ~92.6MB)
3. 720p  - ~201.1MB  (was ~176.9MB)
4. 1080p - ~364.4MB  (was ~340.1MB)
```

## Download Status Display

### Before (Confusing):
```
[download] Destination: video.f134.mp4
[download] Destination: audio.f140.m4a
[######..............]  35.2% | Size: 18.0MB
```
*Which file is downloading? Video or audio?*

### After (Clear):
```
Downloading: VIDEO
[#################.........]  55.3% | Size: 28.3MB

Downloading: AUDIO
[################..........]  52.1% | Size: 12.7MB

Merging video and audio...

[SUCCESS] Download completed!
```

## Technical Details

### File Detection:
```python
# Video formats: f134, f135, f136, f137, etc.
if '.f134' in line or '.f135' in line:
    print("Downloading: VIDEO")

# Audio formats: f140, f141, f251, etc.
elif '.f140' in line or '.f141' in line:
    print("Downloading: AUDIO")

# Merger
elif '[Merger]' in line:
    print("Merging video and audio...")
```

### Size Calculation:
```python
# Find best audio format
for f in formats:
    if acodec != 'none' and vcodec == 'none':
        best_audio_size = f['filesize']

# Calculate total for each quality
total_size = video_size + best_audio_size
```

## Benefits

✅ **Accurate estimates**: Shows true download size
✅ **Clear status**: Know exactly what's downloading
✅ **No confusion**: Video/Audio/Merge stages clear
✅ **Better planning**: Know how much data you'll use

## Files Modified

- `downloader.py`
  - Fixed `get_quality_sizes()` to include audio
  - Added video/audio download detection
  - Added merger status message
  - Added note about separate downloads
