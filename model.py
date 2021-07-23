from flask_pymongo import MongoClient
from flask import jsonify
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from classes import User, Book

client = MongoClient()
db = client.LMS_DB
users = db.Users  # This is the object for the Users collection


def add_user(given_json):
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
    if users.find_one({"email": _email}):
        resp = jsonify("User with same email already exists")
        resp.status_code = 200
        return resp
    user = User(given_json['name'], given_json['email'], given_json['password'])
    user_id = users.insert_one(user.__dict__).inserted_id
    resp = jsonify("User added successfully")
    resp.status_code = 200
    return resp


def view_users():
    """
    This is a method to view all users, and their currently issued books.
    """
    cursor_obj = users.find()
    list_cur = list(cursor_obj)  # we convert the cursor object to a list of dictionaries
    dictlist = []
    for i in list_cur:
        dict = {
            'name': i['name'],
            'email': i['email'],
            'issued_books': i['issued_books']
        }
        dictlist.append(dict)
    resp = jsonify(dictlist)
    resp.status_code = 200
    return resp


def update_user(given_json):
    """
    update_user() needs to handle new passwords, and mainly, issuing and returning of books
    given_json will have the format
    {
        name: #For change of name
        email: #For change of email
        password: #The old/current password for authentication
        new_password: #The new to-be password
    }
    """
    # So over here we do he code if they don't want a new password
    try:
        newpass = given_json['new_password']
        if (check_password_hash(users.find_one({"email": _email})['hashed_password'], given_json['password'])):
            users.update_one({'email': given_json['email']}, {"$set": {'password': generate_password_hash(newpass)}})
            resp = jsonify("Password has been updated")
            resp.status_code = 200
            return resp
        else:
            resp = jsonify("Incorrect Password")
            resp.status_code = 200
            return resp
    except:
        resp = jsonify("No new password entered")
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
