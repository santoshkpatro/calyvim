import importlib


class LazySettings:
    _module = None

    def configure(self, module_path: str):
        self._module = importlib.import_module(module_path)

    def __getattr__(self, name):
        if not self._module:
            raise RuntimeError("Settings have not been configured yet.")
        return getattr(self._module, name)


# Global settings object
settings = LazySettings()
