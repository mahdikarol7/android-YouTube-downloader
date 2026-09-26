#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Downloader - Mobile App (Kivy)
Simple and clean mobile interface for YouTube video downloading
"""

import os
import sys
import threading
from pathlib import Path

# Add parent directory to path to import downloader
sys.path.insert(0, str(Path(__file__).parent.parent))

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.core.window import Window

# Import our downloader
from downloader import YouTubeDownloader

# Set window size for desktop testing
Window.size = (360, 640)

KV = '''
<CustomButton@Button>:
    font_size: sp(16)
    size_hint_y: None
    height: dp(50)
    background_normal: ''
    background_color: 0.2, 0.6, 0.9, 1
    color: 1, 1, 1, 1
    bold: True

<CustomButtonSecondary@Button>:
    font_size: sp(14)
    size_hint_y: None
    height: dp(45)
    background_normal: ''
    background_color: 0.3, 0.7, 0.3, 1
    color: 1, 1, 1, 1

<CustomInput@TextInput>:
    font_size: sp(16)
    size_hint_y: None
    height: dp(50)
    multiline: False
    padding: [dp(10), dp(10)]
    background_normal: ''
    background_active: ''
    background_color: 1, 1, 1, 1
    foreground_color: 0, 0, 0, 1
    cursor_color: 0.2, 0.6, 0.9, 1
    hint_text_color: 0.5, 0.5, 0.5, 1

<QualityButton@Button>:
    font_size: sp(14)
    size_hint_y: None
    height: dp(45)
    background_normal: ''
    background_color: 0.95, 0.95, 0.95, 1
    color: 0.2, 0.2, 0.2, 1
    bold: True

<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)

        # Header
        BoxLayout:
            size_hint_y: None
            height: dp(80)
            orientation: 'vertical'

            Label:
                text: 'YouTube Downloader'
                font_size: sp(24)
                bold: True
                color: 0.2, 0.6, 0.9, 1
                size_hint_y: None
                height: dp(40)
                halign: 'center'
                text_size: self.size

            Label:
                text: 'Simple & Fast'
                font_size: sp(14)
                color: 0.5, 0.5, 0.5, 1
                size_hint_y: None
                height: dp(25)
                halign: 'center'
                text_size: self.size

        # URL Input
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(100)
            spacing: dp(5)

            Label:
                text: 'YouTube URL'
                font_size: sp(14)
                color: 0.3, 0.3, 0.3, 1
                size_hint_y: None
                height: dp(25)
                halign: 'left'
                text_size: self.size

            CustomInput:
                id: url_input
                hint_text: 'Paste YouTube link here...'
                on_text_validate: root.check_url()

        # Paste button
        CustomButtonSecondary:
            text: '📋 Paste from Clipboard'
            on_press: root.paste_from_clipboard()

        # Divider
        BoxLayout:
            size_hint_y: None
            height: dp(1)
            canvas:
                Color:
                    rgba: 0.8, 0.8, 0.8, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

        # Quality Selection
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(180)
            spacing: dp(8)

            Label:
                text: 'Select Quality'
                font_size: sp(14)
                color: 0.3, 0.3, 0.3, 1
                size_hint_y: None
                height: dp(25)
                halign: 'left'
                text_size: self.size

            GridLayout:
                cols: 2
                spacing: dp(8)
                size_hint_y: None
                height: dp(140)
                row_default_height: dp(45)
                row_force_default: True

                QualityButton:
                    id: q360
                    text: '360p - Small, Fast'
                    on_press: root.select_quality(360, self)

                QualityButton:
                    id: q480
                    text: '480p - Recommended'
                    on_press: root.select_quality(480, self)

                QualityButton:
                    id: q720
                    text: '720p - HD'
                    on_press: root.select_quality(720, self)

                QualityButton:
                    id: q1080
                    text: '1080p - Full HD'
                    on_press: root.select_quality(1080, self)

        # Download Button
        CustomButton:
            id: download_btn
            text: '📥 Start Download'
            on_press: root.start_download()
            disabled: True

        # Progress Area
        BoxLayout:
            id: progress_area
            orientation: 'vertical'
            size_hint_y: None
            height: 0
            opacity: 0
            spacing: dp(8)

            Label:
                id: status_label
                text: 'Ready'
                font_size: sp(13)
                color: 0.4, 0.4, 0.4, 1
                size_hint_y: None
                height: dp(20)
                halign: 'center'
                text_size: self.size

            ProgressBar:
                id: progress_bar
                max: 100
                value: 0
                size_hint_y: None
                height: dp(10)

            Label:
                id: progress_text
                text: '0%'
                font_size: sp(12)
                color: 0.5, 0.5, 0.5, 1
                size_hint_y: None
                height: dp(20)
                halign: 'center'
                text_size: self.size

        # Footer
        Label:
            text: 'Downloads saved to: /downloads folder'
            font_size: sp(11)
            color: 0.6, 0.6, 0.6, 1
            size_hint_y: None
            height: dp(20)
            halign: 'center'
            text_size: self.size

<ErrorPopup@Popup>:
    title: 'Error'
    size_hint: 0.85, 0.35
    auto_dismiss: True
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)
        Label:
            id: error_msg
            text: ''
            font_size: sp(15)
            color: 0.8, 0.2, 0.2, 1
            halign: 'center'
            valign: 'middle'
            text_size: self.size
        CustomButtonSecondary:
            text: 'OK'
            on_press: root.dismiss()

<SuccessPopup@Popup>:
    title: 'Success!'
    size_hint: 0.85, 0.35
    auto_dismiss: True
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)
        Label:
            id: success_msg
            text: ''
            font_size: sp(15)
            color: 0.2, 0.7, 0.3, 1
            halign: 'center'
            valign: 'middle'
            text_size: self.size
        CustomButton:
            text: 'OK'
            on_press: root.dismiss()

<InfoPopup@Popup>:
    title: 'Info'
    size_hint: 0.85, 0.4
    auto_dismiss: True
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)
        Label:
            id: info_msg
            text: ''
            font_size: sp(14)
            color: 0.3, 0.3, 0.3, 1
            halign: 'center'
            valign: 'middle'
            text_size: self.size
        CustomButton:
            text: 'OK'
            on_press: root.dismiss()
'''


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.downloader = YouTubeDownloader()
        self.selected_quality = 480
        self.download_thread = None
        self.selected_quality_btn = None

    def on_enter(self):
        """Called when screen is entered"""
        # Set default quality selection
        self.select_quality(480, self.ids.q480)

    def select_quality(self, quality, btn):
        """Handle quality selection"""
        self.selected_quality = quality
        # Update button colors
        for qid in ['q360', 'q480', 'q720', 'q1080']:
            b = self.ids[qid]
            if b == btn:
                b.background_color = (0.2, 0.6, 0.9, 1)
                b.color = (1, 1, 1, 1)
            else:
                b.background_color = (0.95, 0.95, 0.95, 1)
                b.color = (0.2, 0.2, 0.2, 1)

        # Enable download button
        self.ids.download_btn.disabled = False

    def check_url(self):
        """Validate URL"""
        url = self.ids.url_input.text.strip()
        if url and self.downloader.validate_youtube_url(url):
            self.ids.download_btn.disabled = False

    def paste_from_clipboard(self):
        """Paste URL from clipboard"""
        try:
            from kivy.core.clipboard import Clipboard
            text = Clipboard.paste()
            if text:
                self.ids.url_input.text = text
                self.check_url()
        except Exception as e:
            print(f"Clipboard error: {e}")

    def start_download(self):
        """Start the download process"""
        url = self.ids.url_input.text.strip()
        if not url:
            self.show_error("Please enter a YouTube URL")
            return

        if not self.downloader.validate_youtube_url(url):
            self.show_error("Invalid YouTube URL")
            return

        # Show progress area
        self.ids.progress_area.height = dp(80)
        self.ids.progress_area.opacity = 1
        self.ids.progress_bar.value = 0
        self.ids.progress_text.text = '0%'
        self.ids.status_label.text = 'Starting...'
        self.ids.download_btn.disabled = True

        # Start download in background thread
        self.download_thread = threading.Thread(
            target=self._download_worker,
            args=(url, self.selected_quality),
            daemon=True
        )
        self.download_thread.start()

        # Start progress updater
        Clock.schedule_interval(self.update_progress, 0.5)

    def _download_worker(self, url, quality):
        """Worker thread for downloading"""
        try:
            # Monkey patch the progress display
            original_display = self.downloader.display_progress

            def mobile_display(progress_info, start_time):
                if progress_info and 'percent' in progress_info:
                    percent = progress_info['percent']
                    # Schedule UI update on main thread
                    Clock.schedule_once(
                        lambda dt: self._update_progress_ui(percent, progress_info.get('size', 'N/A')),
                        0
                    )

            self.downloader.display_progress = mobile_display

            success, result = self.downloader.download_video(url, quality)

            # Restore original
            self.downloader.display_progress = original_display

            # Call completion on main thread
            Clock.schedule_once(lambda dt: self._download_complete(success, result), 0)

        except Exception as e:
            Clock.schedule_once(lambda dt: self._download_error(str(e)), 0)

    def _update_progress_ui(self, percent, size):
        """Update progress UI from main thread"""
        self.ids.progress_bar.value = percent
        self.ids.progress_text.text = f'{percent:.1f}%'
        self.ids.status_label.text = f'Downloading... {size}'

    def update_progress(self, dt):
        """Periodic progress check"""
        pass  # Handled by callback

    def _download_complete(self, success, result):
        """Handle download completion"""
        Clock.unschedule(self.update_progress)

        if success:
            self.ids.progress_bar.value = 100
            self.ids.progress_text.text = '100%'
            self.ids.status_label.text = 'Complete!'
            self.show_success(f"Video saved!\nDescription saved too!")
        else:
            self.ids.status_label.text = 'Failed'
            self.show_error(result)

        self.ids.download_btn.disabled = False

    def _download_error(self, error_msg):
        """Handle download error"""
        Clock.unschedule(self.update_progress)
        self.ids.status_label.text = 'Error'
        self.ids.download_btn.disabled = False
        self.show_error(error_msg)

    def _update_progress_ui(self, percent, size):
        """Update progress UI from main thread"""
        self.ids.progress_bar.value = percent
        self.ids.progress_text.text = f'{percent:.1f}%'
        self.ids.status_label.text = f'Downloading... {size}'

    def show_error(self, message):
        """Show error popup"""
        popup = Builder.load_string('''
ErrorPopup:
    id: error_msg
''')
        popup.ids.error_msg.text = message
        popup.open()

    def show_success(self, message):
        """Show success popup"""
        popup = Builder.load_string('''
SuccessPopup:
    id: success_msg
''')
        popup.ids.success_msg.text = message
        popup.open()

    def show_info(self, message):
        """Show info popup"""
        popup = Builder.load_string('''
InfoPopup:
    id: info_msg
''')
        popup.ids.info_msg.text = message
        popup.open()


class YouTubeDownloaderApp(App):
    def build(self):
        self.title = 'YouTube Downloader'
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    YouTubeDownloaderApp().run()