from flask import Flask, jsonify, request, Response

import json

from settings import *

from BookModel import *

import datetime

import jwt

app.config["SECRET_KEY"] = "meow"


@app.route("/login", methods=["GET"])
def get_token():
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
    token = jwt.encode({"exp": expiration_date}, app.config["SECRET_KEY"], algorithm="HS256")
    return token


@app.route("/books", methods=["GET"])
def get_books():
    token = request.args.get("token")
    try:
        jwt.decode(token, app.config["SECRET_KEY"])
    except:
        return jsonify({"error": "need a valid token to view this page"})

    return jsonify({"books": Book.get_all_books()})


@app.route("/books/<int:isbn>", methods=["GET"])
def get_books_by_isbn(isbn):
    return_value = Book.get_book_by(isbn)
    return jsonify(return_value)


def validbookobject(bookobject):
    if "name" in bookobject and "price" in bookobject and "isbn" in bookobject:
        return True
    else:
        return False


@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if validbookobject(request_data):
        Book.add_book(request_data["name"], request_data["price"], request_data["isbn"])
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(request_data['isbn'])
        return response
    else:
        invalidbookobjecterrormsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 9780394800165 }"
        }
        response = Response(json.dumps(invalidbookobjecterrormsg), status=400, mimetype='application/json')
        return response;


@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    Book.replace_book(isbn, request_data["price"], request_data["name"])

    return jsonify({"status": "book updated"})


@app.route("/books/<int:isbn>", methods=["PATCH"])
def update_book(isbn):
    request_data = request.get_json()
    Book.update_book_name(isbn, request_data["price"])

    response = Response("", status=201, mimetype='application/json')
    return response


@app.route("/books/<int:isbn>", methods=["PATCH"])
def update_books(isbn):
    request_data = request.get_json()
    Book.update_book_price(isbn, request_data["price"])

    response = Response("", status=201, mimetype='application/json')
    return response


@app.route("/books/<int:isbn>", methods=["DELETE"])
def delete_book(isbn):
    Book.del_book(isbn)

    response = Response("", status=201, mimetype='application/json')
    return response


app.run(port=8000)
