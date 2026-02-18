# 🌍 Smart Translator for macOS

A lightweight, privacy-focused macOS menu bar application that uses local LLMs (via Ollama) to translate and correct text directly from your clipboard.

## ✨ Features

* **Clipboard Integration:** Instantly process text currently in your clipboard without opening a new window.
* **Local Privacy:** All processing happens locally on your machine using Ollama. No data is sent to the cloud.
* **Smart Modes:**
    * **Correct Clipboard:** Fixes grammar, spelling, and clarity while preserving original formatting.
    * **Translation:** Supports translation to Chinese, French, and English.
* **Dynamic Model Switching:** Automatically detects models installed in Ollama (e.g., Llama 3.2, Mistral, DeepSeek) and allows you to switch between them on the fly.
* **Undo Capability:** Accidentally overwrote your clipboard? Quickly undo the last operation.
* **Native Experience:** distinct menu bar icon, system notifications, and native macOS build.

## 🛠️ Prerequisites

1.  **macOS** (Silicon or Intel)
2.  **Ollama** must be installed and running.
    * Download from [ollama.com](https://ollama.com)
    * Ensure the server is running (`ollama serve`).
3.  **Models:** You need at least one model pulled. For example:
    ```bash
    ollama pull llama3.2
    ollama pull mistral
    ```

## 🚀 Installation

### Option 1: Build the App (Recommended)

This allows you to install it as a proper Application in your `/Applications` folder.

1.  Clone this repository.
2.  Make the build script executable:
    ```bash
    chmod +x build_script.sh
    ```
3.  Run the build script:
    ```bash
    ./build_script.sh
    ```
    *This script will clean previous builds, package the app using `py2app`, and move it to your Applications folder.*

4.  **Important Permissions:**
    Upon first launch, you must grant the app permissions to modify your clipboard:
    * Open **System Preferences** > **Security & Privacy** > **Privacy**.
    * Add **Smart Translator** to **Accessibility**.
    * Allow **Notifications** when prompted.

### Option 2: Run from Source

If you want to develop or test without building:

1.  Install dependencies:
    ```bash
    pip install rumps requests pyperclip py2app
    ```
2.  Run the script:
    ```bash
    python3 smart_translator_dynamic.py
    ```

## ⚙️ Configuration

The app automatically manages configuration in `~/Library/Application Support/SmartTranslator/models.json`.

* **Refresh Models:** Click "Refresh from API" in the menu to sync with your current Ollama models.
* **Manual Config:** You can also run the included helper script to generate a config file manually:
    ```bash
    python3 generate_models_json.py
    ```

## 🖥️ Usage

1.  **Copy** any text you want to process.
2.  Click the **🌍 icon** in your menu bar.
3.  Select an action (e.g., "Correct Clipboard" or "Translate to French").
4.  Wait for the notification confirming completion.
5.  **Paste** the result—your clipboard has been automatically updated!

## 🔧 Troubleshooting

* **"Offline" Status:** Ensure Ollama is running (`ollama serve`) and accessible at `localhost:11434`.
* **Installation Failed:** If the build script fails, ensure you have `py2app` installed (`pip install py2app`).
* **Clipboard not changing:** Verify that you have granted Accessibility permissions in System Settings.
