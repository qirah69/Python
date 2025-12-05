from repo.repo_book import RepoBook
from domain.domain import Book

import unittest
from repo.repo_book import RepoBook
from repo.repo_client import RepoClient
from domain.domain import Book, Client

class TestRepoBook(unittest.TestCase):
    
    def setUp(self):
        self.repo = RepoBook()

    def test_add_book(self):
        book = Book(1, "Test Title", "Desc", "Author")
        self.repo.add_book(book)
        
        all_books = self.repo.get_all_books()
        self.assertEqual(len(all_books), 1)
        self.assertEqual(all_books[0].title, "Test Title")

    def test_remove_book(self):
        # 1. Add a book first
        book = Book(1, "To Delete", "Desc", "Auth")
        self.repo.add_book(book)

        # 2. Delete it
        self.repo.delete_book_by_id(1)

        # 3. Check if list is empty
        all_books = self.repo.get_all_books()
        self.assertEqual(len(all_books), 0)

class TestRepoClient(unittest.TestCase):

    def setUp(self):
        self.repo = RepoClient()

    def test_add_client(self):
        client = Client(1, "Alice")
        self.repo.add_client(client)

        all_clients = self.repo.get_all_clients()
        self.assertEqual(len(all_clients), 1)
        self.assertEqual(all_clients[0].name, "Alice")

    def test_remove_client(self):
        client = Client(1, "Bob")
        self.repo.add_client(client)

        self.repo.remove_client(1)

        all_clients = self.repo.get_all_clients()
        self.assertEqual(len(all_clients), 0)