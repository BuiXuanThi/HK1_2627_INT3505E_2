from flask import Flask, jsonify, request, render_template_string
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from marshmallow import Schema, fields

app = Flask(__name__)

BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "year": 2008},
    {"id": 2, "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann", "year": 2017},
]

class BookSchema(Schema):
    id = fields.Int(dump_only=True, metadata={"example": 1})
    title = fields.Str(required=True, metadata={"example": "Clean Code"})
    author = fields.Str(required=True, metadata={"example": "Robert C. Martin"})
    year = fields.Int(required=True, metadata={"example": 2008})

class CreateBookSchema(Schema):
    title = fields.Str(required=True, metadata={"example": "Refactoring"})
    author = fields.Str(required=True, metadata={"example": "Martin Fowler"})
    year = fields.Int(required=True, metadata={"example": 2018})

@app.get("/books")
def list_books():
    return jsonify(BOOKS), 200

@app.post("/books")
def create_book():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    title, author, year = data.get("title"), data.get("author"), data.get("year")
    if not title or not author or not isinstance(year, int):
        return jsonify({"error": "title and author are required; year must be an integer"}), 422

    book = {
        "id": max((b["id"] for b in BOOKS), default=0) + 1,
        "title": title, "author": author, "year": year
    }
    BOOKS.append(book)
    response = jsonify(book)
    response.status_code = 201
    response.headers["Location"] = f"/books/{book['id']}"
    return response

spec = APISpec(
    title="Books API",
    version="1.0.0",
    openapi_version="3.0.3",
    info={"description": "Existing Flask Books API documented with OpenAPI and Swagger UI."},
    plugins=[MarshmallowPlugin()],
)
spec.components.schema("Book", schema=BookSchema)
spec.components.schema("CreateBook", schema=CreateBookSchema)

spec.path(path="/books", operations={
    "get": {
        "tags": ["books"], "operationId": "listBooks", "summary": "Get all books",
        "responses": {"200": {"description": "A list of books", "content": {
            "application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Book"}}}
        }}}
    },
    "post": {
        "tags": ["books"], "operationId": "createBook", "summary": "Create a new book",
        "requestBody": {"required": True, "content": {"application/json": {
            "schema": {"$ref": "#/components/schemas/CreateBook"}
        }}},
        "responses": {
            "201": {"description": "Book created successfully", "content": {"application/json": {
                "schema": {"$ref": "#/components/schemas/Book"}
            }}},
            "400": {"description": "Invalid JSON body"},
            "422": {"description": "Missing or invalid fields"}
        }
    }
})

@app.get("/openapi.json")
def openapi_json():
    return jsonify(spec.to_dict()), 200

SWAGGER_UI_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Books API - Swagger UI</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = () => SwaggerUIBundle({
      url: "/openapi.json",
      dom_id: "#swagger-ui"
    });
  </script>
</body>
</html>
"""

@app.get("/docs")
def docs():
    return render_template_string(SWAGGER_UI_HTML)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
