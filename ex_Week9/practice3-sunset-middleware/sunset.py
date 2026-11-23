"""
sunset.py – Decorator tái sử dụng @deprecate_at theo chuẩn RFC 8594

Gắn vào bất kỳ Flask route nào để tự động:
  • Trước sunset_date  → thêm headers Sunset / Deprecation / Link, ghi log WARNING.
  • Từ sunset_date trở đi → trả 410 Gone kèm hướng dẫn chuyển endpoint
"""

import logging
from datetime import datetime, timezone
from email.utils import format_datetime
from functools import wraps

from flask import jsonify, request

log = logging.getLogger("sunset")


# ── Tiện ích ─────────────────────────────────────────────────────────
def http_date(dt: datetime) -> str:
    """Format datetime thành HTTP-date chuẩn RFC 7231 (GMT)."""
    return format_datetime(dt, usegmt=True)


# ── Decorator ────────────────────────────────────────────────────────
def deprecate_at(sunset_date: datetime, replacement: str | None = None):
    """
    Decorator đánh dấu endpoint sẽ ngừng hỗ trợ từ `sunset_date`

    Parameters
    ----------
    sunset_date : datetime (timezone-aware, UTC)
        Thời điểm endpoint chính thức bị ngừng phục vụ
    replacement : str, optional
        Đường dẫn endpoint thay thế (hiển thị trong header Link
        và trong body 410)
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            now = datetime.now(timezone.utc)

            # ── Đã quá hạn → 410 Gone ───────────────────────────
            if now >= sunset_date:
                return (
                    jsonify(
                        {
                            "error": "gone",
                            "sunset": http_date(sunset_date),
                            "use_instead": replacement,
                        }
                    ),
                    410,
                )

            # ── Chưa quá hạn → phục vụ bình thường + headers ────
            result = fn(*args, **kwargs)

            # Hỗ trợ cả dict lẫn tuple (dict, status_code)
            if isinstance(result, tuple):
                body, status = result
            else:
                body, status = result, 200

            r = jsonify(body)
            r.status_code = status
            r.headers["Sunset"] = http_date(sunset_date)
            r.headers["Deprecation"] = "true"
            if replacement:
                r.headers["Link"] = f'<{replacement}>; rel="successor-version"'

            # Ghi log cảnh báo
            log.warning(
                "deprecated_call %s %s", request.path, request.remote_addr
            )

            return r

        return wrapper

    return decorator
