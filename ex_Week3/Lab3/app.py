from flask import Flask, request, jsonify

app = Flask(__name__)

ORDERS = [
    {"id": 1, "customer_id": 1, "status": "paid", "total": 120},
    {"id": 2, "customer_id": 1, "status": "pending", "total": 80},
    {"id": 3, "customer_id": 2, "status": "paid", "total": 200},
    {"id": 4, "customer_id": 2, "status": "cancelled", "total": 50},
    {"id": 5, "customer_id": 3, "status": "paid", "total": 300},
    {"id": 6, "customer_id": 3, "status": "pending", "total": 150},
]


@app.route("/orders", methods=["GET"])
def get_orders():
    result = ORDERS.copy()

    status = request.args.get("status")
    if status:
        result = [
            order for order in result
            if order["status"].lower() == status.lower()
        ]

    customer_id = request.args.get("customer_id")
    if customer_id:
        try:
            customer_id = int(customer_id)
        except ValueError:
            return jsonify({
                "error": "Invalid customer_id"
            }), 400

        result = [
            order for order in result
            if order["customer_id"] == customer_id
        ]

    sort = request.args.get("sort")

    if sort:
        reverse = False

        if sort.startswith("-"):
            reverse = True
            sort = sort[1:]

        allowed_fields = ["id", "customer_id", "status", "total"]

        if sort not in allowed_fields:
            return jsonify({
                "error": f"Cannot sort by '{sort}'"
            }), 400

        result.sort(
            key=lambda x: x[sort],
            reverse=reverse
        )


    cursor = request.args.get("cursor")

    if cursor:
        try:
            cursor = int(cursor)
        except ValueError:
            return jsonify({
                "error": "Invalid cursor"
            }), 400

        result = [
            order for order in result
            if order["id"] > cursor
        ]


    limit = request.args.get("limit")

    if limit:
        try:
            limit = int(limit)
        except ValueError:
            return jsonify({
                "error": "Invalid limit"
            }), 400

        result = result[:limit]

    fields = request.args.get("fields")

    if fields:
        selected_fields = [
            field.strip()
            for field in fields.split(",")
        ]

        result = [
            {
                key: value
                for key, value in order.items()
                if key in selected_fields
            }
            for order in result
        ]

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)