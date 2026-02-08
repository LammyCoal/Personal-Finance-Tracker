from __future__ import annotations
from dataclasses import dataclass,field
from datetime import datetime
from typing import Optional
import re

@dataclass(frozen=True)
class Transaction:
    id: Optional[int] = None
    amount: float = 0.0
    date: str = ""
    type: str = "expense"
    category: Optional[str] = None

    def __post_init__(self):
        """Run validation on all fields after dataclass initialization."""
        self._validate()

    def _validate(self):
        """Central method for all business rules, Validate all init fields"""
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if self.type not in ["expense", "income"]:
            raise ValueError("Type must be either expense or income")
        if not self.date:
            raise ValueError("Date cannot be empty, format must be in YYYY-MM-DD")

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", self.date):
            raise ValueError("Date must be in YYYY-MM-DD format")

        try:
            datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date!!, Must be a real calender date")

        @property
        def signed_amount(self) -> float:
            """Returns positive for income and negative for expense"""
            return self.amount if self.type == "income" else -self.amount

        @property
        def is_income(self) -> bool:
            """Returns if the transaction is an income transaction"""
            return self.type == "income"

        @property
        def is_expense(self) -> bool:
            """Returns if the transaction is an expense transaction"""
            return self.type == "expense"

        def __str__(self) -> str:
            sign = "+" if self.is_income else "-"
            category = f"[{self.category}]" if self.category else ''
            return(
                f"{self.date} {sign}{self.amount:,.2f}"
                f"{self.description} {category}"
                f"(id: {self.id if self.id is not None else 'New'})"
            )

        def __repr__(self) -> str:
            return f"Transaction(id={self.id}, amount={self.amount}, date='{self.date}', "\
                    f"type='{self.type}', description='{self.description}' category={self.category})"
            
