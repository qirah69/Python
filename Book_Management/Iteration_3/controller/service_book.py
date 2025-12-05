from repo.repo_book import RepoBook
from domain.domain import Book

class ServiceBook:
    def __init__(self, repo):
        """
        Initialize the ServiceBook with a repository instance.
        
        Args:
            repo: The book repository to use for data operations
        """
        self._repo = repo

    def __validate(self, book):
        """
        Validate a book object to ensure it meets all requirements.
        
        Args:
            book: The book object to validate
            
        Raises:
            TypeError: If the book is not a Book instance
            ValueError: If book ID is negative or title is empty
        """
        if not isinstance(book, Book):
            raise TypeError("The provided value is not a Book instance.")
        if book.id < 0:
            raise ValueError("Book ID must be non-negative.")
        if not book.title:
            raise ValueError("Book title cannot be empty.")

    def add_book(self, book):
        """
        Add a new book to the repository after validation.
        
        Args:
            book: The book object to add
            
        Raises:
            TypeError: If the book is not a Book instance
            ValueError: If book ID is negative or title is empty
        """
        self.__validate(book)
        self._repo.add_book(book)

    def get_all_books(self):
        """
        Retrieve all books from the repository.
        
        Returns:
            list: A list of all Book objects in the repository
        """
        return self._repo.get_all_books()
    
    def remove_book(self, id):
        """
        Remove a book from the repository by its ID.
        
        Args:
            id: The ID of the book to remove
            
        Raises:
            TypeError: If the ID is not an integer
            ValueError: If the ID is negative
        """
        if not isinstance(id, int):
            raise TypeError("Book ID must be an integer.")
        if id < 0:
            raise ValueError("Book ID must be non-negative.")
        self._repo.delete_book_by_id(id)

    def update_book(self, new_book):
        """
        Update an existing book in the repository after validation.
        
        Args:
            new_book: The updated Book object with new values
            
        Raises:
            TypeError: If the book is not a Book instance
            ValueError: If book ID is negative or title is empty
        """
        self.__validate(new_book)
        self._repo.update_book(new_book)

    def search_by_title(self, title_query):
        """
        Search for books by title in the repository.
        
        Args:
            title_query: The title or partial title to search for
            
        Returns:
            list: A list of Book objects matching the search query
            
        Raises:
            TypeError: If the title_query is not a string
        """
        if not isinstance(title_query, str):
            raise TypeError("Title query must be a string.")
        return self._repo.search_by_title(title_query)