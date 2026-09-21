import hashlib
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

BOOKS = [
    {
        "id": 1,
        "title": "Spring Boot in Practice",
        "author": "John Thompson",
        "price": 45.99
    },
    {
        "id": 2,
        "title": "Microservices Patterns",
        "author": "Chris Richardson",
        "price": 52.50
    },
    {
        "id": 3,
        "title": "Head First Design Patterns",
        "author": "Eric Freeman",
        "price": 37.99
    }
]


@app.get("/books/<int:bid>")
def get_book_with_etag(bid):

    book = next((b for b in BOOKS if b["id"] == bid), None)

    if book is None:
        return jsonify({"error": "book not found"}), 404

    book_string = str(book).encode("utf-8")
    etag = '"' + hashlib.md5(book_string).hexdigest() + '"'

    client_etag = request.headers.get("If-None-Match")

    if client_etag == etag:
        return "", 304

    resp = make_response(jsonify(book), 200)

    resp.headers["ETag"] = etag
    resp.headers["Cache-Control"] = "public, max-age=60"

    return resp

if __name__ == "__main__":
    app.run(debug=True)