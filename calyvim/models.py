class CalyModel:
    table_name: str = None

    def __init__(self, *args, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    @classmethod
    def infer_table_name(cls):
        return cls.__name__.lower() + "s"

    @classmethod
    def all(cls):
        table = cls.table_name or cls.infer_table_name()
