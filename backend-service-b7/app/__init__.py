from pathlib import Path

from flask import Flask
from marshmallow import ValidationError
from sqlalchemy import event
from werkzeug.exceptions import HTTPException

from .api.healthz import healthz_bp
from .api.orders import orders_bp
from .api.products import products_bp
from .api.ready import ready_bp
from .config import database_config
from .extensions import db, migrate


def enable_foreign_keys(connection, record):
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_mapping(database_config())
    if config:
        app.config.update(config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        if db.engine.dialect.name == "sqlite":
            event.listen(db.engine, "connect", enable_foreign_keys)

    for blueprint in (products_bp, orders_bp, healthz_bp, ready_bp):
        app.register_blueprint(blueprint)

    @app.errorhandler(ValidationError)
    def invalid_input(error):
        return {"error": "validation_error", "detail": error.messages}, 422

    @app.errorhandler(HTTPException)
    def http_error(error):
        response = error.get_response()
        response.data = app.json.dumps({"error": error.name, "detail": error.description})
        response.content_type = "application/json"
        return response

    return app
