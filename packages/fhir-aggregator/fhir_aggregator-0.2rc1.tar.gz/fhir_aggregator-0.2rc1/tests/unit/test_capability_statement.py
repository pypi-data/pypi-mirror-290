import json

import pytest
from pydantic import ValidationError

from fhir_aggregator.client import CapabilityStatementSummary


@pytest.fixture()
def dbgap_capability_statement(mocker):
    with open('tests/fixtures/dbgap_capability_statement.json') as fp:
        _ = json.load(fp)
    mocker.retrieve = lambda queries: _
    return mocker


@pytest.fixture()
def kf_capability_statement(mocker):
    with open('tests/fixtures/kf_capability_statement.json') as fp:
        _ = json.load(fp)
    mocker.retrieve = lambda queries: _
    return mocker


@pytest.fixture()
def gtex_capability_statement(mocker):
    with open('tests/fixtures/gtex_capability_statement.json') as fp:
        _ = json.load(fp)
    mocker.retrieve = lambda queries: _
    return mocker


def test_capability_statement_summary():
    """Test the capability statement summary, basic validation."""
    with pytest.raises(ValidationError):
        CapabilityStatementSummary(capability_statement=None)
    with pytest.raises(ValidationError):
        CapabilityStatementSummary(capability_statement={})
    with pytest.raises(ValidationError):
        CapabilityStatementSummary(capability_statement={'resourceType': 'Foo'})

    capability_statement_summary = CapabilityStatementSummary(capability_statement={'resourceType': 'CapabilityStatement'})
    assert len(capability_statement_summary.warnings) > 0


def test_dbgap_capability_statement(dbgap_capability_statement):
    """Query dbGap server."""
    capability_statement = dbgap_capability_statement.retrieve(['metadata'])
    assert capability_statement
    assert isinstance(capability_statement, dict)
    dbgap_capability_statement_summary = CapabilityStatementSummary(capability_statement=capability_statement)
    assert dbgap_capability_statement_summary.resource_types == ['Observation', 'OperationDefinition', 'Patient', 'ResearchStudy']
    assert len(dbgap_capability_statement_summary.extensions) == 0


def test_kf_capability_statement(kf_capability_statement):
    """Query kf server."""
    capability_statement = kf_capability_statement.retrieve(['metadata'])
    assert capability_statement
    assert isinstance(capability_statement, dict)
    kf_capability_statement_summary = CapabilityStatementSummary(capability_statement=capability_statement)
    print(kf_capability_statement_summary.resource_types)
    assert kf_capability_statement_summary.resource_types == ['Account', 'ActivityDefinition', 'AdverseEvent',
                                                              'AllergyIntolerance', 'Appointment',
                                                              'AppointmentResponse', 'AuditEvent', 'Basic', 'Binary',
                                                              'BiologicallyDerivedProduct', 'BodyStructure', 'Bundle',
                                                              'CapabilityStatement', 'CarePlan', 'CareTeam',
                                                              'CatalogEntry', 'ChargeItem', 'ChargeItemDefinition',
                                                              'Claim', 'ClaimResponse', 'ClinicalImpression',
                                                              'CodeSystem', 'Communication', 'CommunicationRequest',
                                                              'CompartmentDefinition', 'Composition', 'ConceptMap',
                                                              'Condition', 'Consent', 'Contract', 'Coverage',
                                                              'CoverageEligibilityRequest',
                                                              'CoverageEligibilityResponse', 'DetectedIssue', 'Device',
                                                              'DeviceDefinition', 'DeviceMetric', 'DeviceRequest',
                                                              'DeviceUseStatement', 'DiagnosticReport',
                                                              'DocumentManifest', 'DocumentReference',
                                                              'EffectEvidenceSynthesis', 'Encounter', 'Endpoint',
                                                              'EnrollmentRequest', 'EnrollmentResponse',
                                                              'EpisodeOfCare', 'EventDefinition', 'Evidence',
                                                              'EvidenceVariable', 'ExampleScenario',
                                                              'ExplanationOfBenefit', 'FamilyMemberHistory', 'Flag',
                                                              'Goal', 'GraphDefinition', 'Group', 'GuidanceResponse',
                                                              'HealthcareService', 'ImagingStudy', 'Immunization',
                                                              'ImmunizationEvaluation', 'ImmunizationRecommendation',
                                                              'ImplementationGuide', 'InsurancePlan', 'Invoice',
                                                              'Library', 'Linkage', 'List', 'Location', 'Measure',
                                                              'MeasureReport', 'Media', 'Medication',
                                                              'MedicationAdministration', 'MedicationDispense',
                                                              'MedicationKnowledge', 'MedicationRequest',
                                                              'MedicationStatement', 'MedicinalProduct',
                                                              'MedicinalProductAuthorization',
                                                              'MedicinalProductContraindication',
                                                              'MedicinalProductIndication',
                                                              'MedicinalProductIngredient',
                                                              'MedicinalProductInteraction',
                                                              'MedicinalProductManufactured',
                                                              'MedicinalProductPackaged',
                                                              'MedicinalProductPharmaceutical',
                                                              'MedicinalProductUndesirableEffect', 'MessageDefinition',
                                                              'MessageHeader', 'MolecularSequence', 'NamingSystem',
                                                              'NutritionOrder', 'Observation', 'ObservationDefinition',
                                                              'OperationDefinition', 'OperationOutcome', 'Organization',
                                                              'OrganizationAffiliation', 'Parameters', 'Patient',
                                                              'PaymentNotice', 'PaymentReconciliation', 'Person',
                                                              'PlanDefinition', 'Practitioner', 'PractitionerRole',
                                                              'Procedure', 'Provenance', 'Questionnaire',
                                                              'QuestionnaireResponse', 'RelatedPerson', 'RequestGroup',
                                                              'ResearchDefinition', 'ResearchElementDefinition',
                                                              'ResearchStudy', 'ResearchSubject', 'RiskAssessment',
                                                              'RiskEvidenceSynthesis', 'Schedule', 'SearchParameter',
                                                              'ServiceRequest', 'Slot', 'Specimen',
                                                              'SpecimenDefinition', 'StructureDefinition',
                                                              'StructureMap', 'Subscription', 'Substance',
                                                              'SubstanceNucleicAcid', 'SubstancePolymer',
                                                              'SubstanceProtein', 'SubstanceReferenceInformation',
                                                              'SubstanceSourceMaterial', 'SubstanceSpecification',
                                                              'SupplyDelivery', 'SupplyRequest', 'Task',
                                                              'TerminologyCapabilities', 'TestReport', 'TestScript',
                                                              'ValueSet', 'VerificationResult', 'VisionPrescription']
    assert len(kf_capability_statement_summary.extensions) == 0


