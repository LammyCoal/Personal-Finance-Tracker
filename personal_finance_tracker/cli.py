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

@app.command(name="list")
def list_transactions(
        oldest_first: bool = typer.Option(
        False,
        "--reverse",
        "-r",
        help="Shows the oldest transaction first.(default is newest first)",
        ),

        by_type: Optional[str] = typer.Option(
            None,
            "--type",
            "-t",
            help="Filter transactions by type: income or expense",
        ),
            
        by_category: Optional[str] = typer.Option(
            None,
            "--category",
            "-c",
            help="Filter transactions by category",
        ),
):
    """list  transactions in a beautiful table and also supports filtering"""
    storage = TransactionStorage()
    all_transactions = storage.get_all_transactions()
    if by_type:
        if by_type not in ["income", "expense"]:
            typer.secho(f"Error: Invalid type filter: {by_type}. Must be 'income' or 'expense'.", fg=typer.colors.RED, bold=True, err=True)
            raise typer.Exit(code=1)
        all_transactions = [t for t in all_transactions if t.type == by_type]
    if by_category:
        all_transactions = [t for t in all_transactions if t.category == by_category]
    

    if not all_transactions:
        typer.echo("No transactions yet")
        return

    tx = sorted(all_transactions, key=lambda t: t.date, reverse=not oldest_first)

    console = Console()
    table = Table(title="TRANSACTIONS", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Date")
    table.add_column("Type", style="blue")
    table.add_column("Amount", justify="right",style="magenta")
    table.add_column("Description")
    table.add_column("Category", style="yellow")

    for transaction in tx:
        amount_in_str = f"{transaction.signed_amount:+,.2f}"
        amount_style = "green" if transaction.is_income else "red"
        table.add_row(
            str(transaction.id),
            transaction.date,
            transaction.type.upper(),
            amount_in_str,
            transaction.description.capitalize() or "",
            transaction.category.capitalize() or "",
            style= amount_style if transaction.is_income or transaction.is_expense else None,
        )

    console.print(table)
    typer.secho(f"Total : {len(tx)} transaction(s)", dim=True)

@app.command()  
def balance():
        """Shows current balance"""
        stor = TransactionStorage()
        bal = stor.get_balance()
        colour = typer.colors.GREEN if bal > 0 else typer.colors.RED
        typer.secho(f"Your current balance: {bal:,.2f}", fg=colour, bold=True)

@app.command()
def delete(
            id_: int = typer.Argument(..., help="Transaction ID to delete."),
    ):
        """Deletes a transaction by ID"""
        sto = TransactionStorage()
        if sto.delete_transaction(id_):
            typer.secho(f"Deleted transaction with id: {id_}", fg=typer.colors.GREEN, bold=True)
        else:
            typer.secho(f"Failed: Transaction id not found!!!", fg=typer.colors.RED, bold=True , err=True)
            raise typer.Exit(code=1)


if __name__ == "__main__":
    app()