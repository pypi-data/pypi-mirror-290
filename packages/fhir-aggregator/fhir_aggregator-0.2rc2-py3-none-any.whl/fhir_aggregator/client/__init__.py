import itertools
import logging
from abc import abstractmethod
from typing import Callable, Optional, Generator

import inflection
import urllib3.util
from fhirclient import client
from pydantic import BaseModel, model_validator, computed_field
from functional import seq

logger = logging.getLogger(__name__)


LOGGED_ALREADY = set()

def NULL_LAMBDA(*args): None  # noqa


TO_ITERATOR = lambda responses: seq(itertools.chain.from_iterable(responses))  # noqa


class FHIRClient(client.FHIRClient):
    """Instances of this class handle authorizing and talking to FHIR Service.

    Parameters:
        See https://github.com/smart-on-fhir/client-py/blob/master/fhirclient/client.py#L19

    Returns:
        Instance of client, with injected authorization method

    Examples: ::
        from fhir_aggregator.client import FHIRClient
        settings = {
            'app_id': 'my_web_app',
            'api_base': 'https://healthcare.googleapis.com/v1/projects/gcp-testing-308520/locations/us-east4/datasets/testset/fhirStores/fhirstore/fhir'
        }

    """

    def __init__(self, *args, **kwargs):
        """Pass args to super, add authenticator, prepares connection."""
        # grab auth if passed
        auth = None
        if 'auth' in kwargs:
            auth = kwargs['auth']
            del kwargs['auth']

        _settings = kwargs['settings']
        api_base = _settings['api_bases'].pop()
        _settings['api_base'] = api_base

        super(FHIRClient, self).__init__(*args, **kwargs)
        client_major_version = int(client.__version__.split('.')[0])
        assert client_major_version >= 4, f"requires version >= 4.0.0 current version {client.__version__} `pip install -e git+https://github.com/smart-on-fhir/client-py#egg=fhirclient`"
        if auth:
            logger.debug("Setting auth")
            self.server.auth = auth
            self.server.session.hooks['response'].append(self.server.auth.handle_401)
        self.prepare()
        assert self.ready, "server should be ready"

    @staticmethod
    def entries(responses: list, callback: Callable = NULL_LAMBDA) -> Generator[dict, None, None]:
        """Return all resources in a response, by iterating over Bundle.entry."""
        if not isinstance(responses, list):
            responses = [responses]
        for response in responses:
            if response.get('resourceType', '') == 'Bundle' and response.get('total', None) == 0:
                continue
            if 'entry' not in response:
                callback(response)
                yield response
            for _ in response.get('entry', []):
                callback(_['resource'])
                yield _['resource']

    def pages(self, path, callback: Callable = NULL_LAMBDA, fetch_all: bool = True) -> Generator[dict, None, None]:
        """Get all pages of a resource"""
        response = self.server.request_json(path=path)
        yield from self.entries(response)
        while 'link' in response and fetch_all:
            _next = next((lnk for lnk in response['link'] if lnk['relation'] == 'next'), None)
            if not _next:
                break
            next_link = _next['url'].replace(self.server.base_uri, '')
            if 'localhost' in next_link:
                msg = "replacing localhost in next_link"
                if msg not in LOGGED_ALREADY:
                    logger.warning(f"replacing localhost in next_link: {next_link}")
                    LOGGED_ALREADY.add(msg)

                parsed_url = urllib3.util.parse_url(next_link)
                path = parsed_url.path
                query = parsed_url.query
                if query:
                    next_link = f"{path}?{query}"
                else:
                    next_link = path

            # print('NEXT LINK', next_link)
            callback(next_link)
            response = self.server.request_json(path=next_link)
            yield from self.entries(response)

    def retrieve(self, queries, callback: Callable = NULL_LAMBDA, chain: Callable = TO_ITERATOR, fetch_all: bool = True):
        """Query server with queries, internally creates a list of generators, default chain will return an iterator."""
        if not isinstance(queries, list):
            queries = [queries]
        responses = [self.pages(path=_, callback=callback, fetch_all=fetch_all) for _ in queries]
        # return [_ for _ in chain(responses)]
        yield from chain(responses)


