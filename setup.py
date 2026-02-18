"""
Setup script to package the SmartTranslator app as a proper macOS application.
This creates a standalone app that can be installed in the Applications folder.
"""

from setuptools import setup

APP = ['smart_translator_dynamic.py']  # Your main script filename
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['rumps', 'requests'],
    'plist': {
        'LSUIElement': True,  # This hides the dock icon
        'CFBundleName': 'SmartTranslator',
        'CFBundleDisplayName': 'Smart Translator',
        'CFBundleIdentifier': 'com.yourusername.smarttranslator',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2025 Your Name',
        'NSUserNotificationAlertStyle': 'alert',  # Enable notifications
        'NSSupportsAutomaticTermination': False,  # Prevent auto-termination
        'LSBackgroundOnly': False,  # Allow notifications
    },
    'iconfile': 'icon.icns',  # Optional: path to your .icns icon file
    'includes': ['pyperclip', 'collections', 'json', 'os', 'datetime'],  # Ensure all dependencies
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)