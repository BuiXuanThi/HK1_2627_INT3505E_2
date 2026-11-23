"""
Practice 4 – Blue-Green routing demo (Flask).
Endpoint duy nhất POST /orders đóng vai trò API Gateway,
điều hướng request tới v1 hoặc v2 handler theo 3 tầng ưu tiên
"""

from flask import Flask, jsonify, request

import gateway
from gateway import dispatch

app = Flask(__name__)


# ── Endpoint chính ───────────────────────────────────────────────────
@app.route("/orders", methods=["POST"])
def create_order():
    body = request.get_json(silent=True) or {}
    which, result = dispatch(body)

    resp = jsonify(result)
    resp.status_code = 201 if which == "v2" else 200
    resp.headers["X-Order-Handler"] = which
    return resp


# ── Admin endpoint: cập nhật V2_PERCENT lúc runtime ─────────────────
@app.route("/admin/config", methods=["POST"])
def admin_config():
    data = request.get_json(silent=True) or {}
    if "v2_percent" in data:
        pct = int(data["v2_percent"])
        if not 0 <= pct <= 100:
            return jsonify({"error": "v2_percent must be 0-100"}), 400
        gateway.V2_PERCENT = pct
        return jsonify({"v2_percent": pct, "message": "updated"})
    return jsonify({"error": "nothing to update"}), 400


# ── Chạy server ─────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
