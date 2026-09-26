[app]

# (str) Title of your application
title = YouTube Downloader

# (str) Package name
package.name = youtubedownloader

# (str) Package domain (needed for android/ios packaging)
package.domain = org.youtubedownloader

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,txt

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,yt-dlp,requests,certifi,urllib3,charset_normalizer,idna

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source = my_requirements_dir

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 2.3.0

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal, white, yellow, orange, violet, indigo
#android.presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format
#android.presplash_lottie = "path/to/lottie/file.json"

# (str) Adaptive icon of the application (used if Android API level is 26+)
#android.adaptive_icon = %(source.dir)s/data/icon.png

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE,FOREGROUND_SERVICE

# (list) features (adds uses-feature -tags to manifest)
#android.features = android.hardware.usb.host

# (int) Target Android API, should be as high as possible.
#android.api = 33

# (int) Minimum API your APK / AAB will support.
#android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 33

# (str) Android NDK version to use
#android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
#android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid extra downloads
#android.skip_update = False

# (bool) If True, then automatically accept SDK license
#android.accept_sdk_license = False

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
#android.activity_class_name = org.kivy.android.PythonActivity

# (str) Extra xml to write directly inside the <manifest> element of AndroidManifest.xml
#android.manifest_extra = <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />

# (str) Extra xml to write directly inside the <manifest><application> tag of AndroidManifest.xml
#android.manifest_extra_application = <provider android:name="androidx.core.content.FileProvider" android:authorities="${applicationId}.fileprovider" android:exported="false" android:grantUriPermissions="true"><meta-data android:name="android.support.FILE_PROVIDER_PATHS" android:resource="@xml/file_paths"></meta-data></provider>

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Android logcat output to stdout
#android.logcat = False

# (str) Android logcat format
#android.logcat_format = %(format)s

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# In past, was `android.arch` = armeabi-v7a
android.archs = arm64-v8a, armeabi-v7a

# (int) overrides automatic versionCode computation (used in build.gradle)
#android.numeric_version = 1

# (bool) enables Android auto backup feature (Android API >= 23)
android.allow_backup = True

# (str) XML file for custom backup rules (see official Android documentation)
#android.backup_rules =

# (str) XML file for custom full backup content (see official Android documentation)
#android.full_backup_content =

# (str) XML file for custom data extraction rules (see official Android documentation)
#android.data_extraction_rules =

# (str) XML file for custom backup rules for Android 12+
#android.backup_rules_v31 =

#
# Python for android (p4a) specific
#

# (str) python-for-android URL to use for checkout
#p4a.url = https://github.com/kivy/python-for-android.git

# (str) python-for-android branch to use
#p4a.branch = master

# (str) python-for-android git commit to use
#p4a.commit = HEAD

# (str) python-for-android fork to use in case fork is needed
#p4a.fork = kivy

# (str) python-for-android bootstrap to use
#p4a.bootstrap = sdl2

# (int) port number to specify an export port for the p4a
#p4a.port = 8888

# (str) Comma separated extra flags to pass to p4a
#p4a.extra_flags =

#
# iOS specific
#

# (str) Path to the certificate for signing the .ipa file
#ios.codesign.allowed = false

# (str) Name of the certificate to use for signing the .ipa file
#ios.codesign.identity =

# (str) Path to the provisioning profile for the .ipa file
#ios.provisioning_profile =

# (str) URL to the App Store
#ios.url =

# (str) Custom entitlements file to add to the .ipa file
#ios.entitlements =

# (bool) Should use the new Xcode build system (only for Xcode >= 10)
#ios.new_build = True

# (bool) Use .aab instead of .apk for Android
#android.release_artifact = aab

#
# Buildozer global
#

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
#build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa, .aab, etc.) storage
#bin_dir = ./bin

#    -----------------------------------------------------------------------------
#    List as sections
#
#    You can define all the "list" as [section:key].
#    Each line will be considered as a option to the list.
#    Let's take [app] / source.exclude_patterns.
#    Instead of doing:
#
#[app]
#source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
#    This can be translated into:
#
#[app:source.exclude_patterns]
#license
#data/audio/*.wav
#data/images/original/*
#
#
#    -----------------------------------------------------------------------------
#    Profiles
#
#    You can extend section / key with a profile
#    For example, you want to deploy a demo version of your application without
#    HD content. You could do:
#
#    [app@demo]
#    title = My Application (demo)
#
#    [app:source.exclude_patterns@demo]
#    images/hd/*
#
#    Then, invoke the command line with the "demo" profile:
#
#    buildozer@demo android debug
#

#    -----------------------------------------------------------------------------
#    Commands alias
#
#    You can define your own command that will execute a list of commands
#
#    [commands]
#    mycommand = adb logcat -s python

# (str) Alias to run test
# test = pytest

# (str) Custom hook to run before building
# pre_build_hook = my_hook.py

# (str) Custom hook to run after building
# post_build_hook = my_hook.py

#    -----------------------------------------------------------------------------
#    Add your own options
#    -----------------------------------------------------------------------------

# Example:
# [mysection]
# myoption = somevalue

# (str) Minimum ios version
#ios.min_os_version = 11.0

# (str) Bundle identifier for ios
#ios.bundle_id =

# (str) Framework directory
#ios.framework_dir =

# (bool) If True, include all python stdlib modules in the package
#p4a.whitelist_modules =

# (str) Path to the icon for the app
#icon.filename = icon.png