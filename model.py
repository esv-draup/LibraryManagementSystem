from flask_pymongo import MongoClient
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

client = MongoClient()
db = client.LMS_DB
users = db.Users


class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.hashed_password = generate_password_hash(password)
        self.issued_books = {"1": "Harry Potter", "2": "Harry Potter 2", "3": "Harry Potter 3"}


def add_user(given_json):
    # Add function to check if there is already a user with the same email ID
    # Add password functionality
    """
    given_json will have the format
    {
        name:
        email:
        password:
    }
    The password will be hashed and stored into the database.
    """
    _email = given_json['email']
    if (users.find_one({"email": _email})):
        resp = jsonify("User with same email already exists")
        resp.status_code = 200
        return resp
    user = User(given_json['name'], given_json['email'], given_json['password'])
    user_id = users.insert_one(user.__dict__).inserted_id
    resp = jsonify("User added successfully")
    resp.status_code = 200
    return resp


def remove_user(given_json):
    # The user will also give their password here so we would want to check that.
    """
    given_json will have the format
    {
        email:
        password:
    }
    This will enable the user to delete their own account, provided that the password they entered has the same
    hash as the one that is stored in the database.
    """
    _email = given_json['email']
    if (check_password_hash(users.find_one({"email": _email})['hashed_password'], given_json['password'])):
        users.delete_one({"email": _email})
        resp = jsonify("User removed Successfully")
        resp.status_code = 200
        return resp
    else:
        resp = jsonify("Incorrect Password")
        resp.status_code = 200
        return resp