"""
This will be the controller file, atleast initiallly for now.
Controllers are supposed to process the API calls and deal with making the view and the model codes run
"""
import model
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({"Hello": "World"})

@app.route('/users/add', methods = ['POST'])
def add_user():
    resp = model.add_user(request.get_json())
    return resp

@app.route('/users/remove', methods = ['DELETE'])
def remove_user():
    resp = model.remove_user(request.get_json())
    return resp

@app.route('/users/<int:index>')
def view_user():
    print("Hello WOrld")



app.run()