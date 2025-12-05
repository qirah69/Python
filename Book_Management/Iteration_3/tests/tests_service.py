import unittest

from domain.domain import Book, Client, Rental
from repo.repo_book import RepoBook
from repo.repo_client import RepoClient
from repo.repo_rental import RepoRental
from controller.service_book import ServiceBook
from controller.service_client import ServiceClient
from controller.service_rental import ServiceRental

"""
Unit tests for the service classes.

This module contains tests for ServiceBook, ServiceClient, and ServiceRental
to verify business logic, validation, and rental operations.
"""

class TestServiceClient(unittest.TestCase):
    def setUp(self):
        """
        Initialize a ServiceClient instance for testing.
        """
        self.repo = RepoClient()
        self.service = ServiceClient(self.repo)

    def test_add_valid_client(self):
        """
        Test adding a valid client to the service.
        Verifies that the client is added successfully.
        """
        client = Client(1, "Alice")
        self.service.add_client(client)
        self.assertEqual(len(self.service.get_all_clients()), 1)

    def test_add_invalid_client_name(self):
        """
        Test adding a client with an empty name.
        Verifies that a ValueError is raised for empty names.
        """
        # Name cannot be empty
        bad_client = Client(1, "")
        with self.assertRaises(ValueError):
            self.service.add_client(bad_client)

    def test_add_negative_id(self):
        """
        Test adding a client with a negative ID.
        Verifies that a ValueError is raised for negative IDs.
        """
        bad_client = Client(-1, "Bob")
        with self.assertRaises(ValueError):
            self.service.add_client(bad_client)

class TestServiceRental(unittest.TestCase):
    def setUp(self):
        """
        Initialize ServiceRental instances with all required repositories for testing.
        Pre-loads sample books and clients for rental tests.
        """
        # ServiceRental needs ALL three repos to work
        self.book_repo = RepoBook()
        self.client_repo = RepoClient()
        self.rental_repo = RepoRental()
        
        self.service = ServiceRental(self.rental_repo, self.book_repo, self.client_repo)

        # Pre-load some data so we can test renting
        self.book_repo.add_book(Book(100, "Dune", "SciFi", "Herbert"))
        self.client_repo.add_client(Client(1, "Alice"))
        self.client_repo.add_client(Client(2, "Bob"))

    def test_rent_book_success(self):
        """
        Test successfully renting a book.
        Verifies that a rental is created when both book and client exist.
        """
        # Alice rents Book 100
        self.service.add_rental(1, 100, 1, "2024-01-01")
        self.assertEqual(len(self.service.get_all_rentals()), 1)

    def test_rent_book_already_rented(self):
        """
        Test renting a book that is already rented.
        Verifies that a ValueError is raised when attempting to rent an unavailable book.
        """
        # 1. Alice rents it first
        self.service.add_rental(1, 100, 1, "2024-01-01")
        
        # 2. Bob tries to rent the SAME book (should fail)
        with self.assertRaises(ValueError) as context:
            self.service.add_rental(2, 100, 2, "2024-01-02")
        
        # Optional: Check the error message says "already rented"
        self.assertIn("already rented", str(context.exception))

    def test_rent_nonexistent_book(self):
        """
        Test renting a book that doesn't exist in the repository.
        Verifies that a ValueError is raised for non-existent books.
        """
        # Trying to rent Book ID 999 (which doesn't exist)
        with self.assertRaises(ValueError):
            self.service.add_rental(1, 999, 1, "2024-01-01")

    def test_report_borrowers_sorting(self):
        """
        Test that the borrowers report is sorted correctly by name then date.
        Verifies the correct sorting order: Name (alphabetical), then Rented Date (chronological).
        """
        # This tests the complex "Sort by Name, then Date" requirement
        
        # Setup: Bob rents Jan 5, Alice rents March 1, Alice rents Jan 1
        self.service.add_rental(1, 100, 2, "2024-01-05") # Bob
        self.service.return_book(1, "2024-01-10") # Returned
        
        self.service.add_rental(2, 100, 1, "2024-03-01") # Alice Late
        self.service.return_book(2, "2024-03-05")
        
        self.service.add_rental(3, 100, 1, "2024-01-01") # Alice Early

        # Call the report
        report = self.service.get_report_book_borrowers(100)

        # Verify Order:
        # 1. Alice (2024-01-01) - Alphabetical first, then earliest date
        self.assertEqual(report[0]['Client'], "Alice")
        self.assertEqual(report[0]['Rented Date'], "2024-01-01")
        
        # 2. Alice (2024-03-01)
        self.assertEqual(report[1]['Rented Date'], "2024-03-01")
        
        # 3. Bob
        self.assertEqual(report[2]['Client'], "Bob")

    def test_most_active_clients_top_20(self):
        """
        Test retrieving the top 20% most active clients.
        Verifies that only the top 20% of clients by rental count are returned.
        """
        # Add enough clients to test the math (Need at least 5 to get 1 in top 20%)
        for i in range(3, 8): 
            self.client_repo.add_client(Client(i, f"User{i}"))
            
        # Alice (ID 1) rents 3 times
        for i in range(10, 13):
            self.service.add_rental(i, 100, 1, "2024-01-01")
            self.service.return_book(i, "2024-01-02")

        # Bob (ID 2) rents 1 time
        self.service.add_rental(20, 100, 2, "2024-01-01")

        # Get report
        result = self.service.get_most_active_clients()

        # Should only return Alice (Top 1 out of 7)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0].name, "Alice")