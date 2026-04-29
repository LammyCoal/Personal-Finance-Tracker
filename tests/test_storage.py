import pytest
from src.finance_tracker.model import Transaction

def test_add_and_get_all_transactions(storage,sample_transaction):
    get_id = storage.add_transaction(sample_transaction)
    assert get_id is not None
    assert get_id > 0

    retrieve_tx = storage.get_transactions_by_id(get_id)
    assert retrieve_tx is not None
    assert retrieve_tx['amount'] == sample_transaction.amount
    assert retrieve_tx['description'] == sample_transaction.description
    assert retrieve_tx['type'] == sample_transaction.type

def test_get_all_transactions(storage):
    storage.add_transaction(Transaction.create_new(900, "2026-04-29",type_="income"))
    storage.add_transaction(Transaction.create_new(900, "2026-04-29",type_="expense"))

    all_txs = storage.get_all_transactions()
    assert len(all_txs) == 2

def test_delete_transactions(storage,sample_transaction):
    tx= storage.add_transaction(sample_transaction)
    assert storage.delete_transaction(tx) is True

    assert storage.delete_transaction(tx) is False
    assert storage.get_transactions_by_id(tx) is None
    