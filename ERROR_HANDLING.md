# Error Handling Improvements

## What's New

Added automatic retries, 403 error handling, and yt-dlp update option to fix download failures.

## Problem Solved

Previously, if YouTube blocked a download (HTTP 403 Forbidden), the download would just fail with no recovery option.

## New Error Handling Features

### 1. Automatic Retries with Fallbacks

**Before:**
- Single format attempt
- Fails immediately on error

**After:**
- Tries multiple format specifications
- Automatic fallback to alternative formats
- Shows retry progress

```
Format 1: bestvideo[height<=360][vcodec~="^(avc|hev)"]+bestaudio...
  → If fails, tries Format 2

Format 2: bestvideo[height<=360]+bestaudio/best[height<=360]/best
  → If fails, tries Format 3

Format 3: best[height<=360]/best
  → If all fail, asks to update yt-dlp
```

### 2. HTTP 403 Error Detection

**Detects these errors:**
- HTTP Error 403: Forbidden
- Unable to download video data
- YouTube blocking

**Automatic response:**
```
[WARNING] Format blocked by YouTube, trying next format...
[WARNING] HTTP error, trying next format...
```

### 3. yt-dlp Update Option

**When all formats fail:**
```
[ERROR] All download attempts failed
This might be due to YouTube blocking or outdated yt-dlp

Do you want to update yt-dlp? (y/n): y

  Updating yt-dlp...
  [OK] yt-dlp updated to version 2024.01.15

  Please try downloading again with the updated version
```

### 4. Better Error Messages

**Before (cluttered):**
```
[youtube] Extracting URL...
[youtube] Downloading webpage...
[youtube] Downloading android vr player API JSON...
[info] Downloading 1 format(s): 134+140
ERROR: unable to download video data: HTTP Error 403: Forbidden
```

**After (filtered):**
```
[WARNING] Format blocked by YouTube, trying next format...
```

## Example Flow

### Scenario: First format blocked by YouTube

```
  Starting download...

  Retrying with alternative format...

  [##########..............]  35.2% | Size: 18.20MB

  [SUCCESS] Download completed!
```

### Scenario: All formats fail

```
  Starting download...

  [WARNING] Format blocked by YouTube, trying next format...
  [WARNING] HTTP error, trying next format...

  [ERROR] All download attempts failed
  This might be due to YouTube blocking or outdated yt-dlp

  Do you want to update yt-dlp? (y/n): y

  Updating yt-dlp...
  [OK] yt-dlp updated to version 2024.01.15

  Please try downloading again with the updated version
```

## Fallback Format Chain

### For Long Videos (e.g., 360p):
```
1. bestvideo[height<=360][vcodec~="^(avc|hev)"]+bestaudio[acodec~="^(mp4a|aac)"]
2. bestvideo[height<=360]+bestaudio/best[height<=360]/best
3. best[height<=360]/best
```

### For YouTube Shorts:
```
1. bestvideo[vcodec~="^(avc|hev)"]+bestaudio[acodec~="^(mp4a|aac)"]/bestvideo+bestaudio/best
2. bestvideo+bestaudio/best
3. best
```

## New Command Added

### update_yt_dlp():
```python
def update_yt_dlp(self):
    """Update yt-dlp to latest version"""
    result = subprocess.run(
        ['pip', 'install', '--upgrade', 'yt-dlp'],
        ...
    )
```

**Called when:**
- User chooses to update after failure
- Manual update option

## Benefits

✅ **Automatic Recovery**: Retries with different formats  
✅ **403 Error Handling**: Detects and bypasses YouTube blocks  
✅ **Easy Updates**: One-click yt-dlp update  
✅ **Clear Messages**: Filtered, user-friendly output  
✅ **Better UX**: Less confusing error messages  

## Files Modified

- `downloader.py`
  - Added `update_yt_dlp()` method
  - Added retry logic with 3 format fallbacks
  - Added 403 error detection
  - Added update prompt on failure
  - Filtered verbose output
  - Added `--no-check-certificate` flag

## Common Causes of 403 Errors

1. **Outdated yt-dlp**: YouTube changes their API
2. **Rate limiting**: Too many downloads
3. **Regional blocks**: Some videos restricted
4. **Age-restricted**: Requires authentication
5. **Private videos**: Access denied

## Solutions

**Automatic (in downloader):**
- Retry with different formats
- Update yt-dlp

**Manual:**
```bash
pip install --upgrade yt-dlp
```

**Advanced:**
- Add cookies from browser
- Use proxy/VPN
- Wait and try later
