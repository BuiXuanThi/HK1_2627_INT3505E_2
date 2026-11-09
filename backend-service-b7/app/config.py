import os

def database_config():
    url = os.environ.get("DATABASE_URL", "sqlite:///service.db")
    options = {}
    if url.startswith("postgresql+psycopg://"):
        options = {"pool_pre_ping": True, "connect_args": {"connect_timeout": 3}}
    return {"SQLALCHEMY_DATABASE_URI": url, "SQLALCHEMY_ENGINE_OPTIONS": options}
