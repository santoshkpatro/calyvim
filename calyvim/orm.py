import importlib


def belongs_to(model_name: str, fk: str = None):
    fk = fk or model_name.lower() + "_id"

    def getter(self):
        fk_value = getattr(self, fk, None)
        if fk_value is None:
            return None

        try:
            module_path = f"app.models.{model_name.lower()}"
            model_module = importlib.import_module(module_path)
            model_cls = getattr(model_module, model_name)
        except (ImportError, AttributeError) as e:
            raise ImportError(
                f"Could not resolve model '{model_name}' from '{module_path}': {e}"
            )

        return model_cls.find(fk_value)

    return property(getter)


def has_many(model_name: str, fk: str):
    def getter(self):
        if not hasattr(self, "id") or self.id is None:
            raise AttributeError("has_many() requires a valid 'id' on the instance")

        try:
            module_path = f"app.models.{model_name.lower()}"
            model_module = importlib.import_module(module_path)
            model_cls = getattr(model_module, model_name)
        except (ImportError, AttributeError) as e:
            raise ImportError(
                f"Could not resolve model '{model_name}' from '{module_path}': {e}"
            )

        return model_cls.where(**{fk: self.id})  # returns a chainable QueryBuilder

    return property(getter)
