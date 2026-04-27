import pytest
from src.finance_tracker.model import Transaction

def test_create_transaction():
    transaction = Transaction.create_new(
        amount=100,
        date="2026-04-27",
        description="Foodstuffs",
        type_="expense",
        category="Food"
    )
    assert transaction.amount == 100
    assert transaction.date == "2026-04-27"
    assert transaction.description == "Foodstuffs"
    assert transaction.is_expense == True
    assert transaction.signed_amount == -100

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

def test_str_representation():
    t1 = Transaction.create_new(amount=500, date="2026-04-15", type_="income", description="Test", category="Bonus")
    assert "2026-04-15" in str(t1)
    assert "Test" in str(t1)
    assert "500" in str(t1)

def test_input_arrangement():
    t1 = Transaction.create_new(amount=500, date=" 2026-04-15 ", type_="INCOME  ", description="  TEST", category="  Salary" )
    assert t1.date == "2026-04-15"
    assert t1.type == "income"
    assert t1.description == "test"
    assert t1.category == "salary"

