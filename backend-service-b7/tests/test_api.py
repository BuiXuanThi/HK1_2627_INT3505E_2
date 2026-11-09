import pytest
from sqlalchemy import event
from sqlalchemy.exc import OperationalError

from app import create_app
from app.extensions import db

PRODUCTS = "/api/v1/products"
ORDERS = "/api/v1/orders"


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.engine.dispose()


@pytest.fixture
def client(app):
    return app.test_client()


def product(client, sku, stock=10):
    response = client.post(PRODUCTS, json={
        "sku": sku, "name": sku, "price_cents": 1200, "qty_in_stock": stock,
    })
    assert response.status_code == 201
    assert client.get(response.headers["Location"]).status_code == 200
    return response.json["id"]


def test_product_lifecycle(client):
    first = product(client, "AAA")
    second = product(client, "BBB")
    detail = f"{PRODUCTS}/{first}"
    page = client.get(PRODUCTS, query_string={"page": 2, "size": 1}).json
    assert (page["total"], page["page"], page["size"]) == (2, 2, 1)
    assert page["items"][0]["id"] == second
    response = client.patch(detail, json={"name": "Updated"})
    assert response.json["name"] == "Updated"
    assert response.json["price_cents"] == 1200
    assert client.post(f"{detail}/reserve", json={"qty": 7}).json["qty_in_stock"] == 3
    conflict = client.post(f"{detail}/reserve", json={"qty": 4})
    assert conflict.status_code == 409
    assert client.get(detail).json["qty_in_stock"] == 3
    assert client.delete(detail).status_code == 204
    assert client.get(detail).status_code == 404
    assert client.post(f"{detail}/reserve", json={"qty": 1}).status_code == 404
    assert client.get(PRODUCTS).json["total"] == 1


def test_product_validation_and_duplicate(client):
    product(client, "AAA")
    payload = {"sku": "AAA", "name": "Duplicate", "price_cents": 0}
    duplicate = client.post(PRODUCTS, json=payload)
    assert duplicate.status_code == 409
    assert set(duplicate.json) == {"error", "detail"}
    for invalid in (-1, True, 0.5, "1200"):
        assert client.post(PRODUCTS, json={**payload, "price_cents": invalid}).status_code == 422
    assert client.post(PRODUCTS, json=[]).status_code == 422
    assert client.get(PRODUCTS, query_string={"page": "bad"}).status_code == 422
    response = client.post(PRODUCTS, json={**payload, "sku": "CCC"})
    assert response.json["qty_in_stock"] == 0


def test_order_creation_and_rollback(client):
    first = product(client, "AAA")
    second = product(client, "BBB")
    items = [{"product_id": first, "qty": 2}, {"product_id": second, "qty": 3}]
    rejected = client.post(ORDERS, json={"items": [items[0], {**items[1], "qty": 11}]})
    assert rejected.status_code == 409
    assert client.get(f"{PRODUCTS}/{first}").json["qty_in_stock"] == 10
    assert client.get(ORDERS).json == {"items": []}
    assert client.post(ORDERS, json={"items": [items[0], items[0]]}).status_code == 422
    response = client.post(ORDERS, json={"items": items})
    assert response.status_code == 201
    assert [(i["product_id"], i["qty"], i["unit_price_cents"]) for i in response.json["items"]] == [
        (first, 2, 1200), (second, 3, 1200)
    ]
    assert client.get(f"{PRODUCTS}/{first}").json["qty_in_stock"] == 8
    client.patch(f"{PRODUCTS}/{first}", json={"price_cents": 1500})
    client.delete(f"{PRODUCTS}/{second}")
    assert client.get(response.headers["Location"]).json["items"] == response.json["items"]


def test_orders_eager_loading_has_constant_query_count(app, client):
    def add_order(start):
        ids = [product(client, f"SKU-{n}") for n in range(start, start + 2)]
        response = client.post(ORDERS, json={"items": [
            {"product_id": id, "qty": 1} for id in ids
        ]})
        assert response.status_code == 201

    def assert_order_queries(expected_count):
        statements = []

        def count(connection, cursor, statement, parameters, context, executemany):
            statements.append(statement)

        with app.app_context():
            engine = db.engine
        event.listen(engine, "before_cursor_execute", count)
        try:
            response = client.get(ORDERS)
        finally:
            event.remove(engine, "before_cursor_execute", count)
        assert response.status_code == 200
        assert len(response.json["items"]) == expected_count
        assert all(len(order["items"]) == 2 for order in response.json["items"])
        assert all(item["product"]["sku"] for order in response.json["items"] for item in order["items"])
        assert len(statements) == 2

    add_order(0)
    assert_order_queries(1)
    for start in (2, 4, 6):
        add_order(start)
    assert_order_queries(4)


def test_health_checks_independent(app, client, monkeypatch):
    assert client.get("/healthz").json == {"status": "ok"}
    assert client.get("/ready").json == {"status": "ready"}

    def unavailable():
        raise OperationalError("SELECT 1", {}, OSError("database unavailable"))

    with app.app_context():
        monkeypatch.setattr(db.engine, "connect", unavailable)
    assert client.get("/healthz").status_code == 200
    assert client.get("/ready").status_code == 503

