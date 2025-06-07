import sqlite3
from calyvim.conf import settings


def get_connection():
    global _connection
    if _connection is None:
        db = getattr(settings, "DATABASE", {})

        if db.get("ENGINE") == "sqlite":
            _connection = sqlite3.connect(db["NAME"], check_same_thread=False)
            _connection.row_factory = sqlite3.Row
        else:
            raise NotImplementedError("Only SQLite is supported.")
    return _connection
