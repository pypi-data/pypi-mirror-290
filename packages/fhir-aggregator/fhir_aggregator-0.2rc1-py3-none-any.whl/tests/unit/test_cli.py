from click.testing import CliRunner

from fhir_aggregator.cli import cli


commands = {
    'credentials': ['add', 'delete', 'get', 'list', 'update'],
    'metrics': ['create'],
    'normalize': ['results'],
    'search': ['query'],
    'servers': ['list'],
}


def test_all():
    """Simple test of all commands and subcommands"""
    runner = CliRunner()
    for command_name in commands:
        result = runner.invoke(cli, [command_name, '--help'])
        assert result.exit_code == 0, f'Error: {command_name}'
        for subcommand in commands[command_name]:
            result = runner.invoke(cli, [command_name, subcommand, '--help'])
            assert result.exit_code == 0, f'Error: {command_name} {subcommand}'
