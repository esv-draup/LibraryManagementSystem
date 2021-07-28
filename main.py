from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from librarian.librarian import Librarian
from book.book import Book
from user.user import User

app = Flask(__name__)
api = Api(app)

api.add_resource(User, '/users')
api.add_resource(Book, '/books')
api.add_resource(Librarian, '/librarians')
if __name__ == "__main__":
    app.run()
