from domain.domain import Book
from controller.service import ServiceBook
class Console:
    def __init__(self, service):
        self._service = service

    def run_console(self):
        while True:
            print("1. Add Book")
            print("2. List All Books")
            print("3. Remove Book by ID")
            print("4. Update Book")
            print("0. Exit")
            choice = input("Choose an option: ")
            match choice:
                case '1':
                    try:
                        id = int(input("Enter Book ID: "))
                        title = input("Enter Book Title: ")
                        description = input("Enter Book Description: ")
                        author = input("Enter Book Author: ")
                        book = Book(id, title, description, author)
                        self._service.add_book(book)
                        print("Book added successfully.")
                    except Exception as e:
                        print(f"Error: {e}")
                case '2':
                    books = self._service.get_all_books()
                    if not books:
                        print("No books available.")
                    else:
                        for book in books:
                            print(book)
                case '3':
                    try:
                        id = int(input("Enter Book ID to remove: "))
                        self._service.remove_book(id)
                        print("Book removed successfully.")
                    except Exception as e:
                        print(f"Error: {e}")
                case '4':
                    try:
                        id = int(input("Enter Book ID to update: "))
                        title = input("Enter new Book Title: ")
                        description = input("Enter new Book Description: ")
                        author = input("Enter new Book Author: ")
                        updated_book = Book(id, title, description, author)
                        self._service.update_book(updated_book)
                        print("Book updated successfully.")
                    except Exception as e:
                        print(f"Error: {e}")
                case '0':
                    break
                case _ :
                    print("Invalid option. Please try again.")