class ResourceSummary(BaseModel):
    """All summaries should inherit from this class."""
    warnings: list[str] = []

    @computed_field()
    @property
    def simplified(self) -> dict:
        _ = {'identifier': self.identifier.get('value', None)}
        _.update(self.scalars)
        _.update(self.codings)
        _.update(self.extensions)
        return _

    def simplify_extensions(self, resource: dict = None, _extensions: dict = None) -> dict:
        """Extract extension values, derive key from extension url"""

        def _populate_simplified_extension(_):
            # simple extension
            value_normalized, extension_key = normalize_value(_)
            extension_key = _['url'].split('/')[-1]
            extension_key = inflection.underscore(extension_key).removesuffix(".json").removeprefix("structure_definition_")
            assert value_normalized is not None, f"extension: {extension_key} = {value_normalized} {_}"
            _extensions[extension_key] = value_normalized

        if not _extensions:
            _extensions = {}

        if not resource:
            resource = self.resource_dict

        for _ in resource.get('extension', [resource]):
            if 'extension' not in _.keys():
                if 'resourceType' not in _.keys():
                    _populate_simplified_extension(_)
                continue
            elif set(_.keys()) == set(['url', 'extension']):
                for child_extension in _['extension']:
                    self.simplify_extensions(resource=child_extension, _extensions=_extensions)

        return _extensions

    @property
    @abstractmethod
    def resource_dict(self) -> dict:
        """subclasses should override: Return the resource dictionary."""
        pass

    @computed_field
    @property
    def extensions(self) -> dict:
        return self.simplify_extensions()

    @computed_field
    @property
    def scalars(self) -> dict:
        """Return a dictionary of scalar values."""
        return {k: v for k, v in self.resource_dict.items() if (not isinstance(v, list) and not isinstance(v, dict))}

    @computed_field
    @property
    def codings(self) -> dict:
        """Return a dictionary of scalar values."""
        _codings = {}
        for k, v in self.resource_dict.items():
            if k in ['identifier', 'extension']:
                continue
            if isinstance(v, list):
                for _ in v:
                    if isinstance(_, dict):
                        for value, source in normalize_coding(_):
                            _codings[k] = value
            elif isinstance(v, dict):
                for value, source in normalize_coding(v):
                    _codings[k] = value
        return _codings

    @property
    def identifier(self) -> str:
        """Return the official identifier, or first of a resource."""
        identifiers = self.resource_dict.get('identifier', [])
        official_identifiers = [_ for _ in identifiers if _.get('use', '') == 'official']
        if not official_identifiers and identifiers:
            return identifiers[0]
        elif official_identifiers:
            return official_identifiers[0]
        else:
            return {}


class CapabilityStatementSummary(ResourceSummary):
    """Summarize a capability statement."""
    capability_statement: dict
    _resource_types: list[str] = []

    @property
    def resource_dict(self) -> dict:
        return self.capability_statement

    @model_validator(mode='before')
    def set_summary_fields(cls, values):
        capability_statement = values.get('capability_statement')

        assert capability_statement, f"Expected capability_statement, got {capability_statement}"
        assert isinstance(capability_statement, dict), f"Expected dict, got {type(capability_statement)}"
        assert 'resourceType' in capability_statement, f"Expected resourceType in {capability_statement}"
        assert capability_statement['resourceType'] == 'CapabilityStatement', f"Expected CapabilityStatement, got {capability_statement['resourceType']}"

        if 'rest' not in capability_statement:
            values['warnings'] = []
            values['warnings'].append(f"CapabilityStatement has no rest")
        return values

    @property
    def resource_types(self) -> list[str]:
        resource_types = []
        capability_statement = self.capability_statement
        if not self._resource_types:
            if 'rest' not in capability_statement:
                logger.warning(f"CapabilityStatement has no rest: {capability_statement}")
            else:
                for rest in capability_statement['rest']:
                    if 'resource' not in rest:
                        logger.warning(f"Rest has no resource: {rest}")
                    else:
                        for resource in rest['resource']:
                            resource_types.append(resource['type'])
            self._resource_types = sorted(resource_types)
        return self._resource_types

    @property
    def everything(self) -> list[str]:
        assert self.capability_statement, f"Expected capability_statement, got {self.capability_statement}"
        assert 'rest' in self.capability_statement, f"Expected rest in {self.capability_statement}"
        for rest in self.capability_statement['rest']:
            assert 'operation' in rest, f"Expected operation in {rest}"
            for operation in rest['operation']:
                _name = operation['name']


class ResearchStudySummary(ResourceSummary):
    """Summarize a research study."""

    research_study: dict

    @computed_field
    @property
    def resource_dict(self) -> dict:
        return self.research_study


class OperationDefinitionSummary(ResourceSummary):
    """Summarize an operation definition."""

    operation_definition: list[dict]

    @property
    def resource_dict(self) -> dict:
        return self.operation_definition[0]

    @property
    def everything(self) -> list[str]:
        """Resources that have an $everything operation."""
        resources = []
        for _ in self.operation_definition:
            if _['code'] != 'everything':
                continue
            resources.extend(_['resource'])
        return sorted(resources)


