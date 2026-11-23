"""
handlers.py – Business logic cho v1 và v2 order processing
"""


def v1_create_order(body: dict) -> dict:
    """Schema cũ: tạo đơn hàng cơ bản."""
    return {
        "version": "v1",
        "status": "created",
        "account_id": body.get("account_id"),
        "item": body.get("item", "default"),
    }


def v2_create_order(body: dict) -> dict:
    """Schema mới: xác nhận đơn hàng + ưu tiên xử lý"""
    return {
        "version": "v2",
        "order_status": "confirmed",
        "account_id": body.get("account_id"),
        "item": body.get("item", "default"),
        "priority_processing": True,
    }
