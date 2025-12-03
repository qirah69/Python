class Book:
    def __init__(self, id, title, description, author):
        self.id = id
        self.title = title
        self.description = description
        self.author = author
    
    def __str__(self):
        return f"Book[ID: {self.id}, Title: {self.title}, Description: {self.description}, Author: {self.author}]"
    
class Client:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"Client[ID: {self.id}, Name: {self.name}]"
    
class Rental:
    def __init__(self, id, book_id, client_id, rented_date, returned_date=None):
        self.id = id
        self.book_id = book_id
        self.client_id = client_id
        self.rented_date = rented_date
        self.returned_date = returned_date
    
    def __str__(self):
        return (f"Rental[ID: {self.id}, Book ID: {self.book_id}, Client ID: {self.client_id}, "
                f"Rented Date: {self.rented_date}, Returned Date: {self.returned_date}]")