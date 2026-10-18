import json
from pathlib import Path

from flask import Blueprint, jsonify, request
from jsonschema import validate, ValidationError

from models import db, Book


books_bp = Blueprint(
    "books",
    __name__,
    url_prefix="/api/v1/books"
)


# Load JSON Schema
SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "book.json"

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    BOOK_SCHEMA = json.load(f)


@books_bp.get("")
def list_books():
    books = db.session.query(Book).all()

    return jsonify([
        book.to_dict()
        for book in books
    ]), 200


@books_bp.get("/<int:book_id>")
def get_book(book_id):
    book = db.session.get(Book, book_id)

    if book is None:
        return jsonify({
            "error": "Book not found"
        }), 404

    return jsonify(book.to_dict()), 200


@books_bp.post("")
def create_book():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Invalid JSON body"
        }), 400

    try:
        validate(
            instance=data,
            schema=BOOK_SCHEMA
        )
    except ValidationError as e:
        return jsonify({
            "error": "Validation failed",
            "message": e.message
        }), 400

    book = Book(
        title=data["title"],
        isbn=data["isbn"],
        price_vnd=data["price_vnd"],
        stock=data.get("stock", 0),
        category_id=data.get("category_id")
    )

    db.session.add(book)
    db.session.commit()

    return jsonify(book.to_dict()), 201


@books_bp.put("/<int:book_id>")
def update_book(book_id):
    book = db.session.get(Book, book_id)

    if book is None:
        return jsonify({
            "error": "Book not found"
        }), 404

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Invalid JSON body"
        }), 400

    try:
        validate(
            instance=data,
            schema=BOOK_SCHEMA
        )
    except ValidationError as e:
        return jsonify({
            "error": "Validation failed",
            "message": e.message
        }), 400

    book.title = data["title"]
    book.isbn = data["isbn"]
    book.price_vnd = data["price_vnd"]
    book.stock = data.get("stock", 0)
    book.category_id = data.get("category_id")

    db.session.commit()

    return jsonify(book.to_dict()), 200


@books_bp.delete("/<int:book_id>")
def delete_book(book_id):
    book = db.session.get(Book, book_id)

    if book is None:
        return jsonify({
            "error": "Book not found"
        }), 404

    db.session.delete(book)
    db.session.commit()

    return "", 204