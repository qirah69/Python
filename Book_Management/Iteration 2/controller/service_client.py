from repo.repo_client import RepoClient
from domain.domain import Client
class ServiceClient:
    def __init__(self, repo: RepoClient):
        self._repo = repo

    def __validate(self, client):
        if not isinstance(client, Client):
            raise TypeError("The provided value is not a Client instance.")
        if client.id < 0:
            raise ValueError("Client ID must be non-negative.")
        if not client.name:
            raise ValueError("Client name cannot be empty.")

    def add_client(self, client):
        self.__validate(client)
        self._repo.add_client(client)

    def get_all_clients(self):
        return self._repo.get_all_clients()

    def remove_client(self, client_id):
        if not isinstance(client_id, int):
            raise TypeError("Client ID must be an integer.")
        if client_id < 0:
            raise ValueError("Client ID must be non-negative.")
        self._repo.remove_client(client_id)

    def update_client(self, client):
        self.__validate(client)
        self._repo.update_client(client)

    def search_by_name(self, name_query):
        if not isinstance(name_query, str):
            raise TypeError("Name query must be a string.")
        return self._repo.search_by_name(name_query)