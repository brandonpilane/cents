import click
import csv
from pathlib import Path

data = Path.home() / "cents.csv" # Path to the CSV file

def not_found():
    """
        Function to handle the case when the CSV file is not found.
        It creates a new CSV file with the appropriate headers.
    """
    click.echo(f"No transactions found. Run \'"+ click.style("cents add", fg="green") + f"\' to add a new transaction.")
    with open(data, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Id", "Date", "Description", "Amount", "Type"])

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(f"Cents, a CLI for managing your finances.")
        if not data.exists():
            not_found()
        click.echo(cli.get_help(ctx))  # Show help message

@cli.command()
@click.argument("desc")
@click.argument("amount")
def add(desc, amount):
    """
        Add a new transaction.

        Args: 
            desc: Description of the transaction
            amount: Amount of the transaction   

        Example:
            cents add "Groceries" 100
    
    """
    click.echo(f"Adding transaction: {desc} for {amount}")
