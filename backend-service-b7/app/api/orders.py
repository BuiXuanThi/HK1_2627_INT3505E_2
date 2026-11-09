from flask import Blueprint, request, url_for
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..extensions import db
from ..models import Order, OrderItem
from ..schemas import OrderIn, OrderOut
from .products import reserve_stock

orders_bp = Blueprint("orders", __name__, url_prefix="/api/v1/orders")
orders_with_items = select(Order).options(selectinload(Order.items).joinedload(OrderItem.product))


@orders_bp.get("")
def list_orders():
    return {"items": OrderOut(many=True).dump(
        db.session.scalars(orders_with_items.order_by(Order.id)).all()
    )}


@orders_bp.get("/<int:id>")
def get_order(id):
    order = db.first_or_404(orders_with_items.where(Order.id == id))
    return OrderOut().dump(order)


@orders_bp.post("")
def create_order():
    data = OrderIn().load(request.get_json())
    order = Order()
    # Consistent lock ordering for orders that share products.
    for item in sorted(data["items"], key=lambda item: item["product_id"]):
        product = reserve_stock(item["product_id"], item["qty"])
        order.items.append(OrderItem(
            product=product, qty=item["qty"], unit_price_cents=product.price_cents
        ))
    db.session.add(order)
    db.session.flush()
    body = OrderOut().dump(order)
    location = url_for(".get_order", id=order.id)
    db.session.commit()
    return body, 201, {"Location": location}
