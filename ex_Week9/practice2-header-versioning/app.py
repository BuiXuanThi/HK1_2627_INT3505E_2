"""
Practice 2 – Header Versioning với decorator @api_version (Flask)
Client chọn phiên bản qua header  X-API-Version
Server phản hồi kèm header  X-API-Version-Served
"""

from functools import wraps
from flask import Flask, request, jsonify

app = Flask(__name__)

# ── Cấu hình version ────
LATEST = "2"                            # mặc định khi client không gửi header
SUPPORTED = {"1", "2", "2024-06-20"}    # tập phiên bản được hỗ trợ

# ── Dữ liệu mẫu ──
USERS = {
    1: {"f": "Văn",  "l": "Nguyễn", "e": "a@vnu.vn"},
    2: {"f": "Linh", "l": "Trần",   "e": "linh@vnu.vn"},
    3: {"f": "Minh", "l": "Lê",     "e": "minh@vnu.vn"},
}


# ── Decorator @api_version ───────────────────────────────────────────
def api_version(supported, default):
    """
    Decorator đọc header X-API-Version, kiểm tra tính hợp lệ,
    rồi truyền `version` làm tham số đầu tiên vào hàm route

    - Thiếu header  → dùng `default`
    - Version không thuộc `supported` → 400 (không fallback)
    - Hàm route có thể trả về dict hoặc tuple (dict, status_code);
      decorator tự đóng gói thành JSON response và gắn header
      X-API-Version-Served
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            v = request.headers.get("X-API-Version", default)

            # Từ chối version không hỗ trợ
            if v not in supported:
                return jsonify({"error": "unsupported version"}), 400

            # Gọi hàm route gốc, truyền version làm arg đầu tiên
            result = fn(v, *args, **kwargs)

            # Hỗ trợ cả dict lẫn tuple (dict, status_code)
            if isinstance(result, tuple):
                body, status_code = result
            else:
                body, status_code = result, 200

            response = jsonify(body)
            response.status_code = status_code
            response.headers["X-API-Version-Served"] = v
            return response

        return wrapper
    return decorator


# ── Endpoint ─────────────────────────────────────────────────────────
@app.route("/users/<int:uid>")
@api_version(supported=SUPPORTED, default=LATEST)
def get_user(version, uid):
    """Trả về thông tin user theo uid, schema phụ thuộc version."""
    u = USERS.get(uid)
    if u is None:
        return {"error": "not found"}, 404

    if version == "1":
        return {"id": uid, "full_name": f"{u['f']} {u['l']}"}

    # version "2" hoặc "2024-06-20" → schema mới
    return {
        "id": uid,
        "first_name": u["f"],
        "last_name":  u["l"],
        "email":      u["e"],
    }


# ── Chạy server ─────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
