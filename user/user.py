from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify
from flask_restful import Resource
from flask_pymongo import MongoClient
from flask_httpauth import HTTPBasicAuth


client = MongoClient()
db = client.LMS_DB
userDB = db.Users
librarianDB = db.Librarians
auth = HTTPBasicAuth()
auth_lib = HTTPBasicAuth()
auth_user = HTTPBasicAuth()


@auth.verify_password
def verify(username, password):
    try:
        if check_password_hash(librarianDB.find_one({"email": username})['password'], password):
            return True
    except Exception as e:
        if check_password_hash(userDB.find_one({"email": username})['password'], password):
            return True
    except:
        return False


@auth_lib.verify_password
def verify_lib(username, password):
    if check_password_hash(librarianDB.find_one({"email": username})['password'], password):
        return True
    else:
        return False


@auth_user.verify_password
def verify_user(username, password):
    if check_password_hash(userDB.find_one({"email": username})['password'], password):
        return True
    else:
        return False


class User(Resource):
    """
    For all the CRUD operations involving regular users of the library.
    """

    def __init__(self):
        self.issued_book = {}

    # anyone can add users
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

    @auth_lib.login_required
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
                'issued_book': i['issued_book']
            }
            dictlist.append(dicta)
        response = jsonify(dictlist)
        response.status_code = 200
        return response

    @auth.login_required
    def delete(self):
        """
        The delete method will be called upon the DELETE request. It is the Delete in CRUD
        :return:
        """
        librarian_user = False
        try:
            #print(librarian_user)
            librarianname = librarianDB.find_one({"email": request.authorization['username']})
            #print(librarianname)
            if librarianname:
                librarian_user = True
            #print(librarian_user)
        except Exception as e:
            librarian_user = False
            print(e)
        print(request.authorization['username'],request.get_json()['email'], librarian_user)
        if not (request.authorization['username'] == request.get_json()['email']) and not librarian_user:
            resp = jsonify("User cannot remove another user")
            resp.status_code = 200
            return resp
        request_json = request.get_json()
        _email = request_json['email']
        userDB.delete_one({"email": _email})
        resp = jsonify("User removed Successfully")
        resp.status_code = 200
        return resp
