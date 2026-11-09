from marshmallow import Schema, ValidationError, fields, validate, validates_schema

INT_MAX = 2**31 - 1


class ProductOut(Schema):
    id = fields.Int()
    sku = fields.Str()
    name = fields.Str()
    description = fields.Str(allow_none=True)
    price_cents = fields.Int()
    qty_in_stock = fields.Int()
    archived = fields.Bool()


class ProductIn(Schema):
    sku = fields.Str(required=True, validate=validate.Length(min=3, max=32))
    name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(allow_none=True, validate=validate.Length(max=2000))
    price_cents = fields.Int(required=True, strict=True, validate=validate.Range(0, INT_MAX))
    qty_in_stock = fields.Int(load_default=0, strict=True, validate=validate.Range(0, INT_MAX))


class ProductPatch(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=255))
    price_cents = fields.Int(strict=True, validate=validate.Range(0, INT_MAX))


class ReserveIn(Schema):
    qty = fields.Int(required=True, strict=True, validate=validate.Range(1, INT_MAX))


class OrderItemIn(ReserveIn):
    product_id = fields.Int(required=True, strict=True, validate=validate.Range(1, INT_MAX))


class OrderIn(Schema):
    items = fields.List(fields.Nested(OrderItemIn), required=True, validate=validate.Length(min=1))

    @validates_schema
    def unique_products(self, data, **kwargs):
        ids = [item["product_id"] for item in data["items"]]
        if len(set(ids)) != len(ids):
            raise ValidationError({"items": ["Each product may appear only once."]})


class OrderItemOut(Schema):
    product_id = fields.Int()
    qty = fields.Int()
    unit_price_cents = fields.Int()
    product = fields.Nested(ProductOut, only=("id", "sku", "name"))


class OrderOut(Schema):
    id = fields.Int()
    created_at = fields.DateTime()
    items = fields.List(fields.Nested(OrderItemOut))
