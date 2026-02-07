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
    
