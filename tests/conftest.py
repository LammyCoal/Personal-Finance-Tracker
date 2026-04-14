import pytest
from pathlib import Path
import tempfile
import shutil
from src.finance_tracker.storage import TransactionStorage
from src.finance_tracker.model import Transaction

@pytest.fixture(scope='function')
def test_db_path(tmp_path: Path)->Path:
    return tmp_path / 'test_finance.db'

@pytest.fixture(scope='function')
def storage(test_db_path: Path)->TransactionStorage:
    storage = TransactionStorage(db_path=test_db_path)
    conn = storage._get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL not null,
    date TEXT NOT NULL,
    description TEXT,
    category TEXT,
    type TEXT not null CHECK(type IN ('income', 'expense'))
    )
    """)
    conn.commit()
    conn.close()

    return storage

@pytest.fixture
def sample_transaction():
    return Transaction.create_new(
        amount=20000,
        date= "2026-14-4",
        description= "April salary",
        type_ = "income",
        category= "Salary"
    )