import importlib


def belongs_to(model_name: str, fk: str = None):
    fk = fk or model_name.lower() + "_id"

    def getter(self):
        module_path = f"app.models.{model_name.lower()}"  # e.g., app.models.user
        model_module = importlib.import_module(module_path)
        model_cls = getattr(model_module, model_name)  # e.g., User
        fk_value = getattr(self, fk, None)
        if fk_value is None:
            return None
        return model_cls.find(fk_value)

    return property(getter)


def has_many(model_name: str, fk: str):
    def getter(self):
        if not hasattr(self, "id"):
            raise AttributeError("has_many() requires the instance to have an 'id'")

        module_path = f"app.models.{model_name.lower()}"
        model_module = importlib.import_module(module_path)
        model_cls = getattr(model_module, model_name)

        return model_cls.where(**{fk: self.id}).all()

    return property(getter)
