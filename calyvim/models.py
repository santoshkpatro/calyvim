import sqlite3
from calyvim.conf import settings


class QueryBuilder:
    def __init__(self, model_cls):
        self.model_cls = model_cls
        self.conditions = []

    def where(self, **kwargs):
        self.conditions.append(kwargs)
        return self

    def all(self):
        table = self.model_cls.get_table_name()
        conn = self.model_cls.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        clauses = []
        values = []

        for cond in self.conditions:
            for key, val in cond.items():
                clauses.append(f"{key} = ?")
                values.append(val)

        sql = f"SELECT * FROM {table}"
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)

        cursor.execute(sql, values)
        rows = cursor.fetchall()
        conn.close()

        return [self.model_cls(**dict(row)) for row in rows]


class CalyModel:
    db_table: str = None

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    @classmethod
    def infer_table_name(cls):
        return cls.__name__.lower() + "s"

    @classmethod
    def get_table_name(cls):
        return cls.db_table or cls.infer_table_name()

    @classmethod
    def get_connection(cls):
        db_path = settings.DATABASE.get("NAME")
        if not db_path:
            raise ValueError("Database path is not set in settings.")
        return sqlite3.connect(db_path)

    @classmethod
    def all(cls):
        table = cls.get_table_name()
        conn = cls.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        conn.close()
        return [cls(**dict(row)) for row in rows]

    @classmethod
    def find(cls, pk):
        table = cls.get_table_name()
        conn = cls.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE id = ?", (pk,))
        row = cursor.fetchone()
        conn.close()
        return cls(**dict(row)) if row else None

    @classmethod
    def where(cls, **conditions):
        return QueryBuilder(cls).where(**conditions)

    def save(self):
        table = self.get_table_name()
        fields = []
        values = []
        placeholders = []

        for key, val in self.__dict__.items():
            if key == "id":
                continue  # Skip 'id' if it's an auto-increment primary key
            fields.append(key)
            values.append(val)
            placeholders.append("?")

        sql = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        self.id = cursor.lastrowid  # Assign the new id
        conn.close()
