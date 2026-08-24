import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "stockpilot.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    conn = get_connection()
    schema_path = BASE_DIR / "schema.sql"
    with open(schema_path, "r") as file:
        schema = file.read()
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print("Database initialized successfully.")