from fhir_aggregator.client import FHIRClient
from fhir_aggregator.client.smart_auth import GoogleFHIRAuth, DBGapFHIRAuth

# set up servers for testing
SERVERS = {}

project = 'ncpi-fhir-cat-2022/locations/us-central1/datasets/GTEx_Open_Access/fhirStores/gtex_v8.2/fhir/'
settings = {
    'app_id': 'gtex',
    'api_bases': [
        'https://healthcare.googleapis.com/v1/projects/' + project,
    ]
}

SERVERS['gtex'] = FHIRClient(settings=settings, auth=GoogleFHIRAuth())

"""Connect to open Kids First fhir server, with several datasets"""
settings = {
    'app_id': 'kf',
    'api_bases': [
        'https://kf-api-fhir-service.kidsfirstdrc.org/',
    ]
}

SERVERS['kf'] = FHIRClient(settings=settings)

settings = {
    'app_id': 'dbgap',
    'api_bases': [
        'https://dbgap-api.ncbi.nlm.nih.gov/fhir/x1',
    ]
}

SERVERS['dbgap'] = FHIRClient(settings=settings, auth=DBGapFHIRAuth(path='tests/fixtures/dbgap-task-specific-token.txt'))
