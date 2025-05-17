import click
import csv

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(f"Cents, a CLI for managing your finances.")
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
    