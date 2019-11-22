from flask import Flask, jsonify, request, Response

import json

from book_list import books

from settings import *


@app.route("/")
def hello_world():
    return "hello this is a welcome message"


@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)


@app.route("/books/<int:isbn>", methods=["GET"])
def get_books_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                "name": book["name"],
                "price": book["price"]
            }
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
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", status=201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(new_book['isbn'])
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
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    for book in books:
        if book["isbn"] == isbn:
            book.update(new_book)

    return jsonify({"status": "book updated"})


@app.route("/books/<int:isbn>", methods=["PATCH"])
def update_book(isbn):
    request_data = request.get_json()

    for book in books:
        if book["isbn"] == isbn:
            book["name"] = request_data["name"]

    response = Response("", status=201, mimetype='application/json')
    return response


@app.route("/books/<int:isbn>", methods=["DELETE"])
def delete_book(isbn):
    for book in range(len(books)):
        if books[book]["isbn"] == isbn:
            del books[book]

    response = Response("", status=201, mimetype='application/json')
    return response


app.run(port=8000)

