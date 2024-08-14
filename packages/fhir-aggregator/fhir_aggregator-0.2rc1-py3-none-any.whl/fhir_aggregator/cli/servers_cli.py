import click

from fhir_aggregator import list_all_servers
from fhir_aggregator.cli.click_util import NaturalOrderGroup


@click.group(name='servers', cls=NaturalOrderGroup)
def cli():
    """Server commands."""
    pass


@cli.command(name='list')
def _list():
    """
    Lists all known servers.
    """
    results = list_all_servers()
    # Process or display the results
    click.echo(f'Servers: {results}')


