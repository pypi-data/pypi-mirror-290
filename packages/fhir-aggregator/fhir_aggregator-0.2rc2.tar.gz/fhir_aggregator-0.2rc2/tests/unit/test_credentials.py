import pytest

from fhir_aggregator import Credential


def test_credential_no_endpoint():
    """Ensure endpoint checked."""
    with pytest.raises(ValueError):
        Credential(endpoint=None, token='token', username='username', password='password')
    Credential(endpoint="endpoint", token='token', username='username', password='password')


def test_credential_no_creds():
    """Ensure creds checked."""
    with pytest.raises(ValueError):
        Credential(endpoint="endpoint",)
    Credential(endpoint="endpoint", token="token")
    Credential(endpoint="endpoint",  username='username', password='password')