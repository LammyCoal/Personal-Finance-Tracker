from datetime import datetime
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from src.finance_tracker.model import Transaction
from src.finance_tracker.storage import TransactionStorage

app = typer.Typer(
    name="finance",
    help="Personal Finance Tracker CLI",
    add_completion=True,
)