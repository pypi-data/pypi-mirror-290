import click
from fhir_aggregator import CredentialManager, Credential
from fhir_aggregator.cli.click_util import NaturalOrderGroup


@click.group(name='credentials', cls=NaturalOrderGroup)
def cli():
    """Credential management commands."""
    pass


@cli.command()
@click.argument('endpoint')
@click.option('--token', default=None, help='Authentication token')
@click.option('--username', default=None, help='Username for authentication')
@click.option('--password', default=None, help='Password for authentication')
def add(endpoint, token, username, password):
    """Add a new credential."""
    manager = CredentialManager()
    credential = Credential(endpoint=endpoint, token=token, username=username, password=password)
    manager.add_or_update_credential(credential)
    click.echo(f'Credential for {endpoint} added.')


@cli.command()
@click.argument('endpoint')
def delete(endpoint):
    """Delete a credential."""
    manager = CredentialManager()
    manager.delete_credential(endpoint)
    click.echo(f'Credential for {endpoint} deleted.')


@cli.command()
@click.argument('endpoint')
def get(endpoint):
    """Get a credential."""
    manager = CredentialManager()
    credential = manager.get_credential(endpoint)
    if credential:
        click.echo(f'Credential: {credential}')
    else:
        click.echo('Credential not found.')


@cli.command(name='list')
def _list():
    """List all credentials."""
    manager = CredentialManager()
    credentials = manager.list_credentials()  # Assuming this method exists
    for endpoint, credential in credentials.items():
        click.echo(f'{endpoint}: {credential}')


@cli.command()
@click.argument('endpoint')
@click.option('--token', default=None, help='Authentication token')
@click.option('--username', default=None, help='Username for authentication')
@click.option('--password', default=None, help='Password for authentication')
def update(endpoint, token, username, password):
    """Update an existing credential."""
    manager = CredentialManager()
    credential = Credential(endpoint=endpoint, token=token, username=username, password=password)
    manager.add_or_update_credential(credential)
    click.echo(f'Credential for {endpoint} updated.')
