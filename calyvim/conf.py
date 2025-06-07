import importlib
import sys
from pathlib import Path


class LazySettings:
    _module = None

    def configure(self, module_path: str):
        # Ensure the parent directory of the module (like config/) is in sys.path
        parts = module_path.split(".")
        if len(parts) > 1:
            parent_dir = Path().resolve()
            if str(parent_dir) not in sys.path:
                sys.path.insert(0, str(parent_dir))

        self._module = importlib.import_module(module_path)

    def __getattr__(self, name):
        if not self._module:
            raise RuntimeError("Settings have not been configured yet.")
        return getattr(self._module, name)


# Global settings object
settings = LazySettings()
