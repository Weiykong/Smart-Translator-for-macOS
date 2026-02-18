import requests
import rumps
import pyperclip
from collections import deque
import json
import os
from datetime import datetime

class SmartTranslatorApp(rumps.App):
    def __init__(self):
        super().__init__("🌍 Translator")
        self.clipboard_history = deque(maxlen=5)
        self.model = None
        self.available_models = []
        self.online = False
        self.models_file = os.path.expanduser("~/Library/Application Support/SmartTranslator/models.json")
        self.ensure_config_directory()
        self.load_models_from_file()
        self.setup_menu()
        self.check_connection()

    def ensure_config_directory(self):
        """Ensure the configuration directory exists"""
        config_dir = os.path.dirname(self.models_file)
        os.makedirs(config_dir, exist_ok=True)

    def load_models_from_file(self):
        """Load models list from JSON file"""
        try:
            if os.path.exists(self.models_file):
                with open(self.models_file, 'r') as f:
                    data = json.load(f)
                    self.available_models = data.get("models", [])
                    self.model = data.get("default_model")
                    
                    # If default model is not in available models, use the first one
                    if self.model not in self.available_models and self.available_models:
                        self.model = self.available_models[0]
                        
                print(f"Loaded {len(self.available_models)} models from file")
                
                # Show notification for loaded models
                if self.available_models:
                    model_name = self.model.split(':')[0] if ':' in self.model else self.model
                    rumps.notification("Models Loaded", f"📚 {len(self.available_models)} models", f"Default: {model_name}")
                        
            else:
                # If no file exists, try to fetch from API and create the file
                print("No models file found, fetching from API...")
                self.fetch_and_save_models()
                
        except Exception as e:
            print(f"Error loading models from file: {e}")
            self.available_models = []
            self.model = None

    def save_models_to_file(self):
        """Save current models list to JSON file"""
        try:
            data = {
                "models": self.available_models,
                "default_model": self.model,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.models_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            print(f"Saved {len(self.available_models)} models to file")
            
        except Exception as e:
            print(f"Error saving models to file: {e}")

    def fetch_and_save_models(self):
        """Fetch models from Ollama API and save to file"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            response.raise_for_status()
            
            data = response.json()
            if "models" in data:
                self.available_models = [model["name"] for model in data["models"]]
                
                # Set default model if none selected
                if not self.model and self.available_models:
                    self.model = self.available_models[0]
                
                # Save to file
                self.save_models_to_file()
                print(f"Fetched and saved {len(self.available_models)} models")
                
            else:
                print("No models found in API response")
                
        except Exception as e:
            print(f"Error fetching models from API: {e}")

    def setup_menu(self):
        """Setup the complete menu structure"""
        self.menu.clear()
        
        # Add main function items
        self.menu.add(rumps.MenuItem("Correct Clipboard", callback=self.correct_clipboard))
        self.menu.add(rumps.separator)
        self.menu.add(rumps.MenuItem("Translate to Chinese", callback=self.translate_to_chinese))
        self.menu.add(rumps.MenuItem("Translate to French", callback=self.translate_to_french))
        self.menu.add(rumps.MenuItem("Translate to English", callback=self.translate_to_english))
        self.menu.add(rumps.separator)
        
        # Add models submenu
        self.add_models_submenu()
        
        # Add remaining items
        self.menu.add(rumps.MenuItem("Undo Last", callback=self.undo_last))

    def add_models_submenu(self):
        """Add the models submenu to the menu"""
        if self.available_models:
            # Create models submenu
            if self.model:
                short_name = self.model.split(':')[0] if ':' in self.model else self.model
                models_menu = rumps.MenuItem(f"Model: {short_name}")
            else:
                models_menu = rumps.MenuItem("Models (none selected)")
            
            # Add model options
            for model_name in self.available_models:
                callback = self.create_model_callback(model_name)
                item_title = f"● {model_name}" if model_name == self.model else f"  {model_name}"
                models_menu.add(rumps.MenuItem(item_title, callback=callback))
            
            # Add separator and refresh option
            models_menu.add(rumps.separator)
            models_menu.add(rumps.MenuItem("↻ Refresh from API", callback=self.refresh_models))
            
        else:
            # No models available
            models_menu = rumps.MenuItem("Models (empty)")
            models_menu.add(rumps.MenuItem("No models found", callback=None))
            models_menu.add(rumps.separator)
            models_menu.add(rumps.MenuItem("↻ Refresh from API", callback=self.refresh_models))
        
        self.menu.add(models_menu)
        self.menu.add(rumps.separator)

    def check_connection(self):
        """Check Ollama connection status"""
        try:
            requests.get("http://localhost:11434", timeout=2)
            self.online = True
            self.title = "🌍 Translator"
        except Exception:
            self.online = False
            self.title = "❌ Offline"
            
        self.update_menu_state()

    def update_menu_state(self):
        """Update menu based on connection status and available models"""
        # Update main function menu items based on status
        translate_methods = [
            ("Correct Clipboard", self.correct_clipboard),
            ("Translate to Chinese", self.translate_to_chinese),
            ("Translate to French", self.translate_to_french),
            ("Translate to English", self.translate_to_english)
        ]
        
        for item_name, method in translate_methods:
            try:
                menu_item = self.menu[item_name]
                if self.available_models and self.model:
                    menu_item.set_callback(method)
                else:
                    menu_item.set_callback(None)
            except KeyError:
                continue

    def create_model_callback(self, model_name):
        """Create a callback function for model selection"""
        def callback(_):
            self.select_model(model_name)
        return callback

    def select_model(self, model_name):
        """Select a specific model and save to file"""
        old_model = self.model
        self.model = model_name
        self.save_models_to_file()  # Save the new default
        self.setup_menu()  # Rebuild menu to show updated selection
        
        # Show notification with model change info
        if old_model != model_name:
            short_name = model_name.split(':')[0] if ':' in model_name else model_name
            rumps.notification("Model Loaded", f"✅ {short_name}", f"Ready to use {model_name}")
        else:
            rumps.notification("Model Selected", "", f"Using: {model_name}")

    def refresh_models(self, _):
        """Manually refresh the list of available models from API"""
        self.title = "⏳ Refreshing..."
        
        try:
            # Check connection first
            requests.get("http://localhost:11434", timeout=2)
            self.online = True
            
            # Fetch and save new models
            old_count = len(self.available_models)
            self.fetch_and_save_models()
            self.setup_menu()  # Rebuild menu with new models
            
            new_count = len(self.available_models)
            if new_count != old_count:
                rumps.notification("Models Updated", f"🔄 Found {new_count} models", f"Changed from {old_count} models")
            else:
                rumps.notification("Models Refreshed", f"✅ {new_count} models", "No changes detected")
                
        except Exception:
            self.online = False
            rumps.notification("Refresh Failed", "❌ Connection error", "Ollama is not accessible")
        finally:
            self.title = "🌍 Translator" if self.online else "❌ Offline"

    def translate_to_chinese(self, _):
        self.process_and_update("Chinese")
    
    def translate_to_french(self, _):
        self.process_and_update("French")
    
    def translate_to_english(self, _):
        self.process_and_update("English")

    def process_text(self, text, action):
        """Process text using the selected model"""
        if not self.model:
            return "Error: No model selected"
            
        self.title = "⏳ Processing..."
        try:
            prompt = self.build_prompt(text, action)
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            if "response" in result:
                return result["response"].strip()
            else:
                return f"Error: Unexpected response format: {result}"
                
        except json.JSONDecodeError as e:
            return f"JSON Error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            self.title = "🌍 Translator" if self.online else "❌ Offline"

    def build_prompt(self, text, action):
        """Build prompt for the LLM based on the action"""
        if action == "correct":
            return f"""You're a language enhancer expert. 
        Your role is to enhance and correct input text while preserving its language:
        1. Fix spelling/grammar
        2. Improve clarity
        3. Keep original formatting
        Return ONLY the corrected text without any explanations or commentary.
        Keep the original line breaks, spacing, and formatting.
        Keep the original text in the same language (English or French).
        Keep the tone and style of the original text.
        Now, correct this text:

Text:
{text}"""
        else:
            return f"""You're a translator expert. 
        - Accurate: Maintain the exact meaning of the original text
        - Save 原样: Preserve all original formatting, spacing, and special characters
        - Return ONLY the translated text without any explanations or commentary
        Now, translate this text to {action}:

Text:
{text}"""

    def correct_clipboard(self, _):
        self.process_and_update("correct")

    def process_and_update(self, action):
        """Process clipboard content and update it with the result"""
        original = pyperclip.paste().strip()
        if not original:
            rumps.notification("Error", "", "Clipboard is empty")
            return
        
        if not self.model:
            rumps.notification("Error", "", "No model selected")
            return
        
        # Show processing started notification
        short_model = self.model.split(':')[0] if ':' in self.model else self.model
        rumps.notification("Processing...", f"📝 {action}", f"Using {short_model}")
        
        processed = self.process_text(original, action)
        if processed and not processed.startswith("Error"):
            pyperclip.copy(processed)
            self.clipboard_history.append(processed)
            
            # Show completion notification with preview
            preview = processed[:50] + "..." if len(processed) > 50 else processed
            action_emoji = {"correct": "✏️", "Chinese": "🇨🇳", "French": "🇫🇷", "English": "🇺🇸"}.get(action, "✅")
            rumps.notification("Completed!", f"{action_emoji} {action} finished", preview)
        else:
            rumps.notification("Error", f"❌ {action} failed", processed)

    def quit_app(self, _):
        """Quit the application"""
        rumps.notification("Smart Translator", "👋 Goodbye!", "Application closing...")
        rumps.quit_application()

    def undo_last(self, _):
        """Undo last clipboard operation"""
        if len(self.clipboard_history) > 1:
            self.clipboard_history.pop()  # Remove current
            previous = self.clipboard_history[-1]  # Get the previous one
            pyperclip.copy(previous)
            preview = previous[:40] + "..." if len(previous) > 40 else previous
            rumps.notification("Undone", "↩️ Restored previous", preview)
        else:
            rumps.notification("Undo", "⚠️ Nothing to undo", "No previous versions available")

if __name__ == "__main__":
    # Set LSUIElement to hide dock icon - must be done before app initialization
    import AppKit
    info = AppKit.NSBundle.mainBundle().infoDictionary()
    info["LSUIElement"] = "1"
    
    app = SmartTranslatorApp()
    rumps.notification("Smart Translator", "🚀 Ready!", "Click the 🌍 icon to start translating")
    app.run()