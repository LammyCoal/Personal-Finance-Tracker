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

@app.command()
def add(
        amount: float = typer.Argument(..., help="Amount to be added: Must be positive."),
        date: str = typer.Option(
            None,
            "--date",
            "-d",
            help="Date of when the transaction is added. YYYY-MM-DD(default: today",
        ),
        description: str = typer.Option(
            '',
            "--description",
            "-desc",
            help="Description of the transaction.",
        ),
        type_: str = typer.Option(
            "expense",
            "--type",
            "-t",
            help="Type of the transaction: income or expense",
        ),
        category: Optional[str] = typer.Option(
            None,
            "--category",
            "-c",
            help="Category( e.g salary, food, gym)",
        ),
):
    """Adds a new transaction"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    try:
        tn= Transaction.create_new(
            amount=amount,
            date=date,
            description=description,
            category=category,
            type_=type_,
        )
        storage = TransactionStorage()
        new_id = storage.add_transaction(tn)
        typer.secho(f"✓ Successfully added: {new_id}", fg=typer.colors.GREEN, bold=True)
        typer.echo(tn)
    except ValueError as ve:
        typer.secho(f"Error: {ve}", fg=typer.colors.RED, bold=True, err=True)
        raise typer.Exit(code=1)
