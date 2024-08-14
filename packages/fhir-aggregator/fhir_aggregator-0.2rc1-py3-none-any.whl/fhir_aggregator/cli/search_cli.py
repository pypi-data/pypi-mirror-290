import click
import yaml

from fhir_aggregator import search_all_servers
from fhir_aggregator.cli.click_util import NaturalOrderGroup


@click.group(name='search', cls=NaturalOrderGroup)
def cli():
    """Search commands."""
    pass


@cli.command()
@click.argument('yaml_file', type=click.Path(exists=True))
def query(yaml_file):
    """
    Reads a YAML file of queries and searches all servers.

    :param yaml_file: Path to the YAML file containing the queries.
    """
    with open(yaml_file, 'r') as file:
        queries = yaml.safe_load(file)

    # Assuming queries is a list of query strings
    for _ in queries:
        results = search_all_servers(_)
        # Process or display the results
        click.echo(f'Results for query "{_}": {results}')