def normalize_value(resource_dict: dict) -> tuple[Optional[str], Optional[str]]:
    """return a tuple containing the normalized value and the name of the field it was derived from"""
    value_normalized = None
    value_source = None

    if 'valueQuantity' in resource_dict:
        value = resource_dict['valueQuantity']
        value_normalized = f"{value['value']} {value.get('unit', '')}"
        value_source = 'valueQuantity'
    elif 'valueCodeableConcept' in resource_dict:
        value = resource_dict['valueCodeableConcept']
        value_normalized = ' '.join([coding.get('display', coding.get('code', '')) for coding in value.get('coding', [])])
        value_source = 'valueCodeableConcept'
    elif 'valueCoding' in resource_dict:
        value = resource_dict['valueCoding']
        value_normalized = value['display']
        value_source = 'valueCoding'
    elif 'valueString' in resource_dict:
        value_normalized = resource_dict['valueString']
        value_source = 'valueString'
    elif 'valueCode' in resource_dict:
        value_normalized = resource_dict['valueCode']
        value_source = 'valueCode'
    elif 'valueBoolean' in resource_dict:
        value_normalized = str(resource_dict['valueBoolean'])
        value_source = 'valueBoolean'
    elif 'valueInteger' in resource_dict:
        value_normalized = str(resource_dict['valueInteger'])
        value_source = 'valueInteger'
    elif 'valueRange' in resource_dict:
        value = resource_dict['valueRange']
        low = value['low']
        high = value['high']
        value_normalized = f"{low['value']} - {high['value']} {low.get('unit', '')}"
        value_source = 'valueRange'
    elif 'valueRatio' in resource_dict:
        value = resource_dict['valueRatio']
        numerator = value['numerator']
        denominator = value['denominator']
        value_normalized = f"{numerator['value']} {numerator.get('unit', '')}/{denominator['value']} {denominator.get('unit', '')}"
        value_source = 'valueRatio'
    elif 'valueSampledData' in resource_dict:
        value = resource_dict['valueSampledData']
        value_normalized = value['data']
        value_source = 'valueSampledData'
    elif 'valueTime' in resource_dict:
        value_normalized = resource_dict['valueTime']
        value_source = 'valueTime'
    elif 'valueDateTime' in resource_dict:
        value_normalized = resource_dict['valueDateTime']
        value_source = 'valueDateTime'
    elif 'valuePeriod' in resource_dict:
        value = resource_dict['valuePeriod']
        value_normalized = f"{value['start']} to {value['end']}"
        value_source = 'valuePeriod'
    elif 'valueUrl' in resource_dict:
        value_normalized = resource_dict['valueUrl']
        value_source = 'valueUrl'
    elif 'valueDate' in resource_dict:
        value_normalized = resource_dict['valueDate']
        value_source = 'valueDate'
    elif 'valueCount' in resource_dict:
        value_normalized = resource_dict['valueCount']['value']
        value_source = 'valueCount'
    # for debugging...
    else:
        raise ValueError(f"value[x] not found in {resource_dict}")

    return value_normalized, value_source


def normalize_coding(resource_dict: dict) -> list[tuple[str, str]]:
    def extract_coding(coding_list):
        # return a concatenated string
        # return ','.join([coding.get('display', '') for coding in coding_list if 'display' in coding])
        # or alternatively return an array
        return [coding.get('display', coding.get('code', '')) for coding in coding_list]

    def find_codings_in_dict(d: dict, parent_key: str = '') -> list[tuple[str, str]]:
        codings = []
        for key, value in d.items():
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        # Check if the dict contains a 'coding' list
                        if 'coding' in item and isinstance(item['coding'], list):
                            coding_string = extract_coding(item['coding'])
                            codings.append((coding_string, key))
                        if 'code' in item:
                            # print(f">>> DBG value: {item} {key} {parent_key}")
                            coding_string = item['code']
                            codings.append((coding_string, key))

                        # Recursively search in the dict
                        codings.extend(find_codings_in_dict(item, key))
            elif isinstance(value, dict):
                # Check if the dict contains a 'coding' list
                if 'coding' in value and isinstance(value['coding'], list):
                    coding_string = extract_coding(value['coding'])
                    codings.append((coding_string, key))

                # Recursively search in the dict
                codings.extend(find_codings_in_dict(value, key))
        return codings

    return find_codings_in_dict(resource_dict)


def is_number(s):
    """ Returns True if string is a number. """
    try:
        complex(s)
        return True
    except ValueError:
        return False


