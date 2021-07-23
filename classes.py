from werkzeug.security import generate_password_hash
class User:
    def __init__(self, name, email, password, librarian=False):
        self.name = name
        self.email = email
        self.hashed_password = generate_password_hash(password)
        self.issued_books = {}
        self.librarian = librarian


class Book:
    def __init__(self, name, book_id, genre):
        self.name = name
        self.book_id = book_id
        self.genre = genre
