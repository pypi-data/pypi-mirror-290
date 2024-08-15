import pytest

from tests.integration import SERVERS


@pytest.fixture()
def gtex():
    return SERVERS['gtex']


@pytest.fixture()
def dbgap():
    return SERVERS['dbgap']


@pytest.fixture()
def kf():
    return SERVERS['kf']


@pytest.fixture()
def queries():
    """Queries to run on FHIR servers."""
    return [
        'metadata',
        'ResearchStudy?_count=1000',
    ]
