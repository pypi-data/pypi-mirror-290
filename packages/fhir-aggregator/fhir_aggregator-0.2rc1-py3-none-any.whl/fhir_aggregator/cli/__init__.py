import click

from fhir_aggregator.cli import servers_cli, credentials_cli, search_cli, metrics_cli, normalize_cli
from fhir_aggregator.cli.click_util import NaturalOrderGroup


@click.group(cls=NaturalOrderGroup)
def cli():
    """FHIR Aggregator Command Line Interface."""
    pass


# add subcommands to the cli
cli.add_command(servers_cli.cli)
cli.add_command(credentials_cli.cli)
cli.add_command(search_cli.cli)
cli.add_command(metrics_cli.cli)
cli.add_command(normalize_cli.cli)
