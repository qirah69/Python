"""
Unit tests for the repository classes.

This module contains comprehensive unit tests for the Book, Client, and Rental
repository classes. It tests core functionality including adding, removing,
searching, and updating entities in the repositories.
"""

import unittest
from domain.domain import Book, Client, Rental
from repo.repo_book import RepoBook
from repo.repo_client import RepoClient
from repo.repo_rental import RepoRental

class TestRepoBook(unittest.TestCase):
    def setUp(self):
        """
        Initialize a RepoBook instance for testing.
        """
        self.repo = RepoBook()

    def test_add_and_remove(self):
        """
        Test adding a book to the repository and then removing it by ID.
        Verifies that the repository size changes accordingly.
        """
        book = Book(1, "Title", "Desc", "Auth")
        self.repo.add_book(book)
        self.assertEqual(len(self.repo.get_all_books()), 1)
        
        self.repo.delete_book_by_id(1)
        self.assertEqual(len(self.repo.get_all_books()), 0)

    def test_search(self):
        """
        Test searching for books by title.
        Verifies that the search returns the correct book when a partial title match is found.
        """
        self.repo.add_book(Book(1, "Harry Potter", "Magic", "Rowling"))
        results = self.repo.search_by_title("Harry")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Harry Potter")

class TestRepoClient(unittest.TestCase):
    def setUp(self):
        """
        Initialize a RepoClient instance for testing.
        """
        self.repo = RepoClient()

    def test_add_and_remove(self):
        """
        Test adding a client to the repository and then removing it by ID.
        Verifies that the repository size changes accordingly.
        """
        client = Client(1, "Alice")
        self.repo.add_client(client)
        self.assertEqual(len(self.repo.get_all_clients()), 1)
        
        self.repo.remove_client(1)
        self.assertEqual(len(self.repo.get_all_clients()), 0)

class TestRepoRental(unittest.TestCase):
    def setUp(self):
        """
        Initialize a RepoRental instance for testing.
        """
        self.repo = RepoRental()

    def test_add_rental(self):
        """
        Test adding a rental to the repository.
        Verifies that the rental is added and the repository size increases.
        """
        rental = Rental(1, 100, 1, "2024-01-01")
        self.repo.add_rental(rental)
        self.assertEqual(len(self.repo.get_all_rentals()), 1)

    def test_remove_rental(self):
        """
        Test removing a rental from the repository by ID.
        Verifies that the rental is removed and the repository size decreases.
        """
        rental = Rental(1, 100, 1, "2024-01-01")
        self.repo.add_rental(rental)
        
        # Remove by ID
        self.repo.remove_rental(1)
        self.assertEqual(len(self.repo.get_all_rentals()), 0)

    def test_update_rental_return(self):
        """
        Test updating a rental's return date.
        Verifies that the return date is correctly updated in the repository.
        """
        # Add rental
        rental = Rental(1, 100, 1, "2024-01-01")
        self.repo.add_rental(rental)
        
        # Update return date
        self.repo.update_rental(1, "2024-01-05")
        
        # Verify it changed
        updated_rental = self.repo.find_rental_by_id(1)
        self.assertEqual(updated_rental.returned_date, "2024-01-05")