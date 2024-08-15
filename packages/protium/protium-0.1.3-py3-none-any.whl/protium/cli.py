# /cli.py

import json

import click

from .api import ApiClient
from .version import __version__

# Create an instance of ApiClient
api_client = ApiClient()


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(f"protium CLI version {__version__}")
        click.echo("Use one of the following commands:")
        click.echo("  list    - List all projects")
        click.echo("  create  - Create a project from a JSON file")
        click.echo("  version - Display the version number")
        click.echo("\nUse 'ptm <command> --help' for more information on a command.")


@click.command()
def list():
    """List all projects"""
    response = api_client.list()
    if response:
        click.echo(json.dumps(response, indent=2))
    else:
        click.echo("Failed to retrieve the list.")


@click.command()
@click.option("-f", "--file", type=click.Path(exists=True), help="JSON file to upload")
def create(file):
    """Create a project from a JSON file"""
    if file:
        try:
            with open(file, "r") as f:
                data = json.load(f)
            response = api_client.create(data)
            click.echo(json.dumps(response, indent=2))
        except json.JSONDecodeError:
            click.echo("Invalid JSON file.")
        except Exception as e:
            click.echo(f"Error: {e}")
    else:
        click.echo("No file provided. Use the -f option to specify a JSON file.")


@click.command()
def version():
    """Display the version number"""
    click.echo(f"protium version {__version__}")


cli.add_command(list)
cli.add_command(create)
cli.add_command(version)

if __name__ == "__main__":
    cli()
