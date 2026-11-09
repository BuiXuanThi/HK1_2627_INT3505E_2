from flask import Blueprint, abort, request, url_for
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..models import Product
from ..schemas import INT_MAX, ProductIn, ProductOut, ProductPatch, ReserveIn

products_bp = Blueprint("products", __name__, url_prefix="/api/v1/products")
active_products = select(Product).where(Product.archived.is_(False))


def active_product(id):
    return db.first_or_404(active_products.where(Product.id == id))


def reserve_stock(id, qty):
    # UPDATE atomically checks stock and obtains the current price in the same transaction.
    product = db.session.scalars(
        update(Product)
        .where(Product.id == id, Product.archived.is_(False), Product.qty_in_stock >= qty)
        .values(qty_in_stock=Product.qty_in_stock - qty)
        .returning(Product),
        execution_options={"populate_existing": True},
    ).one_or_none()
    if product is None:
        active_product(id)
        abort(409, description="Insufficient stock")
    return product


@products_bp.get("")
def list_products():
    try:
        page = max(1, int(request.args.get("page", 1)))
        size = min(100, max(1, int(request.args.get("size", 20))))
    except ValueError:
        abort(422, description="page and size must be integers")
    if page > INT_MAX:
        abort(422, description="page is out of range")
    result = db.paginate(
        active_products.order_by(Product.id), page=page, per_page=size, error_out=False
    )
    return {
        "items": ProductOut(many=True).dump(result.items),
        "page": page,
        "size": size,
        "total": result.total,
    }


@products_bp.get("/<int:id>")
def get_product(id):
    return ProductOut().dump(active_product(id))


@products_bp.post("")
def create_product():
    product = Product(**ProductIn().load(request.get_json()))
    db.session.add(product)
    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        if db.session.scalar(select(Product.id).where(Product.sku == product.sku)) is not None:
            abort(409, description="SKU already exists")
        raise
    body = ProductOut().dump(product)
    db.session.commit()
    return body, 201, {"Location": url_for(".get_product", id=product.id)}


@products_bp.post("/<int:id>/reserve")
def reserve_product(id):
    data = ReserveIn().load(request.get_json())
    body = ProductOut().dump(reserve_stock(id, data["qty"]))
    db.session.commit()
    return body


@products_bp.patch("/<int:id>")
def patch_product(id):
    changes = ProductPatch().load(request.get_json())
    if not changes:
        return ProductOut().dump(active_product(id))
    product = db.session.scalars(
        update(Product)
        .where(Product.id == id, Product.archived.is_(False))
        .values(**changes)
        .returning(Product)
    ).one_or_none()
    if product is None:
        abort(404)
    body = ProductOut().dump(product)
    db.session.commit()
    return body


@products_bp.delete("/<int:id>")
def delete_product(id):
    result = db.session.execute(
        update(Product)
        .where(Product.id == id, Product.archived.is_(False))
        .values(archived=True)
    )
    if result.rowcount == 0:
        abort(404)
    db.session.commit()
    return "", 204
