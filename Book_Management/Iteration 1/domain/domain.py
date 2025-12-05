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