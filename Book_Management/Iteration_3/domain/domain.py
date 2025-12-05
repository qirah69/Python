class Book:
    def __init__(self, id, title, description, author):
        """
        Initialize a Book object.
        
        Args:
            id: The unique identifier for the book
            title: The title of the book
            description: A description of the book
            author: The author of the book
        """
        self.id = id
        self.title = title
        self.description = description
        self.author = author
    
    def __str__(self):
        """
        Return a string representation of the Book object.
        
        Returns:
            str: A formatted string with book details
        """
        return f"Book[ID: {self.id}, Title: {self.title}, Description: {self.description}, Author: {self.author}]"
    
class Client:
    def __init__(self, id, name):
        """
        Initialize a Client object.
        
        Args:
            id: The unique identifier for the client
            name: The name of the client
        """
        self.id = id
        self.name = name

    def __str__(self):
        """
        Return a string representation of the Client object.
        
        Returns:
            str: A formatted string with client details
        """
        return f"Client[ID: {self.id}, Name: {self.name}]"
    
class Rental:
    def __init__(self, id, book_id, client_id, rented_date, returned_date=None):
        """
        Initialize a Rental object.
        
        Args:
            id: The unique identifier for the rental
            book_id: The ID of the rented book
            client_id: The ID of the client renting the book
            rented_date: The date the book was rented
            returned_date: The date the book was returned (optional, defaults to None)
        """
        self.id = id
        self.book_id = book_id
        self.client_id = client_id
        self.rented_date = rented_date
        self.returned_date = returned_date
    
    def __str__(self):
        """
        Return a string representation of the Rental object.
        
        Returns:
            str: A formatted string with rental details
        """
        return (f"Rental[ID: {self.id}, Book ID: {self.book_id}, Client ID: {self.client_id}, "
                f"Rented Date: {self.rented_date}, Returned Date: {self.returned_date}]")