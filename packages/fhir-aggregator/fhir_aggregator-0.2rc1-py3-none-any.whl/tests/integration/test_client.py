import itertools
from collections import Counter
from unittest.mock import patch

import pytest
import requests
from fhirclient.server import FHIRUnauthorizedException
from functional import seq

from fhir_aggregator.client import ResearchStudySummary
from pprint import pprint


@pytest.fixture()
def unauthorized_request(mocker):
    mocker.status_code = 401
    mocker.json = lambda: {'error': 'Unauthorized'}
    return mocker


def test_unauthorized_request(dbgap, unauthorized_request):
    with pytest.raises(FHIRUnauthorizedException):
        with patch.object(requests.Session, 'get', return_value=unauthorized_request):
            responses = dbgap.retrieve(['metadata'])
            assert seq(responses).first()


def test_dbgap(dbgap):
    """Query dbGap server."""
    responses = dbgap.retrieve('ResearchStudy/phs002409')
    research_study = seq(responses).first()
    summary = ResearchStudySummary(research_study=research_study)

    print(summary.identifier)
    assert summary.identifier['value'] == 'phs002409.v1.p1'

    print(summary.extensions)
    assert summary.extensions == {
        'research_study_study_overview_url': 'https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs002409.v1.p1',
        'research_study_release_date': '2021-09-09', 'research_study_study_consents_study_consent': 'GRU',
        'research_study_content_num_phenotype_datasets': 2, 'research_study_content_num_molecular_datasets': 0,
        'research_study_content_num_variables': 58, 'research_study_content_num_documents': 0,
        'research_study_content_num_analyses': 0, 'research_study_content_num_subjects': 813,
        'research_study_content_num_samples': 0, 'research_study_content_num_sub_studies': 0}

    pprint(summary.research_study['extension'])

    responses = dbgap.retrieve('Patient?_count=1000&_has:ResearchSubject:individual:study=' + summary.research_study['id'])
    copy1, copy2 = itertools.tee(responses, 2)
    counter = Counter([_['resourceType'] for _ in copy1])
    print(counter)
    assert counter == {'Patient': 813}

    responses = dbgap.retrieve(f'Patient/{seq(copy2).first()["id"]}')
    patient = seq(responses).first()
    assert patient
    print(patient)
    assert patient['resourceType'] == 'Patient'
