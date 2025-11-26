import unittest
from controller.service_book import ServiceBook
from repo.repo_book import RepoBook
from domain.domain import Book

class TestServiceBook(unittest.TestCase):
    
    def setUp(self):
        # The service NEEDS a repository to work, so we create one here.
        self.repo = RepoBook()
        self.service = ServiceBook(self.repo)

    def test_add_valid_book(self):
        # Happy path: everything should work
        book = Book(1, "Valid Title", "Desc", "Author")
        self.service.add_book(book)
        
        # Check if it actually got into the repo
        self.assertEqual(len(self.service.get_all_books()), 1)

    def test_add_invalid_book_id(self):
        # Sad path: Negative ID should fail
        bad_book = Book(-5, "Title", "Desc", "Author")
        
        # We expect a ValueError here. If no error happens, the test FAILS.
        with self.assertRaises(ValueError):
            self.service.add_book(bad_book)

    def test_add_invalid_book_title(self):
        # Sad path: Empty title should fail
        bad_book = Book(1, "", "Desc", "Author")
        
        with self.assertRaises(ValueError):
            self.service.add_book(bad_book)
    
    def test_remove_book(self):