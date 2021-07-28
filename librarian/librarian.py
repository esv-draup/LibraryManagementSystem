from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource
from flask_pymongo import MongoClient
from flask_httpauth import HTTPBasicAuth
from flask import request, jsonify

client = MongoClient()
db = client.LMS_DB
librarianDB = db.Librarians
auth_lib = HTTPBasicAuth()

@auth_lib.verify_password
def verify_lib(username, password):
    if check_password_hash(librarianDB.find_one({"email": username})['password'], password):
        return True
    else:
        return False

class Librarian(Resource):

    @auth_lib.login_required
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

    @auth_lib.login_required
    def get(self):
        """
        The get method will be called upon the GET request. It is the Read in CRUD
        This method will be to view all users. This may be a librarian only feature.
        :return:
        """
        cursor_obj = librarianDB.find()
        list_cur = list(cursor_obj)  # we convert the cursor object to a list of dictionaries
        dictlist = []
        for i in list_cur:
            dicta = {
                'name': i['name'],
                'email': i['email']
            }
            dictlist.append(dicta)
        response = jsonify(dictlist)
        response.status_code = 200
        return response

    @auth_lib.login_required
    def delete(self):
        request_json = request.get_json()
        _email = request_json['email']
        librarianDB.delete_one({"email": _email})
        resp = jsonify("Librarian removed Successfully")
        resp.status_code = 200
        return resp