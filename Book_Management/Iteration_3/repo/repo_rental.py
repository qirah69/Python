class RepoRental:
    def __init__(self):
        """
        Initialize an empty RepoRental repository.
        """
        self._rentals = []

    def add_rental(self, rental):
        """
        Add a new rental to the repository.
        
        Args:
            rental: The Rental object to add
        """
        self._rentals.append(rental)

    def remove_rental(self, id):
        """
        Remove a rental from the repository by ID.
        
        Args:
            id: The ID of the rental to remove
            
        Raises:
            ValueError: If the rental with the given ID is not found
        """
        for rental in self._rentals:
            if rental.id == id:
                self._rentals.remove(rental)
                return
        raise ValueError(f"Rental with ID {id} not found.")

    def get_all_rentals(self):
        """
        Retrieve all rentals from the repository.
        
        Returns:
            list: A list of all Rental objects
        """
        return self._rentals

    def update_rental(self, rental_id, returned_date):
        """
        Update a rental's return date.
        
        Args:
            rental_id: The ID of the rental to update
            returned_date: The new return date
            
        Raises:
            ValueError: If the rental with the given ID is not found
        """
        for rental in self._rentals:
            if rental.id == rental_id:
                rental.returned_date = returned_date
                return
        raise ValueError(f"Rental with ID {rental_id} not found.")
    
    def find_rental_by_id(self, rental_id):
        """
        Find a rental by its ID.
        
        Args:
            rental_id: The ID of the rental to find
            
        Returns:
            Rental: The Rental object if found, None otherwise
        """
        for rental in self._rentals:
            if rental.id == rental_id:
                return rental
        return None