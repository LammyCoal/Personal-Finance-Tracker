import pytest
from src.finance_tracker.model import Transaction
from tests.conftest import storage

def test_add_and_get_all_transactions(storage,sample_transaction):
    get_id = storage.add_transaction(sample_transaction)
    assert get_id is not None
    assert get_id > 0

    retrieve_tx = storage.get_transaction_by_id(get_id)
    assert retrieve_tx is not None
    assert retrieve_tx.amount == sample_transaction.amount
    assert retrieve_tx.description == sample_transaction.description
    assert retrieve_tx.type == sample_transaction.type

def test_get_all_transactions(storage):
    storage.add_transaction(Transaction.create_new(900, "2026-04-29",type_="income"))
    storage.add_transaction(Transaction.create_new(900, "2026-04-29",type_="expense"))

    all_txs = storage.get_all_transactions()
    assert len(all_txs) == 2

def test_delete_transactions(storage,sample_transaction):
    tx= storage.add_transaction(sample_transaction)
    assert storage.delete_transaction(tx) is True

    assert storage.delete_transaction(tx) is False
    assert storage.get_transaction_by_id(tx) is None

def test_balance(storage):
    storage.add_transaction(Transaction.create_new(1000, "2026-04-29",type_="income"))
    storage.add_transaction(Transaction.create_new(500, "2026-04-29",type_="expense"))
    storage.add_transaction(Transaction.create_new(200, "2026-04-29",type_="expense"))

    balance = storage.get_balance()
    assert balance == 300

def test_balance_without_tx(storage):
    balance = storage.get_balance()
    assert balance == 0

def test_update_transaction(storage,sample_transaction):
    original_tx_id = Transaction.create_new(
        amount=1000,
        date="2026-04-29",
        type_="income",
        description="Original income",
        category="Allawee"
    )


    tx_id = storage.add_transaction(original_tx_id)

    updated_tx = Transaction(
        id=tx_id,
        amount=2000,
        date="2026-04-30",
        type="expense",
        description="Updated income",
        category="Allawee"
    )

    result = storage.update_transaction(updated_tx)
    assert result is True

    retrieved_tx = storage.get_transaction_by_id(tx_id)
    assert retrieved_tx is not None
    assert retrieved_tx.amount == 2000
    assert retrieved_tx.date == "2026-04-30"
    assert retrieved_tx.type == "expense"
    assert retrieved_tx.description == "Updated income"
    assert retrieved_tx.category == "Allawee"

def test_update_transaction_without_id(storage):
    transaction = Transaction.create_new(
        amount = 10000,
        date = "2026-09-21",
        type_ = "expense"
    )

    try:
        storage.update_transaction(transaction)
        assert False, "should return valueError"
    except ValueError:
        pass

