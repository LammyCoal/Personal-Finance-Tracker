from operator import truediv

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

def test_invalid_type():
    with pytest.raises(ValueError, match="Invalid transaction type"):
        Transaction.create_new(amount=100, date="2026-04-15", type_="food supply")

def test_invalid_date():
    with pytest.raises(ValueError, match="Invalid transaction date"):
        Transaction.create_new(amount=100, date="2026/04/15")

def test_transaction_properties():
    t1 = Transaction.create_new(amount=500, date="2026-04-15", type_="income")
    assert t1.is_income is True
    assert t1.signed_amount == 500

    t2 = Transaction.create_new(amount=1000, date="2026-04-15", type_="expense")
    assert t2.is_expense is True
    assert t2.signed_amount == -1000
