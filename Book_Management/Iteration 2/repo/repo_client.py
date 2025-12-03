class RepoClient:
    def __init__(self):
        self._clients = {}

    def add_client(self, client):
        if client.id in self._clients:
            raise ValueError(f"Client with ID {client.id} already exists.")
        self._clients[client.id] = client

    def get_all_clients(self):
        return list(self._clients.values())

    def remove_client(self, client_id):
        if client_id not in self._clients:
            raise ValueError(f"Client with ID {client_id} does not exist.")
        del self._clients[client_id]

    def update_client(self, client):
        if client.id not in self._clients:
            raise ValueError(f"Client with ID {client.id} does not exist.")
        self._clients[client.id] = client

    def search_by_name(self, name_query):
        return [client for client in self._clients.values() if name_query.lower() in client.name.lower()]