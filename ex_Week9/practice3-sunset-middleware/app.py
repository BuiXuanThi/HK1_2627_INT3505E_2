"""
Practice 3 – Sunset middleware demo (Flask)

Ba endpoint minh hoạ 3 trạng thái vòng đời API:
  • /api/v0/users/<uid>  → đã quá hạn (410 Gone)
  • /api/v1/users/<uid>  → sắp ngừng hỗ trợ (200 + Sunset headers)
  • /api/v2/users/<uid>  → endpoint mới, không deprecation
"""

import logging
from datetime import datetime, timezone

from flask import Flask, jsonify

from sunset import deprecate_at

# ── Logging ──────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)

app = Flask(__name__)

# ── Dữ liệu mẫu ────────────────────────────────────────────────────
USERS = {
    1: {"f": "Văn",  "l": "Nguyễn", "e": "a@vnu.vn"},
    2: {"f": "Linh", "l": "Trần",   "e": "linh@vnu.vn"},
}

# ── Mốc sunset ──────────────────────────────────────────────────────
PAST_SUNSET = datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)   # đã qua
V1_SUNSET   = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)  # tương lai


# ── v0: đã hết hạn → 410 ────────────────────────────────────────────
@app.route("/api/v0/users/<int:uid>")
@deprecate_at(PAST_SUNSET, replacement="/api/v2/users")
def get_user_v0(uid):
    u = USERS.get(uid)
    if u is None:
        return {"error": "not found"}, 404
    return {"id": uid, "full_name": f"{u['f']} {u['l']}"}


# ── v1: chưa hết hạn → 200 + Sunset headers ─────────────────────────
@app.route("/api/v1/users/<int:uid>")
@deprecate_at(V1_SUNSET, replacement="/api/v2/users")
def get_user_v1(uid):
    u = USERS.get(uid)
    if u is None:
        return {"error": "not found"}, 404
    return {"id": uid, "full_name": f"{u['f']} {u['l']}"}


# ── v2: endpoint mới, không deprecation ──────────────────────────────
@app.route("/api/v2/users/<int:uid>")
def get_user_v2(uid):
    u = USERS.get(uid)
    if u is None:
        return jsonify({"error": "not found"}), 404
    return jsonify({
        "id": uid,
        "first_name": u["f"],
        "last_name":  u["l"],
        "email":      u["e"],
    })


# ── Chạy server ─────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
