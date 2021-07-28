from werkzeug.security import generate_password_hash
from flask_restful import Resource
from flask_pymongo import MongoClient
from flask import request, jsonify

client = MongoClient()
db = client.LMS_DB
librarianDB = db.Librarians


class Librarian(Resource):
    def post(self):
        request_json = request.get_json()
        if request_json['name'] and request_json['email'] and request_json['password']:
            self.name = request_json['name']
            self.email = request_json['email']
            self.password = generate_password_hash(request_json['password'])
        librarianID = librarianDB.insert_one(self.__dict__).inserted_id
        response = jsonify("Librarian Created Successfully.")
        response.status_code = 200
        return response
