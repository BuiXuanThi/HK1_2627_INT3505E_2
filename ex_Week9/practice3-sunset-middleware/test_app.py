"""Quick smoke tests using Flask test client"""
from app import app

c = app.test_client()

# ── Test 1: v1 chưa hết hạn → 200 + Sunset headers ──────────────────
print("=== Test 1: GET /api/v1/users/1  (chưa hết hạn) ===")
r = c.get("/api/v1/users/1")
print(f"Status     : {r.status_code}")
print(f"Sunset     : {r.headers.get('Sunset')}")
print(f"Deprecation: {r.headers.get('Deprecation')}")
print(f"Link       : {r.headers.get('Link')}")
print(f"Body       : {r.get_json()}")
assert r.status_code == 200
assert r.headers["Sunset"] is not None
assert r.headers["Deprecation"] == "true"
assert 'rel="successor-version"' in r.headers["Link"]
assert r.get_json()["full_name"] == "Văn Nguyễn"
print("PASSED\n")

# ── Test 2: v0 đã hết hạn → 410 Gone ────────────────────────────────
print("=== Test 2: GET /api/v0/users/1  (đã hết hạn) ===")
r = c.get("/api/v0/users/1")
print(f"Status : {r.status_code}")
print(f"Body   : {r.get_json()}")
assert r.status_code == 410
body = r.get_json()
assert body["error"] == "gone"
assert body["use_instead"] == "/api/v2/users"
assert "2025" in body["sunset"]
print("PASSED\n")

# ── Test 3: v2 endpoint mới → 200, không có Sunset headers ──────────
print("=== Test 3: GET /api/v2/users/1  (endpoint mới) ===")
r = c.get("/api/v2/users/1")
print(f"Status     : {r.status_code}")
print(f"Sunset     : {r.headers.get('Sunset')}")
print(f"Body       : {r.get_json()}")
assert r.status_code == 200
assert r.headers.get("Sunset") is None
assert r.headers.get("Deprecation") is None
assert r.get_json()["email"] == "a@vnu.vn"
print("PASSED\n")

# ── Test 4: v1 user không tồn tại → 404 + Sunset headers ────────────
print("=== Test 4: GET /api/v1/users/999  (not found, chưa hết hạn) ===")
r = c.get("/api/v1/users/999")
print(f"Status     : {r.status_code}")
print(f"Sunset     : {r.headers.get('Sunset')}")
print(f"Deprecation: {r.headers.get('Deprecation')}")
print(f"Body       : {r.get_json()}")
assert r.status_code == 404
assert r.headers["Sunset"] is not None
assert r.headers["Deprecation"] == "true"
assert r.get_json()["error"] == "not found"
print("PASSED\n")

# ── Test 5: v2 user không tồn tại → 404, không Sunset ───────────────
print("=== Test 5: GET /api/v2/users/999  (not found, endpoint mới) ===")
r = c.get("/api/v2/users/999")
print(f"Status : {r.status_code}")
print(f"Body   : {r.get_json()}")
assert r.status_code == 404
assert r.headers.get("Sunset") is None
print("PASSED\n")

print("ALL TESTS PASSED!")
