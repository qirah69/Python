from domain.domain import Rental
from repo.repo_rental import RepoRental
from repo.repo_book import RepoBook
from repo.repo_client import RepoClient

class ServiceRental:
    def __init__(self, repo_rental: RepoRental, repo_book: RepoBook, repo_client: RepoClient):
        self._repo_rental = repo_rental
        self._repo_book = repo_book
        self._repo_client = repo_client

    def add_rental(self, rental_id, book_id, client_id, rented_date):
        if self._repo_book.find_book_by_id(book_id) is None:
            raise ValueError(f"Book with ID {book_id} does not exist.")
        if self._repo_client.find_client_by_id(client_id) is None:
            raise ValueError(f"Client with ID {client_id} does not exist.")
        for rental in self._repo_rental.get_all_rentals():
            if rental.book_id == book_id and rental.returned_date is None :
                 raise ValueError(f"Book with ID {book_id} is already rented and not yet returned.")
        rental = Rental(rental_id, book_id, client_id, rented_date)
        self._repo_rental.add_rental(rental)

    def return_book(self, rental_id, returned_date):
        rental = self._repo_rental.find_rental_by_id(rental_id)
        if rental is None:
            raise ValueError(f"Rental with ID {rental_id} not found.")
        if rental.returned_date is not None:
            raise ValueError(f"Book for Rental ID {rental_id} has already been returned.")
        self._repo_rental.update_rental(rental_id, returned_date)

    def get_all_rentals(self):
        return self._repo_rental.get_all_rentals()