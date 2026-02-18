#!/bin/bash

# Build and Install Smart Translator App
# Run this script to build the app and install it to Applications

echo "🔨 Building Smart Translator app..."

# Clean previous builds
rm -rf build dist

# Build the app
python3 setup.py py2app

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    
    # Install to Applications folder
    echo "📦 Installing to Applications folder..."
    
    # Remove old version if exists
    if [ -d "/Applications/Smart Translator.app" ]; then
        echo "🗑️  Removing old version..."
        rm -rf "/Applications/Smart Translator.app"
    fi
    
    # Copy new version
    cp -R "dist/smart_translator_dynamic.app" "/Applications/Smart Translator.app"
    
    if [ $? -eq 0 ]; then
        echo "🎉 Installation complete!"
        echo "📍 Smart Translator installed to /Applications/Smart Translator.app"
        echo ""
        echo "⚠️  IMPORTANT: First launch instructions:"
        echo "1. Open System Preferences > Security & Privacy > Privacy"
        echo "2. Add Smart Translator to 'Accessibility' (for clipboard access)"
        echo "3. Add Smart Translator to 'Notifications' (for notifications)"
        echo "4. Launch the app from Applications folder"
        echo ""
        echo "🚀 You can now launch Smart Translator!"
        
        # Optionally launch the app
        read -p "Launch Smart Translator now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            open "/Applications/Smart Translator.app"
        fi
    else
        echo "❌ Installation failed. Please check permissions."
    fi
else
    echo "❌ Build failed. Please check for errors above."
fi