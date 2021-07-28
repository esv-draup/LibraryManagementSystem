from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify
from flask_restful import Resource
from flask_pymongo import MongoClient

client = MongoClient()
db = client.LMS_DB
userDB = db.Users
class User(Resource):
    """
    For all the CRUD operations involving regular users of the library.
    """

    def __init__(self):
        self.issued_books = []

    def post(self):
        """
        The post method will be called upon the POST request. It is the Create in CRUD
        This method will be to add new users.
        :return:
        """
        request_json = request.get_json()
        if request_json['name'] and request_json['email'] and request_json['password']:
            self.name = request_json['name']
            self.email = request_json['email']
            self.password = generate_password_hash(request_json['password'])
            userID = userDB.insert_one(self.__dict__).inserted_id
            response = jsonify("User Created Successfully ")
            response.status_code = 200
        else:
            response = jsonify("Information should contain name, email and password. Please try again.")
            response.status_code = 200
            return response
        return response

    def get(self):
        """
        The get method will be called upon the GET request. It is the Read in CRUD
        This method will be to view all users. This may be a librarian only feature.
        :return:
        """
        cursor_obj = userDB.find()
        list_cur = list(cursor_obj)  # we convert the cursor object to a list of dictionaries
        dictlist = []
        for i in list_cur:
            dicta = {
                'name': i['name'],
                'email': i['email'],
                'issued_books': i['issued_books']
            }
            dictlist.append(dicta)
        response = jsonify(dictlist)
        response.status_code = 200
        return response

    def put(self):
        """
        The put method will be called upon the PUT request. It is the Update in CRUD
        This is for updating users, with their issued books.
        :return:
        """
        return

    def delete(self):
        """
        The delete method will be called upon the DELETE request. It is the Delete in CRUD
        :return:
        """
        request_json = request.get_json()
        _email = request_json['email']
        if check_password_hash(userDB.find_one({"email": _email})['password'], request_json['password']):
            userDB.delete_one({"email": _email})
            resp = jsonify("User removed Successfully")
            resp.status_code = 200
            return resp
        else:
            resp = jsonify("Incorrect Password")
            resp.status_code = 200
            return resp