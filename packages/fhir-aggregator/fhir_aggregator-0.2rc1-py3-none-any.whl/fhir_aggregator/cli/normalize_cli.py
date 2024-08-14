import json

import click

from fhir_aggregator import normalize
from fhir_aggregator.cli.click_util import NaturalOrderGroup


@click.group(name='normalize', cls=NaturalOrderGroup)
def cli():
    """Normalization  commands."""
    pass


@cli.command()
@click.argument('results_file', type=click.Path(exists=True))
def results(results_file):
    """
    Normalizes search results stored in a file.

    :param results_file: Path to the file containing raw search results.
    """
    with open(results_file, 'r') as file:
        search_results = json.load(file)

    # normalize is a function that normalizes the search results
    normalized_results = normalize(search_results)

    # For demonstration, let's just print the normalized results
    # In practice, you might save this back to a file or database
    click.echo(json.dumps(normalized_results, indent=4))
