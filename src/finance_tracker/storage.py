from pathlib import Path
from typing import List, Optional, Any, Dict
import sqlite3

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "finance.db"

class TransactionStorage:

    def __init__(self, db_path: Path= DB_PATH):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def add_transaction(self,
                        amount:float,
                        date: str,
                        description: str= "",
                        type_: str= "expense",
                        category: Optional[str] =None) -> int:
        """Add a transaction to the database.
            Returns a transaction ID."""
        if type_ not in ("expense", "income"):
            raise ValueError("Type must be either expense or income ")

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO transactions (amount, date, description, type_, category)
        VALUES (?, ?, ?, ?, ?)""", (amount, date, description, type_, category))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return new_id