#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Downloader - 480p Edition
"""

import sys
import os
import re
import subprocess
import json
from datetime import datetime
from pathlib import Path
import unicodedata
import io
import time

# Fix encoding issues on Windows (only for console mode)
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, TypeError):
        pass

class YouTubeDownloader:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.downloads_dir = self.base_dir / "downloads"
        self.downloads_dir.mkdir(exist_ok=True)

    def sanitize_filename(self, filename):
        """پاکسازی نام فایل از کاراکترهای غیرمجاز"""
        filename = unicodedata.normalize('NFKD', filename)
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = re.sub(r'\s+', ' ', filename).strip()
        filename = filename[:200]
        return filename

    def check_yt_dlp_installed(self):
        """Check if yt-dlp is installed"""
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'yt_dlp', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return True, result.stdout.strip()
            return False, None
        except Exception:
            return False, None

    def update_yt_dlp(self):
        """Update yt-dlp to latest version"""
        print("\n  Updating yt-dlp...")
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode == 0:
                _, new_version = self.check_yt_dlp_installed()
                print(f"  [OK] yt-dlp updated to version {new_version}")
                return True
            else:
                print(f"  [ERROR] Failed to update yt-dlp")
                print(f"  stderr: {result.stderr[:200]}")
                return False
        except Exception as e:
            print(f"  [ERROR] Update failed: {str(e)}")
            return False

    def check_ffmpeg_installed(self):
        """بررسی نصب بودن ffmpeg"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
        except Exception:
            return False

    def validate_youtube_url(self, url):
        """Validate YouTube URL"""
        patterns = [
            r'(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(https?://)?(www\.)?youtube\.com/shorts/[\w-]+',
            r'(https?://)?youtu\.be/[\w-]+',
            r'(https?://)?(www\.)?youtube\.com/embed/[\w-]+',
        ]
        for pattern in patterns:
            if re.match(pattern, url.strip()):
                return True
        return False

    def is_short(self, url, info=None):
        """Check if video is a YouTube Short"""
        # Check URL pattern
        if '/shorts/' in url:
            return True

        # Check duration (Shorts are typically <= 60 seconds)
        if info and info.get('duration'):
            if info['duration'] <= 60:
                return True

        return False

    def format_size(self, size_bytes):
        """Format file size in human readable format"""
        if not size_bytes or size_bytes == 0:
            return "N/A"

        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}TB"

    def get_quality_sizes(self, formats):
        """Get estimated file sizes for different quality levels (video + audio combined)"""
        quality_sizes = {}

        # Target qualities
        target_qualities = [360, 480, 720, 1080]

        # Find best audio format (usually m4a with AAC)
        best_audio_size = 0
        for f in formats:
            acodec = f.get('acodec', 'none')
            vcodec = f.get('vcodec', 'none')
            filesize = f.get('filesize', 0)
            # Find audio-only format (has audio codec but no video codec)
            if filesize and acodec != 'none' and vcodec == 'none':
                if filesize > best_audio_size:
                    best_audio_size = filesize

        for target in target_qualities:
            best_video_format = None
            best_score = -1

            for f in formats:
                height = f.get('height', 0)
                vcodec = f.get('vcodec', 'none')
                filesize = f.get('filesize', 0)

                # Skip formats without size or video codec
                if not filesize or vcodec == 'none':
                    continue

                # Find best video format at or near target quality
                if height and abs(height - target) < 50:
                    # Score: prefer H.264 (avc1), then HEVC (hev1/hvc1), then others
                    # Higher score = better
                    score = 0
                    if height == target:
                        score += 100  # Exact height match
                    elif abs(height - target) <= 20:
                        score += 50   # Close height match

                    # Codec preference
                    if 'avc1' in vcodec.lower() or 'avc3' in vcodec.lower():
                        score += 1000  # H.264 preferred
                    elif 'hev1' in vcodec.lower() or 'hvc1' in vcodec.lower():
                        score += 500   # HEVC next
                    else:
                        score += 100   # Other codecs (VP9, AV1)

                    if score > best_score:
                        best_score = score
                        best_video_format = f

            # Calculate total size (video + audio)
            if best_video_format and best_video_format.get('filesize'):
                video_size = best_video_format['filesize']
                total_size = video_size + best_audio_size
                quality_sizes[target] = self.format_size(total_size)
            else:
                quality_sizes[target] = "N/A"

        return quality_sizes

    def get_video_info(self, url):
        """Get video info"""
        try:
            cmd = [
                sys.executable, '-m', 'yt_dlp',
                '--no-download',
                '--print-json',
                '--no-warnings',
                url
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode != 0:
                error_msg = result.stderr.strip()
                if 'Video unavailable' in error_msg:
                    return None, "Video is unavailable or has been removed"
                elif 'Private video' in error_msg:
                    return None, "This is a private video"
                elif 'Sign in' in error_msg:
                    return None, "Sign in required"
                else:
                    return None, f"Error fetching info: {error_msg}"

            info = json.loads(result.stdout)
            return info, None
        except json.JSONDecodeError:
            return None, "Error parsing video info"
        except subprocess.TimeoutExpired:
            return None, "Timeout fetching video info"
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"

    def parse_progress(self, line):
        """Parse yt-dlp output for progress information"""
        progress_info = {}

        # Match download progress pattern: [download] 45.2% of 123.45MiB at 2.50MiB/s ETA 00:45
        progress_match = re.search(
            r'\[download\]\s+([\d.]+)%\s+of\s+~?([\d.]+\w+)\s+at\s+([\d.]+\w+/s)\s+ETA\s+(\S+)',
            line
        )
        if progress_match:
            progress_info['percent'] = float(progress_match.group(1))
            progress_info['size'] = progress_match.group(2)
            progress_info['speed'] = progress_match.group(3)
            progress_info['eta'] = progress_match.group(4)
            return progress_info

        # Match alternative pattern: [download] 45.2% of 123.45MiB ETA 00:45
        alt_match = re.search(
            r'\[download\]\s+([\d.]+)%\s+of\s+~?([\d.]+\w+)\s+ETA\s+(\S+)',
            line
        )
        if alt_match:
            progress_info['percent'] = float(alt_match.group(1))
            progress_info['size'] = alt_match.group(2)
            progress_info['eta'] = alt_match.group(3)
            return progress_info

        # Match simple percentage: [download] 45.2%
        simple_match = re.search(r'\[download\]\s+([\d.]+)%', line)
        if simple_match:
            progress_info['percent'] = float(simple_match.group(1))
            return progress_info

        return None

    def display_progress(self, progress_info, start_time):
        """Display formatted progress bar"""
        if not progress_info or 'percent' not in progress_info:
            return

        percent = progress_info['percent']
        bar_length = 30
        filled_length = int(bar_length * percent / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)

        # Get size
        size = progress_info.get('size', 'N/A')

        # Clear line and print progress
        sys.stdout.write('\r' + ' ' * 80 + '\r')
        sys.stdout.write(
            f"\r  [{bar}] {percent:5.1f}% | Size: {size}"
        )
        sys.stdout.flush()

    def download_video(self, url, quality=None):
        """Download video with specified quality (None = ask user)"""

        # Check yt-dlp
        yt_dlp_installed, version = self.check_yt_dlp_installed()
        if not yt_dlp_installed:
            print("[ERROR] yt-dlp is not installed!")
            print("\nTo install yt-dlp, run:")
            print("pip install yt-dlp")
            return False, "yt-dlp not installed"

        print(f"[OK] yt-dlp installed (version: {version})")

        # Check ffmpeg
        ffmpeg_installed = self.check_ffmpeg_installed()
        if not ffmpeg_installed:
            print("[WARNING] ffmpeg is not installed!")
            print("Some videos may download without audio")
            print("Install ffmpeg from https://ffmpeg.org")
        else:
            print("[OK] ffmpeg is installed")

        # Validate URL
        if not self.validate_youtube_url(url):
            print("[ERROR] Invalid YouTube URL!")
            return False, "Invalid URL"

        print(f"[OK] URL is valid")

        # Get video info first (needed for Shorts detection and file sizes)
        print("\nFetching video info...")
        info, error = self.get_video_info(url)
        if error:
            print(f"[ERROR] {error}")
            return False, error

        title = info.get('title', 'Unknown')
        duration = info.get('duration', 0)
        uploader = info.get('uploader', 'Unknown')

        # Check if Short (no quality selection needed for Shorts)
        is_video_short = self.is_short(url, info)

        if is_video_short:
            quality = 'best'
            print(f"[INFO] YouTube Short detected - original quality")
            print(f"\n  Title: {title}")
            print(f"  Channel: {uploader}")
            print(f"  Duration: {duration // 60}:{duration % 60:02d}")
        elif quality is None:
            # Get file sizes for different qualities
            print(f"\n  Title: {title}")
            print(f"  Channel: {uploader}")
            print(f"  Duration: {duration // 60}:{duration % 60:02d}")

            # Calculate estimated file sizes
            formats = info.get('formats', [])
            quality_sizes = self.get_quality_sizes(formats)

            # Quality selection for long videos
            print(f"\n{'='*60}")
            print(f"  Select Video Quality:")
            print(f"{'='*60}")

            # Show quality options with file sizes
            options = [
                ('1', 360, 'Small file, faster download'),
                ('2', 480, 'Recommended'),
                ('3', 720, 'HD quality'),
                ('4', 1080, 'Full HD')
            ]

            for key, qual, desc in options:
                size_str = quality_sizes.get(qual, "N/A")
                if size_str != "N/A":
                    print(f"  {key}. {qual}p  - ~{size_str}  ({desc})")
                else:
                    print(f"  {key}. {qual}p  - (Not available)")

            print(f"{'='*60}")
            print(f"  Default: 2 (480p)")
            print(f"{'='*60}\n")

            choice = input("  Enter choice (1-4) or press Enter for default: ").strip()

            quality_map = {
                '1': 360,
                '2': 480,
                '3': 720,
                '4': 1080,
                '': 480  # default
            }

            quality = quality_map.get(choice, 480)

            selected_size = quality_sizes.get(quality, "N/A")
            if choice in quality_map:
                print(f"\n  Selected: {quality}p (~{selected_size})\n")
            else:
                print(f"\n  Using default: 480p (~{selected_size})\n")
        else:
            # Quality was provided, just show info
            print(f"\n  Title: {title}")
            print(f"  Channel: {uploader}")
            print(f"  Duration: {duration // 60}:{duration % 60:02d}")
            print(f"  Quality: {quality}p\n")

        # Create download folder
        safe_title = self.sanitize_filename(title)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{safe_title}_{timestamp}"
        download_path = self.downloads_dir / folder_name
        download_path.mkdir(exist_ok=True)

        print(f"\n  Download folder: {download_path}")
        print(f"  Note: Video and audio download separately, then merge")

        # Download video
        print(f"\n  Starting download...")
        print(f"  {'='*50}\n")
        output_template = str(download_path / f"{safe_title}.%(ext)s")

        # Format selection based on video type with fallbacks
        if is_video_short:
            # YouTube Shorts: download at original quality
            format_specs = [
                'bestvideo[vcodec~="^(avc|hev)"]+bestaudio[acodec~="^(mp4a|aac)"]/bestvideo+bestaudio/best',
                'bestvideo+bestaudio/best',
                'best'
            ]
        else:
            # Long videos: download at specified quality with fallbacks
            format_specs = [
                f'bestvideo[height<={quality}][vcodec~="^(avc|hev)"]+bestaudio[acodec~="^(mp4a|aac)"]/bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best',
                f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best',
                f'best[height<={quality}]/best'
            ]

        # Try each format specification until one works
        for attempt, format_spec in enumerate(format_specs):
            if attempt > 0:
                print(f"\n  Retrying with alternative format...")
                time.sleep(2)

            cmd = [
                sys.executable, '-m', 'yt_dlp',
                '-f', format_spec,
                '--merge-output-format', 'mp4',
                '-o', output_template,
                '--no-warnings',
                '--newline',
                '--no-check-certificate',  # Bypass some certificate issues
                '--extractor-args', 'youtube:player_client=android,tv,web_safari',  # Bypass JS runtime requirement
                url
            ]

            try:
                start_time = time.time()
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='utf-8',
                    errors='replace'
                )

                last_percent = -1
                error_output = []
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        line = output.strip()
                        error_output.append(line)

                        # Detect which file is downloading
                        if '[download] Destination:' in line:
                            if '.f134' in line or '.f135' in line or '.f136' in line or '.f137' in line:
                                sys.stdout.write('\r' + ' ' * 80 + '\r')
                                print("  Downloading: VIDEO")
                            elif '.f140' in line or '.f141' in line or '.f251' in line:
                                sys.stdout.write('\r' + ' ' * 80 + '\r')
                                print("  Downloading: AUDIO")
                        elif '[Merger]' in line:
                            sys.stdout.write('\r' + ' ' * 80 + '\r')
                            print("  Merging video and audio...")

                        # Try to parse progress
                        progress_info = self.parse_progress(line)

                        if progress_info and 'percent' in progress_info:
                            current_percent = int(progress_info['percent'])
                            # Update progress bar only when percent changes
                            if current_percent != last_percent:
                                self.display_progress(progress_info, start_time)
                                last_percent = current_percent
                        else:
                            # Print non-progress lines (status messages, errors, etc.)
                            if line and not line.startswith('\r'):
                                sys.stdout.write('\r' + ' ' * 80 + '\r')
                                # Filter out verbose lines
                                if not any(skip in line for skip in ['[youtube]', '[info]', 'Deleting original']):
                                    print(f"  {line}")

                print()  # New line after progress bar
                returncode = process.poll()

                if returncode == 0:
                    # Save description to txt file
                    description_file = download_path / f"{safe_title}_description.txt"
                    try:
                        with open(description_file, 'w', encoding='utf-8') as f:
                            f.write(f"Title: {title}\n")
                            f.write(f"Channel: {uploader}\n")
                            f.write(f"Duration: {duration // 60}:{duration % 60:02d}\n")
                            f.write(f"URL: {url}\n")
                            f.write(f"Download time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write(f"Quality: {quality}p\n")
                            f.write(f"\nDescription:\n{info.get('description', 'No description available')}\n")
                    except Exception as e:
                        print(f"  [WARNING] Could not save description file: {e}")

                    print(f"\n\n  {'='*50}")
                    print(f"  [SUCCESS] Download completed!")
                    print(f"  Saved to: {download_path}")
                    print(f"  Description saved to: {description_file.name}")
                    print(f"  {'='*50}\n")
                    return True, str(download_path)
                else:
                    # Check if it's a 403 error, connection error, timeout, or similar
                    error_text = '\n'.join(error_output)
                    is_retryable = False
                    if '403' in error_text or 'Forbidden' in error_text:
                        print(f"  [WARNING] Format blocked by YouTube, trying next format...")
                        is_retryable = True
                    elif 'HTTP Error' in error_text:
                        print(f"  [WARNING] HTTP error, trying next format...")
                        is_retryable = True
                    elif 'SSL' in error_text or 'UNEXPECTED_EOF_WHILE_READING' in error_text or 'Read timed out' in error_text or 'Connection' in error_text:
                        print(f"  [WARNING] Connection/SSL error, trying next format...")
                        is_retryable = True
                    elif 'timeout' in error_text.lower():
                        print(f"  [WARNING] Timeout error, trying next format...")
                        is_retryable = True

                    if is_retryable and attempt < len(format_specs) - 1:
                        continue
                    else:
                        print(f"\n  [ERROR] Download failed")
                        return False, f"Download failed (code: {returncode})"

            except subprocess.TimeoutExpired:
                process.kill()
                print(f"  [WARNING] Timeout, trying next format...")
                continue
            except KeyboardInterrupt:
                process.kill()
                print("\n\n[INFO] Download cancelled by user")
                return False, "Download cancelled"
            except Exception as e:
                print(f"  [WARNING] Error: {str(e)}, trying next format...")
                continue

        # All formats failed
        print(f"\n  [ERROR] All download attempts failed")
        print(f"  This might be due to YouTube blocking or outdated yt-dlp")
        print()
        update_choice = input("  Do you want to update yt-dlp? (y/n): ").strip().lower()

        if update_choice in ['y', 'yes', '']:
            if self.update_yt_dlp():
                print("\n  Please try downloading again with the updated version")
            return False, "Update attempted, please retry"

        print(f"\n  Manual solutions:")
        print(f"  1. Run: pip install --upgrade yt-dlp")
        print(f"  2. Check internet connection")
        print(f"  3. Try again later")
        return False, "All download attempts failed"

def main():
    """Main function"""
    downloader = YouTubeDownloader()

    print("\n" + "="*60)
    print("  YouTube Downloader")
    print("="*60 + "\n")

    # Get URL from user
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(f"Input URL: {url}")
    else:
        url = input("\nEnter YouTube URL: ").strip()

    if not url:
        print("[ERROR] No URL provided!")
        sys.exit(1)

    # Download video
    success, result = downloader.download_video(url)

    if success:
        print(f"\nVideo saved to:\n{result}")
        sys.exit(0)
    else:
        print(f"\n[FAILED] Download unsuccessful: {result}")
        sys.exit(1)

if __name__ == "__main__":
    main()
