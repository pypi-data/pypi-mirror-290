import os
from collections import OrderedDict

import click
import yaml
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Credential:
    """
    Represents credentials for accessing a service.

    Attributes:
        endpoint (str): The service endpoint URL. Required.
        token (str): Authentication token. Optional.
        username (str): Username for authentication. Optional.
        password (str): Password for authentication. Optional.
    """
    endpoint: str
    token: str = field(default=None)
    username: str = field(default=None)
    password: str = field(default=None)

    def validate(self):
        """
        Validates the Credential instance to ensure it meets the requirements.

        Raises:
            ValueError: If the endpoint is None or an empty string, or if both token and username/password are not provided.
        """
        if not self.endpoint:
            raise ValueError("Endpoint is required.")
        if not self.token and (not self.username or not self.password):
            raise ValueError("Either token or both username and password must be provided.")

    def __post_init__(self):
        """
        When defined on the class, it will be called by the generated __init__()
        """
        self.validate()


class CredentialManager:
    """
    Manages credentials stored in a YAML file, allowing CRUD operations.

    Attributes:
        credentials_file (Path): Path to the YAML file storing credentials.
        credentials (dict): Loaded credentials from the YAML file.
    """

    def __init__(self):
        """
        Initializes the CredentialManager, loading or creating the credentials file.
        """
        self.credentials_file = Path.home() / '.fhir_aggregator/credentials.yaml'
        self.credentials_file.parent.mkdir(parents=True, exist_ok=True)
        self.credentials = self._load_credentials()

    def _load_credentials(self):
        """
        Loads credentials from the YAML file, or initializes an empty dictionary if the file does not exist.

        Returns:
            dict: The loaded or initialized credentials.
        """
        if self.credentials_file.exists():
            with open(self.credentials_file, 'r') as file:
                return yaml.safe_load(file) or {}
        else:
            return {}

    def save_credentials(self):
        """
        Saves the current state of credentials back to the YAML file.
        """
        with open(self.credentials_file, 'w') as file:
            yaml.safe_dump(self.credentials, file)

    def add_or_update_credential(self, credential):
        """
        Adds a new credential or updates an existing one using the endpoint as the key.

        Args:
            credential (Credential): The credential to add or update.
        """
        self.credentials[credential.endpoint] = {
            'token': credential.token,
            'username': credential.username,
            'password': credential.password
        }
        self.save_credentials()

    def delete_credential(self, endpoint):
        """
        Deletes a credential by its endpoint.

        Args:
            endpoint (str): The endpoint of the credential to delete.
        """
        if endpoint in self.credentials:
            del self.credentials[endpoint]
            self.save_credentials()

    def get_credential(self, endpoint):
        """
        Retrieves a credential by its endpoint.

        Args:
            endpoint (str): The endpoint of the credential to retrieve.

        Returns:
            dict: The credential, if found; otherwise, None.
        """
        return self.credentials.get(endpoint, None)


def metrics(search_results) -> dict:
    """
    Calculate metrics from search results.
    :param search_results:
    :return:
    """
    # Placeholder for metrics calculation logic
    # This should be replaced with actual logic to calculate metrics from search_results
    return {
        'total_results': len(search_results),
        # Add more metrics calculation here
    }


def search_all_servers(query) -> dict:
    """
    Search all servers for a given query.
    :param query:
    :return: Bundle
    """
    # Placeholder for search logic
    # This function should return the search results for a given query
    return f"Search results for {query}"


def normalize(results: dict) -> dict:
    # Placeholder for normalization logic
    # This should be replaced with actual logic to normalize search_results
    return results  # Replace this with actual normalization logic


def list_all_servers() -> list[str]:
    """
    Lists all known servers.
    :return:  A list of known server urls.
    """
    # Placeholder for server list
    return []
