from enum import Enum
from decimal import Decimal
from dataclasses import dataclass

class Category(Enum):
    FOOD = 'Food'
    TRANSPORT = 'Transport'
    UTILITY = 'Utility'
    RENT = 'Rent'
    OTHER = 'Other'

@dataclass
class Transaction:
    title: str
    amount: float
    category: Category

