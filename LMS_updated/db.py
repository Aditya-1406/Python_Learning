

import sqlite3
from pathlib import Path


DB_FILE = Path("lms_update.db")

class Database:
    """SQLite database wrapper with migrations and transaction support."""

    def __init__(self, path=DB_FILE):
        self.path = path

    def connect(self):
        conn = sqlite3.connect(str(self.path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def migrate(self):
        """Create schema if it does not exist."""
        schema = """
        CREATE TABLE IF NOT EXISTS member (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL, -- store a hash ideally
            role TEXT CHECK (role IN ('member', 'admin')) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS book (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            copies_available INTEGER NOT NULL CHECK (copies_available >= 0)
        );

        CREATE TABLE IF NOT EXISTS loan (
            loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            borrowed_on TEXT NOT NULL, -- ISO8601 date/time string
            due_on TEXT NOT NULL,
            returned_on TEXT,
            fine INTEGER NOT NULL DEFAULT 0,
            is_paid INTEGER NOT NULL DEFAULT 0, -- SQLite: 0=false, 1=true
            member_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            FOREIGN KEY (member_id) REFERENCES member(member_id),
            FOREIGN KEY (book_id) REFERENCES book(book_id)
        );
        """
        with self.connect() as conn:
            conn.executescript(schema)

   