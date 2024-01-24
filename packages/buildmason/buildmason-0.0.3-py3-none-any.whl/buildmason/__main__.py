import click
from . import commands

@click.group()
def cli():
    pass

# Add more commands for other project types
cli.add_command(commands.basic_project)
cli.add_command(commands.rest_api)
cli.add_command(commands.blueprint)
