from datetime import datetime, timezone
from email.utils import format_datetime
from flask import Blueprint, jsonify, request
import logging
from .users_data import get_user

log = logging.getLogger("sunset")
bp = Blueprint("v1", __name__, url_prefix="/users")

V1_SUNSET = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
SUCCESSOR = "/api/v2/users" 

def http_date(dt):
    return format_datetime(dt, usegmt=True)

@bp.before_request
def check_sunset():
    # Sau ngày sunset -> 410 Gone (không phải 404)
    if datetime.now(timezone.utc) >= V1_SUNSET:
        return jsonify(error="gone",
                       sunset=http_date(V1_SUNSET),
                       use_instead=SUCCESSOR), 410

@bp.after_request
def add_deprecation_headers(resp):
    resp.headers["Sunset"] = http_date(V1_SUNSET)
    resp.headers["Deprecation"] = "true"
    resp.headers["Link"] = f'<{SUCCESSOR}>; rel="successor-version"'
    log.warning("deprecated_call %s %s", request.path, request.remote_addr)
    return resp

@bp.route("/<int:uid>")
def get(uid):
    u = get_user(uid)
    if not u:
        return {"error": "nf"}, 404
    return {"id": uid,
            "full_name": f"{u['first_name']} {u['last_name']}",
            "email": u["email"]}