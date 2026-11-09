from flask import Blueprint, current_app
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ..extensions import db

ready_bp = Blueprint("ready", __name__)


@ready_bp.get("/ready")
def ready():
    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        current_app.logger.warning("Database readiness check failed", exc_info=True)
        return {"error": "not_ready", "detail": "Database unavailable"}, 503
    return {"status": "ready"}
