from flask import Blueprint, request
from .users_data import get_user, create_user

bp = Blueprint("v2", __name__)

@bp.route("/<int:uid>")
def get(uid):
    u = get_user(uid)
    if not u:
        return {"error": "nf"}, 404
    return {
        "id": uid,
        "first_name": u["first_name"],
        "last_name": u["last_name"],
        "email": u["email"],
    }

@bp.route("/", methods=["POST"])
def create():
    data = request.get_json(silent=True) or {}
    required = ["first_name", "last_name", "email"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return {"error": "missing fields", "fields": missing}, 400

    new_id = create_user(data["first_name"], data["last_name"], data["email"])
    return {
        "id": new_id,
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "email": data["email"],
    }, 201