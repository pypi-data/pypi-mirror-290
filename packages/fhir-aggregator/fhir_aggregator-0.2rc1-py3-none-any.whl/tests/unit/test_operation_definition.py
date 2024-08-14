import json

import pytest
from pydantic import ValidationError

from fhir_aggregator.client import CapabilityStatementSummary, OperationDefinitionSummary


@pytest.fixture()
def dbgap_operation_definition(mocker):
    with open('tests/fixtures/dbgap_operation_definition.json') as fp:
        _ = json.load(fp)
    mocker.retrieve = lambda queries: _
    return mocker


@pytest.fixture()
def kf_operation_definition(mocker):
    with open('tests/fixtures/kf_operation_definition.json') as fp:
        _ = json.load(fp)
    mocker.retrieve = lambda queries: _
    return mocker


@pytest.fixture()
def gtex_operation_definition(mocker):
    with open('tests/fixtures/gtex_operation_definition.json') as fp:
        _ = json.load(fp)
    mocker.retrieve = lambda queries: _
    return mocker


def test_dbgap_operation_definition(dbgap_operation_definition):
    """Query dbGap server."""
    #  Note dbgap does not return OperationDefinition
    operation_definition = dbgap_operation_definition.retrieve(['OperationDefinition?_count=1000'])
    assert isinstance(operation_definition, list)
    operation_definition_summary = OperationDefinitionSummary(operation_definition=operation_definition)
    assert operation_definition_summary.everything == []


def test_kf_operation_definition(kf_operation_definition):
    """Query kf server."""
    operation_definition = kf_operation_definition.retrieve(['OperationDefinition?_count=1000'])
    assert operation_definition
    assert isinstance(operation_definition, list)
    operation_definition_summary = OperationDefinitionSummary(operation_definition=operation_definition)
    assert operation_definition_summary
    print(operation_definition_summary.everything)
    assert operation_definition_summary.everything == ['Encounter', 'Group', 'MedicinalProduct', 'Patient']


def test_gtex_operation_definition(gtex_operation_definition):
    """Query gtex server."""
    #  Note gtex does not return OperationDefinition
    operation_definition = gtex_operation_definition.retrieve(['OperationDefinition?_count=1000'])
    assert isinstance(operation_definition, list)
    operation_definition_summary = OperationDefinitionSummary(operation_definition=operation_definition)
    assert operation_definition_summary.everything == []
