import os
from pathlib import Path
from typing import Dict, Callable, List, Any

from a2r.conf import global_settings
from a2r.conf.reader import read_ini, read_json, read_yaml

TO_LOAD = [global_settings]
READERS: Dict[Callable, List[str]] = {
    read_json: [".json", ".jsn"],
    read_yaml: [".yaml", ".yml"],
    read_ini: [".ini"],
}


class Settings:
    def __init__(self, *modules):
        for module in modules:
            for setting in dir(module):
                if setting.isupper():
                    setattr(self, setting, getattr(module, setting))

    def configure(self, **ext_settings):
        """Set new settings or override default ones."""
        for key, value in ext_settings.items():
            if key.isupper():
                setattr(self, key, value)

    @classmethod
    def read_config(cls, f: Path, *args, **kwargs) -> Any:
        """Reads config_reader file using the best strategy and returns dict"""
        # Normalize the file extension
        _, ext = os.path.splitext(f)
        ext = ext.lower()

        # Find the correct reader based on file extension
        for func, exts in READERS.items():
            if ext in exts:
                return func(f, *args, **kwargs)

        # If no matching reader is found, raise an error
        raise ValueError(f"Unsupported file extension for file: {f}")


settings = Settings(*TO_LOAD)
