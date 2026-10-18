import sys
from pathlib import Path

import pytest

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from app import create_app
from models import db, Book

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.drop_all()
        db.create_all()

        books = [
            Book(
                title="Clean Code",
                isbn="9780132350884",
                genre="Programming",
                price_vnd=450000,
                stock=10
            ),
            Book(
                title="Design Patterns",
                isbn="9780201633610",
                genre="Programming",
                price_vnd=520000,
                stock=8
            ),
            Book(
                title="Fluent Python",
                isbn="9781492056355",
                genre="Programming",
                price_vnd=600000,
                stock=6
            ),
            Book(
                title="Learning SQL",
                isbn="9781492057611",
                genre="Database",
                price_vnd=400000,
                stock=7
            ),
            Book(
                title="Database System Concepts",
                isbn="9780078022159",
                genre="Database",
                price_vnd=700000,
                stock=5
            ),
            Book(
                title="Computer Networks",
                isbn="9780132126953",
                genre="Networking",
                price_vnd=650000,
                stock=4
            )
        ]

        db.session.add_all(books)
        db.session.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_offset_pagination(client):
    response = client.get(
        "/api/v1/books?strategy=offset&offset=0&limit=2"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["data"]) == 2
    assert data["page"]["strategy"] == "offset"
    assert data["page"]["offset"] == 0
    assert data["page"]["limit"] == 2
    assert data["page"]["total"] == 6


def test_offset_second_page(client):
    response = client.get(
        "/api/v1/books?strategy=offset&offset=2&limit=2"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["data"]) == 2
    assert data["page"]["offset"] == 2


def test_genre_filter(client):
    response = client.get(
        "/api/v1/books?strategy=offset&genre=Programming"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["data"]) == 3

    for book in data["data"]:
        assert book["genre"] == "Programming"


def test_multi_key_sort(client):
    response = client.get(
        "/api/v1/books?strategy=offset&sort=genre,price"
    )

    assert response.status_code == 200

    data = response.get_json()

    books = data["data"]

    actual = [
        (book["genre"], book["price_vnd"])
        for book in books
    ]

    assert actual == sorted(actual)


def test_cursor_first_page(client):
    response = client.get(
        "/api/v1/books?strategy=cursor&limit=2&sort=price,id"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["data"]) == 2
    assert data["page"]["strategy"] == "cursor"
    assert data["page"]["more"] is True
    assert data["page"]["next"] is not None


def test_cursor_next_page(client):
    first_response = client.get(
        "/api/v1/books?strategy=cursor&limit=2&sort=price,id"
    )

    first_data = first_response.get_json()

    cursor = first_data["page"]["next"]

    second_response = client.get(
        f"/api/v1/books"
        f"?strategy=cursor"
        f"&limit=2"
        f"&sort=price,id"
        f"&cursor={cursor}"
    )

    assert second_response.status_code == 200

    second_data = second_response.get_json()

    first_ids = {
        book["id"]
        for book in first_data["data"]
    }

    second_ids = {
        book["id"]
        for book in second_data["data"]
    }

    assert first_ids.isdisjoint(second_ids)


def test_invalid_strategy(client):
    response = client.get(
        "/api/v1/books?strategy=abc"
    )

    assert response.status_code == 400


def test_invalid_sort(client):
    response = client.get(
        "/api/v1/books?sort=unknown"
    )

    assert response.status_code == 400


def test_invalid_offset(client):
    response = client.get(
        "/api/v1/books?strategy=offset&offset=-1"
    )

    assert response.status_code == 400