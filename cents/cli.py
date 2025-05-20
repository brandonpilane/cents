import click
import csv
from pathlib import Path
from datetime import datetime
from tabulate import tabulate
from colorama import Fore, Style

data = Path.home() / ".cents.csv" # Path to the CSV file

def not_found(help=True):
    """
        Function to handle the case when the CSV file is not found.
        It creates a new CSV file with the appropriate headers.
    """
    if help:
        click.echo(f"No transactions found. Run \'"+ click.style("cents add", fg="green") + f"\' to add a new transaction.")
    with open(data, "w",newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Id", "Date", "Description", "Amount", "Type"])

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(f"Cents, a CLI for managing your finances.")
        if not data.exists() or data.stat().st_size == 0:
            not_found()
        click.echo(cli.get_help(ctx))  # Show help message

@cli.command()
@click.argument("desc")
@click.argument("amount", type=float)
@click.option("-t", "--type", type=click.Choice(["expense", "income"], case_sensitive=False), default="expense", help="Type of transaction: expense or income")
def add(desc, amount, type):
    """
        Add a new transaction.

        Args: 
            desc: Description of the transaction
            amount: Amount of the transaction   

        Examples:
            cents add "Groceries" 100
            cents add "Salary" 2000 -t income
    
    """
    if not data.exists() or data.stat().st_size == 0:
        not_found(help=False)

    typecolor = "red" if type == "expense" else "green"
    trans_id = len(data.read_text().splitlines())
    with open(data, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([str(trans_id), f"{datetime.now().strftime('%Y-%m-%d')}", desc.capitalize(), amount, type])
    click.echo(f"Transaction added: '{desc.capitalize()}' for " + click.style(f"{amount}", fg=typecolor))
    

def color_headers(headers):
    return [Fore.WHITE + Style.BRIGHT + header + Style.RESET_ALL for header in headers]

@cli.command(name="list")
@click.option("-t", "--type", type=click.Choice(["expense", "income"], case_sensitive=False), help="Filter output by type: expense or income")
@click.option("-v", "--verbose", is_flag=True, help="Show detailed output")
def list_transactions(type, verbose):
    """
        List all transactions.

        Args:
            type: Filter transactions by type (expense or income)
            verbose: Show detailed output

        Examples:
            cents list
            cents list -t income
            cents list -v
    """
    if not data.exists() or data.stat().st_size == 0:
        not_found()
        return

    with open(data, "r") as f:
        reader = csv.reader(f)
        transactions = list(reader)[1:] # Skip the header row

        #color the ammounts based on the type
        for i, row in enumerate(transactions):
            if row[4] == "expense":
                transactions[i][3] = click.style(row[3], fg="red")
            else:
                transactions[i][3] = click.style(row[3], fg="green")

        if verbose:
            filtered_transactions = filter(lambda x: x[4] == type, transactions) if type else transactions
            headers = ["Id", "Date", "Description", "Amount", "Type"]
        else:
            filtered_transactions = filter(lambda x: x[4] == type, transactions) if type else transactions
            # remove the "Id" column and the "Type" column for unverbose mode
            filtered_transactions = [row[:4] for row in filtered_transactions]
            headers = ["Id", "Date", "Description", "Amount"]
        # print the transactions in a table format
        colored_headers = color_headers(headers)
        print(tabulate(filtered_transactions, headers=colored_headers, tablefmt="fancy_grid", floatfmt=".2f", numalign="right", stralign="left"))