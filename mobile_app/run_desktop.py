#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run the mobile app on desktop for testing
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import and run the app
from main import YouTubeDownloaderApp

if __name__ == '__main__':
    # Set window size for mobile-like testing (must be before App instantiation)
    from kivy.core.window import Window
    Window.size = (360, 640)
    Window.minimum_width = 320
    Window.minimum_height = 568

    from main import YouTubeDownloaderApp
    YouTubeDownloaderApp().run()