"""Settings and configuration management"""

import json
import os
from typing import Any, Dict


class Settings:
    """Manage application settings"""

    DEFAULT_SETTINGS = {
        "theme": "light",
        "default_model": "gpt-oss-20b",
        "default_tone": "Professional",
        "default_style": "Concise",
        "default_language": "English",
        "auto_save_history": True,
        "show_advanced_options": False,
        "export_format": "txt",
        "session_memory_enabled": True,
    }

    SETTINGS_FILE = "settings.json"

    def __init__(self, settings_file: str = SETTINGS_FILE):
        self.settings_file = settings_file
        self.settings = self._load_settings()

    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file or create default"""

        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as f:
                    loaded = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    settings = {**self.DEFAULT_SETTINGS, **loaded}
                    return settings
        except Exception:
            pass

        return self.DEFAULT_SETTINGS.copy()

    def _save_settings(self):
        """Save settings to file"""

        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            raise RuntimeError(f"Failed to save settings: {str(e)}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value"""

        return self.settings.get(key, default)

    def set(self, key: str, value: Any):
        """Set setting value"""

        self.settings[key] = value
        self._save_settings()

    def get_all(self) -> Dict[str, Any]:
        """Get all settings"""

        return self.settings.copy()

    def reset_to_defaults(self):
        """Reset settings to defaults"""

        self.settings = self.DEFAULT_SETTINGS.copy()
        self._save_settings()

    def update_settings(self, updates: Dict[str, Any]):
        """Update multiple settings at once"""

        self.settings.update(updates)
        self._save_settings()

    # Convenience methods for specific settings
    def set_theme(self, theme: str):
        """Set color theme"""
        if theme in ["light", "dark"]:
            self.set("theme", theme)

    def get_theme(self) -> str:
        """Get color theme"""
        return self.get("theme", "light")

    def set_default_model(self, model: str):
        """Set default AI model"""
        self.set("default_model", model)

    def get_default_model(self) -> str:
        """Get default AI model"""
        return self.get("default_model", "gpt-oss-20b")

    def set_default_tone(self, tone: str):
        """Set default tone"""
        self.set("default_tone", tone)

    def get_default_tone(self) -> str:
        """Get default tone"""
        return self.get("default_tone", "Professional")

    def set_default_style(self, style: str):
        """Set default style"""
        self.set("default_style", style)

    def get_default_style(self) -> str:
        """Get default style"""
        return self.get("default_style", "Concise")

    def set_default_language(self, language: str):
        """Set default language"""
        self.set("default_language", language)

    def get_default_language(self) -> str:
        """Get default language"""
        return self.get("default_language", "English")

    def set_export_format(self, format: str):
        """Set default export format"""
        if format in ["txt", "docx", "pdf"]:
            self.set("export_format", format)

    def get_export_format(self) -> str:
        """Get default export format"""
        return self.get("export_format", "txt")

    def enable_session_memory(self, enabled: bool):
        """Enable/disable session memory"""
        self.set("session_memory_enabled", enabled)

    def is_session_memory_enabled(self) -> bool:
        """Check if session memory is enabled"""
        return self.get("session_memory_enabled", True)

    def enable_auto_save(self, enabled: bool):
        """Enable/disable auto save history"""
        self.set("auto_save_history", enabled)

    def is_auto_save_enabled(self) -> bool:
        """Check if auto save is enabled"""
        return self.get("auto_save_history", True)


class SessionMemory:
    """Manage session-based memory during app runtime"""

    def __init__(self):
        self.memory = {
            "last_generated_content": None,
            "last_content_type": None,
            "last_topic": None,
            "last_model": None,
            "generation_count": 0,
            "total_words_generated": 0,
            "favorites": [],
        }

    def update_last_generation(
        self,
        content: str,
        content_type: str,
        topic: str,
        model: str,
        word_count: int = None,
    ):
        """Update last generated content info"""

        self.memory["last_generated_content"] = content
        self.memory["last_content_type"] = content_type
        self.memory["last_topic"] = topic
        self.memory["last_model"] = model
        self.memory["generation_count"] += 1

        if word_count:
            self.memory["total_words_generated"] += word_count
        else:
            self.memory["total_words_generated"] += len(content.split())

    def get_last_generation(self) -> Dict[str, Any]:
        """Get last generated content info"""

        return {
            "content": self.memory.get("last_generated_content"),
            "content_type": self.memory.get("last_content_type"),
            "topic": self.memory.get("last_topic"),
            "model": self.memory.get("last_model"),
        }

    def add_favorite(self, content: str):
        """Add to session favorites"""

        if content not in self.memory["favorites"]:
            self.memory["favorites"].append(content)

    def remove_favorite(self, content: str):
        """Remove from session favorites"""

        if content in self.memory["favorites"]:
            self.memory["favorites"].remove(content)

    def get_favorites(self):
        """Get session favorites"""

        return self.memory["favorites"]

    def get_stats(self) -> Dict[str, Any]:
        """Get session statistics"""

        return {
            "generation_count": self.memory["generation_count"],
            "total_words_generated": self.memory["total_words_generated"],
            "favorites_count": len(self.memory["favorites"]),
            "last_model": self.memory["last_model"],
        }

    def clear(self):
        """Clear session memory"""

        self.memory = {
            "last_generated_content": None,
            "last_content_type": None,
            "last_topic": None,
            "last_model": None,
            "generation_count": 0,
            "total_words_generated": 0,
            "favorites": [],
        }
