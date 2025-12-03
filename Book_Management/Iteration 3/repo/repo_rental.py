class RepoRental:
    def __init__(self):
        self._rentals = []

    def add_rental(self, rental):
        self._rentals.append(rental)

    def remove_rental(self, id):
        for rental in self._rentals:
            if rental.id == id:
                self._rentals.remove(rental)
                return
        raise ValueError(f"Rental with ID {id} not found.")

    def get_all_rentals(self):
        return self._rentals

    def update_rental(self, rental_id, returned_date):
        for rental in self._rentals:
            if rental.id == rental_id:
                rental.returned_date = returned_date
                return
        raise ValueError(f"Rental with ID {rental_id} not found.")
    def find_rental_by_id(self, rental_id):
        for rental in self._rentals:
            if rental.id == rental_id:
                return rental
        return None