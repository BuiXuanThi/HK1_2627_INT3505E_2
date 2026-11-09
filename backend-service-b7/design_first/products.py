
from flask import jsonify

products = [
    {"id": 1, "name": "Laptop", "price": 1500},
    {"id": 2, "name": "Mouse", "price": 20}
]

def list_products():
    return jsonify(products), 200

def create_product(body):
    product = {
        "id": len(products) + 1,
        **body
    }
    products.append(product)
    return jsonify(product), 201
