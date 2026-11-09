
from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields, validate

# 1. Data giả lập
products = [
    {"id": 1, "name": "Laptop", "price": 1500},
    {"id": 2, "name": "Mouse", "price": 20}
]

# 2. Schema: định nghĩa dữ liệu
class ProductIn(Schema):
    name = fields.Str(required=True)
    price = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

class ProductOut(Schema):
    id = fields.Int()
    name = fields.Str()
    price = fields.Int()

# 3. Blueprint: khai báo API
blp = Blueprint(
    "products",
    __name__,
    url_prefix="/products",
    description="Product operations"
)

@blp.route("/")
class ProductList(MethodView):

    @blp.response(200, ProductOut(many=True))
    def get(self):
        return products

    @blp.arguments(ProductIn)
    @blp.response(201, ProductOut)
    def post(self, data):
        product = {
            "id": len(products) + 1,
            **data
        }
        products.append(product)
        return product

# 4. Khởi tạo Flask
app = Flask(__name__)

app.config.update(
    API_TITLE="Product API - Code First",
    API_VERSION="v1",
    OPENAPI_VERSION="3.0.3",
    OPENAPI_URL_PREFIX="/",
    OPENAPI_SWAGGER_UI_PATH="/docs",
    OPENAPI_SWAGGER_UI_URL=(
        "https://cdn.jsdelivr.net/npm/"
        "swagger-ui-dist/"
    )
)

api = Api(app)
api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
