from flask_restful import Resource
from flask import jsonify, request
from flask_pymongo import MongoClient
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
import datetime

client = MongoClient()
db = client.LMS_DB
bookDB = db.Books
librarianDB = db.Librarians
userDB = db.Users
auth = HTTPBasicAuth()
auth_lib = HTTPBasicAuth()
auth_user = HTTPBasicAuth()


class UserSession():
    def __init__(self):
        self.user_in_session = ""


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
    # For verifying that password is needed
    if check_password_hash(librarianDB.find_one({"email": username})['password'], password):
        return True
    else:
        return False


us = UserSession()


@auth_user.verify_password
def verify_user(username, password):
    if check_password_hash(userDB.find_one({"email": username})['password'], password):
        us.user_in_session = username
        return True
    else:
        return False


class Book(Resource):
    # Just add authorization from here
    def __init__(self):
        self.issued = {
            "due_date": "",
            "user_name": ""
        }
        """
        The format of issued is as follows
        {
            "due_date": date_object,
            "user_name": user's name
        }
        """

    @auth.login_required
    def get(self):
        # Now I need to show all books
        cursor_obj = bookDB.find()
        list_cur = list(cursor_obj)  # we convert the cursor object to a list of dictionaries
        dictlist = []
        for i in list_cur:
            dicta = {
                'book_name': i['book_name'],
                'book_id': i['book_id'],
                'book_genre': i['book_genre'],
                'issued': i['issued']
            }
            dictlist.append(dicta)
        response = jsonify(dictlist)
        response.status_code = 200
        return response

    @auth_lib.login_required
    def post(self):
        """
        The post method will be called upon the POST request. It is the Create in CRUD
        This method will be to add new books by the librarian.
        :return:
        """

        request_json = request.get_json()
        try:
            if request_json['book_name'] and request_json['book_id'] and request_json['book_genre']:
                self.book_name = request_json['book_name']
                self.book_id = request_json['book_id']
                self.book_genre = request_json['book_genre']
                book_obj_id = bookDB.insert_one(self.__dict__).inserted_id
                response = jsonify("Book added successfully.")
                response.status_code = 200
                return response
            else:
                response = jsonify("Information should contain the book's name, ID and genre. Please try again.")
                response.status_code = 200
                return response
        except Exception as e:
            response = jsonify("Information entered incorrectly. Please try again.")
            response.status_code = 200
            print(e)
            return response

    @auth_user.login_required
    def put(self):
        """
        This is for issuing of book.
        Request will have the format
        {
            "bookID":
        }
        :return:
        """
        request_json = request.get_json()
        try:
            _book_id = request_json['book_id']
            # find in db, if not found, return error, else
            if not (bookDB.find_one({"book_id": _book_id})['book_id']):
                response = jsonify('No book with given bookID is in database, try again.')
                response.status_code = 200
                return response
            if not(bookDB.find_one({"book_id": _book_id})['issued']['user_name'] == us.user_in_session) and not(bookDB.find_one({"book_id": _book_id})['issued']['user_name'] == ""):
                response = jsonify('Book has already been issued to another user.')
                response.status_code = 200
                return response
            duedate = datetime.date.today() + datetime.timedelta(days=14)
            duedate = duedate.strftime("%d/%m/%Y")
            issued_dict = {
                "due_date": duedate,
                "user_name": us.user_in_session
            }
            bookDB.update_one({"book_id": _book_id}, {"$set": {"issued": issued_dict}})
            response = jsonify("Book successfully issued.")
            response.status_code = 200
            return response
        except Exception as e:
            response = jsonify("bookID not found in given input, try again.")
            response.status_code = 200
            print(e)
            return response
        # we will take the person's email from here. Or from the authentication tab.
