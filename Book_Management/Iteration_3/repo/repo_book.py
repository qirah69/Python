class RepoBook:
    def __init__(self):
        """
        Initialize an empty RepoBook repository.
        """
        self._books = []
    
    def add_book(self, book):
        """
        Add a new book to the repository.
        
        Args:
            book: The Book object to add
        """
        self._books.append(book)

    def get_all_books(self):
        """
        Retrieve all books from the repository.
        
        Returns:
            list: A list of all Book objects
        """
        return self._books
    
    def delete_book_by_id(self, book_id):
        """
        Delete a book from the repository by its ID.
        
        Args:
            book_id: The ID of the book to delete
        """
        for book in self._books:
            if book.id == book_id:
                self._books.remove(book)
                return
            
    def update_book(self, updated_book):
        """
        Update an existing book in the repository.
        
        Args:
            updated_book: The Book object with updated information
        """
        for book in self._books:
            if book.id == updated_book.id:
                book.title = updated_book.title
                book.description = updated_book.description
                book.author = updated_book.author
                return
        
    def search_by_title(self, title_query):
        """
        Search for books by title query (case-insensitive partial match).
        
        Args:
            title_query: The title or partial title to search for
            
        Returns:
            list: A list of Book objects matching the query
        """
        return [book for book in self._books if title_query.lower() in book.title.lower()]
    
    def find_book_by_id(self, book_id):
        """
        Find a book by its ID.
        
        Args:
            book_id: The ID of the book to find
            
        Returns:
            Book: The Book object if found, None otherwise
        """
        for book in self._books:
            if book.id == book_id:
                return book
        return None