from flask import Blueprint

healthz_bp = Blueprint("healthz", __name__)


@healthz_bp.get("/healthz")
def healthz():
    return {"status": "ok"}
