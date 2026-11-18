from flask import Flask, send_from_directory
from blueprints.v1 import bp as v1_bp
from blueprints.v2 import bp as v2_bp

app = Flask(__name__)
app.json.ensure_ascii = False
app.register_blueprint(v1_bp, url_prefix="/api/v1/users")
app.register_blueprint(v2_bp, url_prefix="/api/v2/users")

@app.route("/openapi.yaml")
def openapi_spec():
    return send_from_directory(".", "openapi.yaml", mimetype="application/yaml")

@app.route("/docs")
def docs():
    return """<!doctype html>
<html><head><title>Users API</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui.css">
</head><body><div id="ui"></div>
<script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.17.14/swagger-ui-bundle.js"></script>
<script>SwaggerUIBundle({url: "/openapi.yaml", dom_id: "#ui"});</script>
</body></html>"""

if __name__ == "__main__":
    app.run(debug=True)