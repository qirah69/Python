import unittest
from domain.domain import Book, Client

class TestDomain(unittest.TestCase):
    
    def test_book_creation(self):
        # 1. Create a book
        book = Book(1, "Dune", "Sci-fi epic", "Frank Herbert")
        
        # 2. Check if attributes are saved correctly
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Dune")
        self.assertEqual(book.description, "Sci-fi epic")
        self.assertEqual(book.author, "Frank Herbert")

    def test_book_str(self):
        # 1. Create a book
        book = Book(1, "Dune", "Sci-fi epic", "Frank Herbert")
        
        # 2. Check if the string representation is correct
        # Note: This must match exactly what you wrote in __str__
        expected_string = "Book[ID: 1, Title: Dune, Description: Sci-fi epic, Author: Frank Herbert]"
        self.assertEqual(str(book), expected_string)

    def test_client_creation(self):
        # 1. Create a client
        client = Client(1, "Alice")
        
        # 2. Check if attributes are saved correctly
        self.assertEqual(client.id, 1)
        self.assertEqual(client.name, "Alice")

    def test_client_str(self):
        # 1. Create a client
        client = Client(1, "Alice")
        
        # 2. Check if the string representation is correct
        # Note: This must match exactly what you wrote in __str__
        expected_string = "Client[ID: 1, Name: Alice]"
        self.assertEqual(str(client), expected_string)