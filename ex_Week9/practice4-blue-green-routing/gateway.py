"""
gateway.py – Logic định tuyến 3 tầng (Blue-Green routing)

Ưu tiên kiểm tra:
  1. Header X-Cohort (beta / internal)  → v2
  2. Account allow-list                 → v2
  3. Deterministic % bucket (MD5 hash)  → v2 nếu < V2_PERCENT
"""

import hashlib

from flask import request

from handlers import v1_create_order, v2_create_order

# ── Cấu hình mặc định ───────────────────────────────────────────────
V2_PERCENT = 5                              # % lưu lượng chuyển sang v2
V2_COHORTS = {"beta", "internal"}           # cohort header luôn route v2
V2_FORCE_ACCOUNTS = {"acct_42", "acct_99"}  # account luôn route v2


def route_to_v2(body: dict) -> bool:
    """Quyết định request có được route sang v2 hay không."""

    # Ưu tiên 1: Header explicit cohort
    cohort = request.headers.get("X-Cohort", "").lower()
    if cohort in V2_COHORTS:
        return True

    # Ưu tiên 2: Account allow-list
    acct = body.get("account_id", "")
    if acct in V2_FORCE_ACCOUNTS:
        return True

    # Ưu tiên 3: Deterministic percentage bucket
    if V2_PERCENT == 0:
        return False
    if not acct:
        return False
    h = int(hashlib.md5(acct.encode()).hexdigest(), 16)
    return h % 100 < V2_PERCENT


def dispatch(body: dict) -> tuple[str, dict]:
    """Điều hướng request tới handler phù hợp

    Returns
    -------
    (which, result) – ``which`` là ``"v1"`` hoặc ``"v2"``,
                       ``result`` là dict body trả về client
    """
    if route_to_v2(body):
        return "v2", v2_create_order(body)
    return "v1", v1_create_order(body)
