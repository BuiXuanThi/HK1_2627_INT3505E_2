"""LAB 1 — add your five tests here. Do not delete the smoke tests.

A. GET /books, empty database -> HTTP 200 and []
B. GET /books/9999 -> HTTP 404, JSON code == NOT_FOUND
C. POST /books with only author -> HTTP 400, errors contains title
D. POST valid book, DELETE it, GET same id -> HTTP 404
BONUS. Validate a Book response using JSON Schema; add an unknown
       field to a *copy* of the response and assert ValidationError.

Useful imports:
    from jsonschema import validate, ValidationError
    import pytest
    from tools import get_book_schema

Do not depend on test execution order. Fixtures: client, app, sample_book.
"""

"""LAB 1 — API Testing for Books API."""

import pytest
from jsonschema import validate, ValidationError

from tools import get_book_schema


# A. GET /books with an empty database -> 200 and []
def test_get_books_empty(client):
    response = client.get("/books")

    assert response.status_code == 200
    assert response.get_json() == []


# B. GET /books/9999 -> 404 and NOT_FOUND
def test_get_nonexistent_book(client):
    response = client.get("/books/9999")

    assert response.status_code == 404

    data = response.get_json()
    assert data["code"] == "NOT_FOUND"


# C. POST /books with only author -> 400 and errors contains title
def test_create_book_missing_title(client):
    response = client.post(
        "/books",
        json={
            "author": "J.K. Rowling"
        }
    )

    assert response.status_code == 400

    data = response.get_json()
    assert any(
        error["field"] == "title"
        for error in data["errors"]
    )


# D. POST valid book -> DELETE -> GET same ID -> 404
def test_create_delete_get_book(client):
    response = client.post(
        "/books",
        json={
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "year": 2008
        }
    )

    assert response.status_code == 201

    book_id = response.get_json()["id"]

    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404



