from repo.repo import RepoBook
from domain.domain import Book

class ServiceBook:
    def __init__(self, repo):
        self._repo = repo

    def __validate(self, book):
        if not isinstance(book, Book):
            raise TypeError("The provided value is not a Book instance.")
        if book.id < 0:
            raise ValueError("Book ID must be non-negative.")
        if not book.title:
            raise ValueError("Book title cannot be empty.")

    def add_book(self, book):
        self.__validate(book)
        self._repo.add_book(book)

    def get_all_books(self):
        return self._repo.get_all_books()
    
    def remove_book(self, id):
        if not isinstance(id, int):
            raise TypeError("Book ID must be an integer.")
        if id < 0:
            raise ValueError("Book ID must be non-negative.")
        self._repo.delete_book_by_id(id)

    def update_book(self, new_book):
        self.__validate(new_book)
        self._repo.update_book(new_book)