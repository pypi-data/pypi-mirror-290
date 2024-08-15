import json

import click

from fhir_aggregator import metrics
from fhir_aggregator.cli.click_util import NaturalOrderGroup


@click.group(name='metrics', cls=NaturalOrderGroup)
def cli():
    """Metrics  commands."""
    pass


@cli.command()
@click.argument('results_file', type=click.Path(exists=True))
def create(results_file):
    """
    Creates metrics from search results stored in a file.

    :param results_file: Path to the file containing search results.
    """
    with open(results_file, 'r') as file:
        search_results = json.load(file)

    _ = metrics(search_results)

    # Display or store the metrics
    click.echo(f'Metrics: {_}')
