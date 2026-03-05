from pathlib import Path
from typing import List, Optional, Any, Dict
import sqlite3
from src.finance_tracker.model import Transaction


DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "finance.db"

class TransactionStorage:

    def __init__(self, db_path: Path= DB_PATH):
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def add_transaction(self,transaction: Transaction) -> int:
        """Add a transaction to the database, using a Transaction object
            Returns a transaction ID."""
        if transaction.id is not None:
            raise ValueError("Cannot add a transaction with an id")

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO transactions (amount, date, description, type, category)
        VALUES (?, ?, ?, ?, ?)""", (
            transaction.amount,
            transaction.date,
            transaction.description,
            transaction.type,
            transaction.category
        ))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return new_id

    def get_all_transactions(self) -> List[Transaction]:
        """ Returns all transactions as a list of dictionary. """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        transactions_rows = cursor.fetchall()
        conn.close()

        return [Transaction.from_db_row(dict(row)) for row in transactions_rows]

    def get_transactions_by_id(self, tx_id: int) -> Optional[Dict[str, Any]]:
        """ Returns a single transaction matching the given transaction ID or None if not found."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM transactions WHERE id = ?", (tx_id,))
        transactions_row = cursor.fetchone()
        conn.close()

        return Transaction.from_db_row(dict(transactions_row)) if transactions_row else None

    def delete_transaction(self, tx_id: int) -> bool:
        """Deletes a transaction using its ID, returns True if deleted and False otherwise."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
        if_deleted = cursor.rowcount > 0

        conn.commit()
        conn.close()

        return if_deleted

    def get_balance(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END),0)-
            COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END),0)
        AS balance
        FROM transactions
        """)
        result = cursor.fetchone()
        conn.close()

        return result["balance"] if result else 0.0

if __name__ == "__main__":
    storage = TransactionStorage()

#Tests
    #Adding test
t1 = Transaction.create_new(
    amount=10000,
    date= "2026-02-16",
    description="My january salary",
    type_="income",
    category="salary"
)