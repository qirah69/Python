class RepoBook:
    def __init__(self):
        self._books = []
    
    def add_book(self, book):
        self._books.append(book)

    def get_all_books(self):
        return self._books
    
    def delete_book_by_id(self, book_id):
        for book in self._books:
            if book.id == book_id:
                self._books.remove(book)
                return
            
    def update_book(self, updated_book):
        for book in self._books:
            if book.id == updated_book.id:
                book.title = updated_book.title
                book.description = updated_book.description
                book.author = updated_book.author
                return