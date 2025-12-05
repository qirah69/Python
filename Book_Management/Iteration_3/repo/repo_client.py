class RepoClient:
    def __init__(self):
        """
        Initialize an empty RepoClient repository using a dictionary.
        """
        self._clients = {}

    def add_client(self, client):
        """
        Add a new client to the repository.
        
        Args:
            client: The Client object to add
            
        Raises:
            ValueError: If a client with the same ID already exists
        """
        if client.id in self._clients:
            raise ValueError(f"Client with ID {client.id} already exists.")
        self._clients[client.id] = client

    def get_all_clients(self):
        """
        Retrieve all clients from the repository.
        
        Returns:
            list: A list of all Client objects
        """
        return list(self._clients.values())

    def remove_client(self, client_id):
        """
        Remove a client from the repository by ID.
        
        Args:
            client_id: The ID of the client to remove
            
        Raises:
            ValueError: If the client does not exist
        """
        if client_id not in self._clients:
            raise ValueError(f"Client with ID {client_id} does not exist.")
        del self._clients[client_id]

    def update_client(self, client):
        """
        Update an existing client in the repository.
        
        Args:
            client: The Client object with updated information
            
        Raises:
            ValueError: If the client does not exist
        """
        if client.id not in self._clients:
            raise ValueError(f"Client with ID {client.id} does not exist.")
        self._clients[client.id] = client

    def search_by_name(self, name_query):
        """
        Search for clients by name (case-insensitive partial match).
        
        Args:
            name_query: The name or partial name to search for
            
        Returns:
            list: A list of Client objects matching the query
        """
        return [client for client in self._clients.values() if name_query.lower() in client.name.lower()]
    
    def find_client_by_id(self, client_id):
        """
        Find a client by their ID.
        
        Args:
            client_id: The ID of the client to find
            
        Returns:
            Client: The Client object if found, None otherwise
        """
        return self._clients.get(client_id, None)