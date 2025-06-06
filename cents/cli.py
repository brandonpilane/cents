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
        click.echo(click.style("Cents", fg="magenta", blink=True) + f", a CLI for managing your finances.")
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

@cli.command()
@click.argument("id")
def delete(id):
    """
        Delete a transaction by ID.

        Args:
            id: ID of the transaction to delete

        Examples:
            cents delete 1
    """
    if not data.exists() or data.stat().st_size == 0:
        not_found()
        return

    with open(data, "r") as f:
        reader = csv.reader(f)

        rows = list(reader)

        header = list(rows)[0]  # Read the header
        transactions = list(rows)[1:]  # Read the transactions
        # Check if the transaction ID exists
        if not any(row[0] == id for row in transactions):
            click.echo(f"Transaction with id {id} " +  click.style("not found.", fg="red", italic=True))
            return
        # Filter out the transaction to delete
        filtered = [row for row in transactions if row[0] != id]
        # Reassign IDs to be sequential again
        for i, row in enumerate(filtered):
            row[0] = str(i + 1)
        # Write everything back, including the header
        with open(data, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(filtered)
            
    click.echo(f"Transaction with id {id} deleted.")

@cli.command()
@click.argument("id", type=int)
@click.option("--desc", type=str, help="New description of the transaction")
@click.option("--amount", type=float, help="New amount of the transaction")
@click.option("-t", "--type", type=click.Choice(["expense", "income"], case_sensitive=False), help="New type of the transaction")
def edit(id, desc, amount, type):
    """
        Edit a transaction by ID.

        Args:
            id: ID of the transaction to edit
            desc: New description of the transaction
            amount: New amount of the transaction
            type: New type of the transaction

        Examples:
            cents edit 1 --desc "New description"
            cents edit 1 --amount 1000 --type income   
            cents edit 1 --desc "New description" --amount 1000 --type income
            cents edit 1 --type income
    """
    
    updates = {}
    if desc is not None:
        updates["description"] = desc
    if amount is not None:
        updates["amount"] = amount
    if type is not None:
        updates["type"] = type.lower()
    
    if not updates:
        click.echo("No fields to update. Use --desc, --amount, or --type.")
        return

    with open(data, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
        header = list(rows)[0]  # Read the header
        transactions = list(rows)[1:] # Skip the header row
        
        # Check if the transaction ID exists
        if not any(row[0] == id for row in transactions):
            click.echo(f"Transaction with id {id} not found.")
            return
        
        # Find the transaction to edit
        for i, row in enumerate(transactions):
            if row[0] == id:
                break
        else:
            click.echo(f"Transaction with id {id} not found.")
            return
        
        # Update the transaction
        transactions[i][1:] = [updates.get(key, value) for key, value in zip(transactions[i][1:], row[1:])]
        
        # Reassign IDs to be sequential again
        for i, row in enumerate(transactions):
            row[0] = str(i + 1)
        
        # Write everything back, including the header
        with open(data, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(transactions[1:])

    click.echo(f"Transaction with id {id} edited.")