from domain.domain import Rental
from repo.repo_rental import RepoRental
from repo.repo_book import RepoBook
from repo.repo_client import RepoClient

class ServiceRental:
    def __init__(self, repo_rental: RepoRental, repo_book: RepoBook, repo_client: RepoClient):
        self._repo_rental = repo_rental
        self._repo_book = repo_book
        self._repo_client = repo_client

    def get_report_book_borrowers(self, book_id):
        borrowers = []
        for rental in self._repo_rental.get_all_rentals():
            if rental.book_id == book_id:
                client = self._repo_client.find_client_by_id(rental.client_id)
                if client:
                    borrowers.append({'Client': client.name, 'Rented Date': rental.rented_date})
        borrowers.sort(key=lambda item: (item['Client'], item['Rented Date']))
        return borrowers

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
    
    def get_most_rented_books(self):
        rental_count = {}
        for rental in self._repo_rental.get_all_rentals():
            if rental.book_id not in rental_count:
                rental_count[rental.book_id] = 0
            rental_count[rental.book_id] += 1
        sorted_books = sorted(rental_count.items(), key=lambda item: item[1], reverse=True)
        sorted_books = sorted_books[:3]
        result = []
        for book_id, count in sorted_books:
            book = self._repo_book.find_book_by_id(book_id)
            if book:
                result.append((book, count))
        return result
    
    def get_most_active_clients(self):
        client_rental_count = {}
        for rental in self._repo_rental.get_all_rentals():
            if rental.client_id not in client_rental_count:
                client_rental_count[rental.client_id] = 0
            client_rental_count[rental.client_id] += 1
        sorted_clients = sorted(client_rental_count.items(), key=lambda item: item[1], reverse=True)
        top_20_percent_index = max(1, len(sorted_clients) * 20 // 100)
        sorted_clients = sorted_clients[:top_20_percent_index]
        result = []
        for client_id, count in sorted_clients:
            client = self._repo_client.find_client_by_id(client_id)
            if client:
                result.append((client, count))
        return result