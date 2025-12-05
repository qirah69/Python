from domain.domain import Rental
from repo.repo_rental import RepoRental
from repo.repo_book import RepoBook
from repo.repo_client import RepoClient

class ServiceRental:
    def __init__(self, repo_rental: RepoRental, repo_book: RepoBook, repo_client: RepoClient):
        """
        Initialize the ServiceRental with repository instances for rentals, books, and clients.
        
        Args:
            repo_rental (RepoRental): The rental repository
            repo_book (RepoBook): The book repository
            repo_client (RepoClient): The client repository
        """
        self._repo_rental = repo_rental
        self._repo_book = repo_book
        self._repo_client = repo_client

    def get_report_book_borrowers(self, book_id):
        """
        Get a report of all clients who have borrowed a specific book, sorted by name and rental date.
        
        Args:
            book_id: The ID of the book to get borrowers for
            
        Returns:
            list: A list of dictionaries containing borrower names and rental dates
        """
        borrowers = []
        for rental in self._repo_rental.get_all_rentals():
            if rental.book_id == book_id:
                client = self._repo_client.find_client_by_id(rental.client_id)
                if client:
                    borrowers.append({'Client': client.name, 'Rented Date': rental.rented_date})
        borrowers.sort(key=lambda item: (item['Client'], item['Rented Date']))
        return borrowers

    def add_rental(self, rental_id, book_id, client_id, rented_date):
        """
        Add a new rental transaction after validating book and client existence.
        
        Args:
            rental_id: The unique ID for the rental
            book_id: The ID of the book being rented
            client_id: The ID of the client renting the book
            rented_date: The date the book is rented
            
        Raises:
            ValueError: If the book or client doesn't exist, or if the book is already rented
        """
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
        """
        Mark a rental as returned by updating the return date.
        
        Args:
            rental_id: The ID of the rental to mark as returned
            returned_date: The date the book is being returned
            
        Raises:
            ValueError: If the rental doesn't exist or has already been returned
        """
        rental = self._repo_rental.find_rental_by_id(rental_id)
        if rental is None:
            raise ValueError(f"Rental with ID {rental_id} not found.")
        if rental.returned_date is not None:
            raise ValueError(f"Book for Rental ID {rental_id} has already been returned.")
        self._repo_rental.update_rental(rental_id, returned_date)

    def get_all_rentals(self):
        """
        Retrieve all rentals from the repository.
        
        Returns:
            list: A list of all Rental objects in the repository
        """
        return self._repo_rental.get_all_rentals()
    
    def get_most_rented_books(self):
        """
        Get the top 3 most rented books in the system.
        
        Returns:
            list: A list of tuples containing (Book, rental_count) sorted by rental count in descending order
        """
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
        """
        Get the top 20% most active clients (by number of rentals) in the system.
        
        Returns:
            list: A list of tuples containing (Client, rental_count) sorted by rental count in descending order
        """
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