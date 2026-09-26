# Video Codec Fix - H.264 Preference

## Problem

Previously, the downloader was downloading videos with AV1 codec (f251.webm), which:
- Has slower decoding
- Lower compatibility with older devices/players
- Requires more CPU resources to play

## Solution

Updated format selection to **prefer H.264 (avc) codec** for better compatibility.

### Before (Problematic):
```
[download] Destination: video.f251.webm  <-- AV1 codec
```

### After (Fixed):
```
[download] Destination: video.f135.mp4   <-- H.264 codec
```

## Format Selection Logic

The downloader now uses this priority:

1. **H.264/HEVC video** + **AAC audio** (Best compatibility)
2. **Any video** + **Any audio** (Fallback)
3. **Best quality ≤ 480p** (Final fallback)
4. **Best available** (Last resort)

### Format String:
```
bestvideo[height<=480][vcodec~="^(avc|hev)"]
+bestaudio[acodec~="^(mp4a|aac)"]
/bestvideo[height<=480]+bestaudio
/best[height<=480]
/best
```

## Codec Comparison

| Codec | Extension | Compatibility | File Size | CPU Usage |
|-------|-----------|---------------|-----------|-----------|
| H.264 (avc) | .mp4 | ★★★★★ Excellent | Larger | Low |
| H.265 (hev) | .mp4 | ★★★★☆ Good | Medium | Medium |
| VP9 | .webm | ★★★☆☆ Fair | Small | Medium |
| AV1 | .mp4/.webm | ★★☆☆☆ Limited | Smallest | High |

**Recommendation**: H.264 for maximum compatibility

## Example Output

### Format Detection:
```
Available video formats at 480p or lower:

   135 | 480p | avc1       | mp4  |   13.5MB <-- PREFERRED
   244 | 480p | vp9        | webm |    8.9MB
   397 | 480p | av01       | mp4  |    9.4MB

Format selection will prefer H.264 (avc) codec for better compatibility
```

### Download:
```
[download] Destination: Video_Title.f135.mp4
[download] 100% of 13.50MiB in 00:30

[Merger] Merging formats into "Video_Title.mp4"
(No need to convert - already H.264!)
```

## Benefits

✅ **Better Compatibility**: Works on all devices and players
✅ **Faster Playback**: Lower CPU usage
✅ **No Conversion Needed**: Already in MP4/H.264 format
✅ **Smaller Merging**: Faster merge process
✅ **Universal Support**: Works with TV, mobile, web browsers

## Files Modified

- `downloader.py` - Updated format selection logic
  - Added codec preference (H.264/HEVC)
  - Added audio codec preference (AAC)
  - Added codec info display
  - Improved format fallback chain

## Testing

Verified with YouTube video showing:
- Format 135: 480p H.264 (avc1) - 13.5MB ✅ PREFERRED
- Format 244: 480p VP9 - 8.9MB
- Format 397: 480p AV1 - 9.4MB

The downloader now correctly selects H.264 format for downloads.
