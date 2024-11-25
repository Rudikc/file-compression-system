import json
import os


class Settings:
    SETTINGS_FILE = "settings.json"

    def __init__(self):
        self.default_destination = ""
        self.default_algorithm = "zip"
        self.encryption_enabled = False
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, "r") as f:
                data = json.load(f)
                self.default_destination = data.get("default_destination", "")
                self.default_algorithm = data.get("default_algorithm", "zip")
                self.encryption_enabled = data.get("encryption_enabled", False)

    def save_settings(self):
        data = {
            "default_destination": self.default_destination,
            "default_algorithm": self.default_algorithm,
            "encryption_enabled": self.encryption_enabled,
        }
        with open(self.SETTINGS_FILE, "w") as f:
            json.dump(data, f, indent=4)
