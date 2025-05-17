import click

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(f"Cents, a CLI for managing your finances.")
        click.echo(cli.get_help(ctx))  # Show help message