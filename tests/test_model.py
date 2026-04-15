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

def test_negative_amount():
    with pytest.raises(ValueError, match="Amount cannot be negative"):
        Transaction.create_new(amount=-1900, date="2026-04-15", type_= "expense")