def test_gtex_capability_statement(gtex_capability_statement):
    """Query kf server."""
    capability_statement = gtex_capability_statement.retrieve(['metadata'])
    assert capability_statement
    assert isinstance(capability_statement, dict)
    gtex_capability_statement_summary = CapabilityStatementSummary(capability_statement=capability_statement)
    print(gtex_capability_statement_summary.resource_types)
    assert gtex_capability_statement_summary.resource_types == ['Account', 'ActivityDefinition', 'AdverseEvent',
                                                                'AllergyIntolerance', 'Appointment',
                                                                'AppointmentResponse', 'AuditEvent', 'Basic', 'Binary',
                                                                'BiologicallyDerivedProduct', 'BodyStructure', 'Bundle',
                                                                'CapabilityStatement', 'CarePlan', 'CareTeam',
                                                                'CatalogEntry', 'ChargeItem', 'ChargeItemDefinition',
                                                                'Claim', 'ClaimResponse', 'ClinicalImpression',
                                                                'CodeSystem', 'Communication', 'CommunicationRequest',
                                                                'CompartmentDefinition', 'Composition', 'ConceptMap',
                                                                'Condition', 'Consent', 'Contract', 'Coverage',
                                                                'CoverageEligibilityRequest',
                                                                'CoverageEligibilityResponse', 'DetectedIssue',
                                                                'Device', 'DeviceDefinition', 'DeviceMetric',
                                                                'DeviceRequest', 'DeviceUseStatement',
                                                                'DiagnosticReport', 'DocumentManifest',
                                                                'DocumentReference', 'DomainResource',
                                                                'EffectEvidenceSynthesis', 'Encounter', 'Endpoint',
                                                                'EnrollmentRequest', 'EnrollmentResponse',
                                                                'EpisodeOfCare', 'EventDefinition', 'Evidence',
                                                                'EvidenceVariable', 'ExampleScenario',
                                                                'ExplanationOfBenefit', 'FamilyMemberHistory', 'Flag',
                                                                'Goal', 'GraphDefinition', 'Group', 'GuidanceResponse',
                                                                'HealthcareService', 'ImagingStudy', 'Immunization',
                                                                'ImmunizationEvaluation', 'ImmunizationRecommendation',
                                                                'ImplementationGuide', 'InsurancePlan', 'Invoice',
                                                                'Library', 'Linkage', 'List', 'Location', 'Measure',
                                                                'MeasureReport', 'Media', 'Medication',
                                                                'MedicationAdministration', 'MedicationDispense',
                                                                'MedicationKnowledge', 'MedicationRequest',
                                                                'MedicationStatement', 'MedicinalProduct',
                                                                'MedicinalProductAuthorization',
                                                                'MedicinalProductContraindication',
                                                                'MedicinalProductIndication',
                                                                'MedicinalProductIngredient',
                                                                'MedicinalProductInteraction',
                                                                'MedicinalProductManufactured',
                                                                'MedicinalProductPackaged',
                                                                'MedicinalProductPharmaceutical',
                                                                'MedicinalProductUndesirableEffect',
                                                                'MessageDefinition', 'MessageHeader',
                                                                'MolecularSequence', 'NamingSystem', 'NutritionOrder',
                                                                'Observation', 'ObservationDefinition',
                                                                'OperationDefinition', 'OperationOutcome',
                                                                'Organization', 'OrganizationAffiliation', 'Parameters',
                                                                'Patient', 'PaymentNotice', 'PaymentReconciliation',
                                                                'Person', 'PlanDefinition', 'Practitioner',
                                                                'PractitionerRole', 'Procedure', 'Provenance',
                                                                'Questionnaire', 'QuestionnaireResponse',
                                                                'RelatedPerson', 'RequestGroup', 'ResearchDefinition',
                                                                'ResearchElementDefinition', 'ResearchStudy',
                                                                'ResearchSubject', 'Resource', 'RiskAssessment',
                                                                'RiskEvidenceSynthesis', 'Schedule', 'SearchParameter',
                                                                'ServiceRequest', 'Slot', 'Specimen',
                                                                'SpecimenDefinition', 'StructureDefinition',
                                                                'StructureMap', 'Subscription', 'Substance',
                                                                'SubstanceNucleicAcid', 'SubstancePolymer',
                                                                'SubstanceProtein', 'SubstanceReferenceInformation',
                                                                'SubstanceSourceMaterial', 'SubstanceSpecification',
                                                                'SupplyDelivery', 'SupplyRequest', 'Task',
                                                                'TerminologyCapabilities', 'TestReport', 'TestScript',
                                                                'ValueSet', 'VerificationResult', 'VisionPrescription']
    assert len(gtex_capability_statement_summary.extensions) == 0
