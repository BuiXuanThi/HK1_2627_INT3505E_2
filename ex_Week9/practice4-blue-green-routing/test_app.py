"""Quick smoke tests for Blue-Green routing using Flask test client"""
import hashlib

from app import app
import gateway

c = app.test_client()
JSON = {"Content-Type": "application/json"}

# ── Test 1: X-Cohort: beta → v2 (201) ───────────────────────────────
print("=== Test 1: X-Cohort: beta → v2 ===")
r = c.post("/orders", json={"account_id": "acct_1", "item": "widget"},
           headers={"X-Cohort": "beta"})
print(f"Status          : {r.status_code}")
print(f"X-Order-Handler : {r.headers.get('X-Order-Handler')}")
print(f"Body            : {r.get_json()}")
assert r.status_code == 201
assert r.headers["X-Order-Handler"] == "v2"
assert r.get_json()["version"] == "v2"
assert r.get_json()["priority_processing"] is True
print("PASSED\n")

# ── Test 2: Account allow-list (acct_42) → v2 (201) ─────────────────
print("=== Test 2: acct_42 (allow-list) → v2 ===")
r = c.post("/orders", json={"account_id": "acct_42", "item": "gadget"})
print(f"Status          : {r.status_code}")
print(f"X-Order-Handler : {r.headers.get('X-Order-Handler')}")
print(f"Body            : {r.get_json()}")
assert r.status_code == 201
assert r.headers["X-Order-Handler"] == "v2"
print("PASSED\n")

# ── Test 3: acct_100 ở V2_PERCENT=5 → v1 (200) ─────────────────────
# Xác minh rằng acct_100 rơi vào bucket >= 5
h = int(hashlib.md5(b"acct_100").hexdigest(), 16) % 100
print(f"(acct_100 MD5 bucket = {h}, cần >= 5 để vào v1)")
assert h >= 5, f"acct_100 bucket={h} < 5, chọn account khác để test"

gateway.V2_PERCENT = 5  # đảm bảo reset
print("=== Test 3: acct_100 @ V2_PERCENT=5 → v1 ===")
r = c.post("/orders", json={"account_id": "acct_100", "item": "thing"})
print(f"Status          : {r.status_code}")
print(f"X-Order-Handler : {r.headers.get('X-Order-Handler')}")
print(f"Body            : {r.get_json()}")
assert r.status_code == 200
assert r.headers["X-Order-Handler"] == "v1"
assert r.get_json()["version"] == "v1"
print("PASSED\n")

# ── Test 4a: Admin config → tăng V2_PERCENT lên 100 ─────────────────
print("=== Test 4a: POST /admin/config {v2_percent: 100} ===")
r = c.post("/admin/config", json={"v2_percent": 100})
print(f"Status : {r.status_code}")
print(f"Body   : {r.get_json()}")
assert r.status_code == 200
assert r.get_json()["v2_percent"] == 100
print("PASSED\n")

# ── Test 4b: Giờ acct_100 phải vào v2 ───────────────────────────────
print("=== Test 4b: acct_100 @ V2_PERCENT=100 → v2 ===")
r = c.post("/orders", json={"account_id": "acct_100", "item": "thing"})
print(f"Status          : {r.status_code}")
print(f"X-Order-Handler : {r.headers.get('X-Order-Handler')}")
print(f"Body            : {r.get_json()}")
assert r.status_code == 201
assert r.headers["X-Order-Handler"] == "v2"
assert r.get_json()["version"] == "v2"
print("PASSED\n")

# ── Test 5: X-Cohort: internal → v2 ─────────────────────────────────
gateway.V2_PERCENT = 5  # reset lại
print("=== Test 5: X-Cohort: internal → v2 ===")
r = c.post("/orders", json={"account_id": "acct_xyz"},
           headers={"X-Cohort": "Internal"})  # mixed case
print(f"Status          : {r.status_code}")
print(f"X-Order-Handler : {r.headers.get('X-Order-Handler')}")
assert r.status_code == 201
assert r.headers["X-Order-Handler"] == "v2"
print("PASSED\n")

# ── Test 6: Không có body → v1 (bucket fallback) ────────────────────
print("=== Test 6: Empty body → v1 ===")
r = c.post("/orders", json={})
print(f"Status          : {r.status_code}")
print(f"X-Order-Handler : {r.headers.get('X-Order-Handler')}")
assert r.status_code == 200
assert r.headers["X-Order-Handler"] == "v1"
print("PASSED\n")

# ── Test 7: Admin config invalid → 400 ──────────────────────────────
print("=== Test 7: Admin config v2_percent=200 → 400 ===")
r = c.post("/admin/config", json={"v2_percent": 200})
print(f"Status : {r.status_code}")
assert r.status_code == 400
print("PASSED\n")

print("ALL TESTS PASSED!")
