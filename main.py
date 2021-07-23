from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey"
app.config["MONGO_URI"] "mongoDB://localhost:27017/somedatabase"

mongo = PyMongo(app)

if(__name__ == "__main__"):
    app.run(debug=True)