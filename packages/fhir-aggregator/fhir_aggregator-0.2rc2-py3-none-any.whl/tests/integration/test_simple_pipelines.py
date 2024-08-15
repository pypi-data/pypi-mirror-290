import itertools
from collections import Counter

from functional import seq


def identifier(resource):
    """Return the official identifier, or first of a resource."""
    identifiers = resource.get('identifier', [])
    official_identifiers = [_ for _ in identifiers if _.get('use', '') == 'official']
    if not official_identifiers and identifiers:
        return identifiers[0]
    elif official_identifiers:
        return official_identifiers[0]
    else:
        return {}


def retrieve_and_process(server, queries):
    """Query server with queries, collect responses and run through two pipelines."""
    copy1, copy2 = server.retrieve(queries, chain=lambda responses: itertools.tee(itertools.chain.from_iterable(responses), 2))

    items_with_identifiers = seq(copy1).map(lambda _: (_['resourceType'], identifier(_).get('value', None))).filter(lambda _: _[1]).to_list()
    items_without_identifiers = seq(copy2).map(lambda _: (_['resourceType'], identifier(_).get('value', None))).filter(lambda _: not _[1]).to_list()

    return items_with_identifiers, items_without_identifiers


def test_gtex_pipeline(gtex, queries):
    """Query gtex server process using our chain ."""
    items_with_identifiers, items_without_identifiers = retrieve_and_process(gtex, queries)

    assert len(items_with_identifiers) == 1
    assert len(items_without_identifiers) == 1

    assert items_with_identifiers[0][0] == 'ResearchStudy'
    assert items_without_identifiers[0][0] == 'CapabilityStatement'


def test_kf_pipeline(kf, queries):
    """Query KF server,  process using our chain"""
    items_with_identifiers, items_without_identifiers = retrieve_and_process(kf, queries)

    assert len(items_with_identifiers) == 45
    assert len(items_without_identifiers) == 1

    assert items_with_identifiers[0][0] == 'ResearchStudy'
    assert items_without_identifiers[0][0] == 'CapabilityStatement'


def test_dbgap_all_studies(dbgap, queries):
    """Query dbGap server, process using our chain"""
    items_with_identifiers, items_without_identifiers = retrieve_and_process(dbgap, queries)

    assert len(items_with_identifiers) == 2773
    assert len(items_without_identifiers) == 1

    assert items_with_identifiers[0][0] == 'ResearchStudy'
    assert items_without_identifiers[0][0] == 'CapabilityStatement'


def test_dbgap_public_studies(dbgap):
    responses = dbgap.retrieve('ResearchStudy?_security=public,unrestricted&_count=1000')
    counter = Counter([_['resourceType'] for _ in responses])
    print(counter)
    assert counter == {'ResearchStudy': 1893}


def test_dbgap_patient(dbgap):
    # works phs002409
    # does not work phs000635 phs000571 phs001988
    research_study_identifier = 'phs002409'
    # responses = dbgap.retrieve('ResearchSubject?study=' + research_study_identifier)
    responses = dbgap.retrieve(f'Patient?_count=1000&_has:ResearchSubject:individual:study={research_study_identifier}&_revinclude=ResearchSubject:individual')
    counter = Counter([_['resourceType'] for _ in responses])
    print(counter)
    assert counter == {'ResearchSubject': 2, 'Patient': 1}


def test_kf_patient(kf):
    """https://kf-api-fhir-service.kidsfirstdrc.org/Patient?_has:ResearchSubject:individual:study=1883519&_revinclude=Specimen:subject"""
    research_study_identifier = '1883519'
    responses = kf.retrieve(f'Patient?_count=1000&_has:ResearchSubject:individual:study={research_study_identifier}&_revinclude=Specimen:subject&_revinclude=DocumentReference:subject&_revinclude=Condition:subject&_revinclude=MedicationAdministration:subject&_revinclude=Observation:subject&_revinclude=QuestionnaireResponse:subject&_revinclude=MedicationStatement:subject&_revinclude=MedicationDispense:subject')
    counter = Counter([_['resourceType'] for _ in responses])
    print(counter)
    assert counter == {'DocumentReference': 4232, 'Condition': 4109, 'Specimen': 1534, 'Observation': 1199, 'Patient': 753}

