from domain.domain import Book, Client
from controller.service_book import ServiceBook
from controller.service_client import ServiceClient
class Console:
    def __init__(self, service, service_client):
        self._service = service
        self._service_client = service_client

    def run_console(self):
        while True:
            print("1. Add Book")
            print("2. List All Books")
            print("3. Remove Book by ID")
            print("4. Update Book")
            print("5. Search Books by Title")
            print("6. Add Client")
            print("7. List All Clients")
            print("8. Remove Client by ID")
            print("9. Update Client")
            print("10. Search Clients by Name")
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
                case '5':
                    try:
                        title_query = input("Enter title to search: ")
                        results = self._service.search_by_title(title_query)
                        if not results:
                            print("No books found with that title.")
                        else:
                            for book in results:
                                print(book)
                    except Exception as e:
                        print(f"Error: {e}")
                case '6':
                    try:
                        id = int(input("Enter Client ID: "))
                        name = input("Enter Client Name: ")
                        client = Client(id, name)
                        self._service_client.add_client(client)
                        print("Client added successfully.")
                    except Exception as e:
                        print(f"Error: {e}")
                case '7':
                    clients = self._service_client.get_all_clients()
                    if not clients:
                        print("No clients available.")
                    else:
                        for client in clients:
                            print(client)
                case '8':
                    try:    
                        client_id = int(input("Enter Client ID to remove: "))
                        self._service_client.remove_client(client_id)
                        print("Client removed successfully.")
                    except Exception as e:
                        print(f"Error: {e}")
                case '9':
                    try:
                        id = int(input("Enter Client ID to update: "))
                        name = input("Enter new Client Name: ")
                        updated_client = Client(id, name)
                        self._service_client.update_client(updated_client)
                        print("Client updated successfully.")
                    except Exception as e:
                        print(f"Error: {e}")
                case '10':
                    try:
                        name_query = input("Enter name to search: ")
                        results = self._service_client.search_by_name(name_query)
                        if not results:
                            print("No clients found with that name.")
                        else:
                            for client in results:
                                print(client)
                    except Exception as e:
                        print(f"Error: {e}")
                case '0':
                    break
                case _ :
                    print("Invalid option. Please try again.")