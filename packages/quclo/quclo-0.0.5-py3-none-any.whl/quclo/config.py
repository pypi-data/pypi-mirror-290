"""Configuration module for QuClo."""

import configparser
from typing import Dict
from quclo.utils import CONFIG_FILE


class Config:
    """A configuration"""

    parser = configparser.ConfigParser()
    parser.read(CONFIG_FILE)

    @staticmethod
    def _save_key_value(section: str, key: str, value: str):
        """Save a key value pair to the configuration file."""
        if section not in Config.parser:
            Config.parser[section] = {}
        Config.parser[section][key] = value
        with open(CONFIG_FILE, "w") as configfile:
            Config.parser.write(configfile)

    @staticmethod
    def _load_key_value(section: str, key: str) -> str | None:
        """Load a key value pair from the configuration file."""
        if section not in Config.parser:
            return None
        return Config.parser[section][key]

    @staticmethod
    def save_token(token: str):
        """Save the token to the configuration file."""
        Config._save_key_value("auth", "token", token)

    @staticmethod
    def load_token() -> str | None:
        """Load the token from the configuration file."""
        return Config._load_key_value("auth", "token")

    @staticmethod
    def save_default_user(email: str):
        """Save the default user to the configuration file."""
        Config._save_key_value("user", "email", email)

    @staticmethod
    def load_default_user() -> str | None:
        """Load the default user from the configuration file."""
        return Config._load_key_value("user", "email")

    @staticmethod
    def save_default_backend(backend: str):
        """Save the default backend to the configuration file."""
        Config._save_key_value("backend", "name", backend)

    @staticmethod
    def load_default_backend() -> str | None:
        """Load the default backend from the configuration file."""
        return Config._load_key_value("backend", "name")

    @staticmethod
    def save_default_priority(priority: str):
        """Save the default priority to the configuration file."""
        Config._save_key_value("priority", "value", priority)

    @staticmethod
    def load_default_priority() -> str | None:
        """Load the default priority from the configuration file."""
        return Config._load_key_value("priority", "value")

    @staticmethod
    def save_config(data: Dict[str, Dict[str, str]]):
        """Save the configuration to the configuration file."""
        for section, values in data.items():
            for key, value in values.items():
                Config._save_key_value(section, key, value)

    def __str__(self):
        """Return the configuration as a string."""
        string = ""
        for section in Config.parser.sections():
            string += f"[{section}]\n"
            for key, value in Config.parser[section].items():
                string += f"{key} = {value}\n"
        return string
