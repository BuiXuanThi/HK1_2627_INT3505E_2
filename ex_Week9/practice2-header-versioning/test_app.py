"""Quick smoke tests using Flask test client"""
from app import app

c = app.test_client()

print("=== Test 1: No header (default v2) ===")
r = c.get("/users/1")
print(f"Status: {r.status_code}")
print(f"X-API-Version-Served: {r.headers.get('X-API-Version-Served')}")
print(f"Body: {r.get_json()}")
assert r.status_code == 200
assert r.headers["X-API-Version-Served"] == "2"
assert "first_name" in r.get_json()
print()

print("=== Test 2: X-API-Version: 1 ===")
r = c.get("/users/1", headers={"X-API-Version": "1"})
print(f"Status: {r.status_code}")
print(f"X-API-Version-Served: {r.headers.get('X-API-Version-Served')}")
print(f"Body: {r.get_json()}")
assert r.status_code == 200
assert r.headers["X-API-Version-Served"] == "1"
assert "full_name" in r.get_json()
print()

print("=== Test 3: X-API-Version: 2024-06-20 ===")
r = c.get("/users/1", headers={"X-API-Version": "2024-06-20"})
print(f"Status: {r.status_code}")
print(f"X-API-Version-Served: {r.headers.get('X-API-Version-Served')}")
print(f"Body: {r.get_json()}")
assert r.status_code == 200
assert r.headers["X-API-Version-Served"] == "2024-06-20"
assert "email" in r.get_json()
print()

print("=== Test 4: X-API-Version: 99 (unsupported) ===")
r = c.get("/users/1", headers={"X-API-Version": "99"})
print(f"Status: {r.status_code}")
print(f"Body: {r.get_json()}")
assert r.status_code == 400
assert r.get_json()["error"] == "unsupported version"
print()

print("=== Test 5: User not found (404) ===")
r = c.get("/users/999")
print(f"Status: {r.status_code}")
print(f"X-API-Version-Served: {r.headers.get('X-API-Version-Served')}")
print(f"Body: {r.get_json()}")
assert r.status_code == 404
assert r.headers["X-API-Version-Served"] == "2"
assert r.get_json()["error"] == "not found"
print()

print("ALL TESTS PASSED!")
