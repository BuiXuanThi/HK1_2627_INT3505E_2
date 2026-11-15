"""Lab 4: seed ~50 sample books (with year) before running Locust.

Why: a fresh DB is empty, so GET /books/{id} (ids 1..50) is almost all 404
and GET /books?year= always returns []. With data, the measurement reflects
the real 200 path.

Usage (server must be running, DB should still be empty):
    python performance/seed.py --host http://127.0.0.1:5000

Idempotent: if GET /books/50 already returns 200, seeding is skipped.
Standard library only, nothing extra to install.
"""
import argparse
import json
import sys
import urllib.error
import urllib.request

COUNT = 50  # khớp random.randint(1, 50) trong locustfile.py
AUTHORS = ["Alice", "Bob", "Carol", "Dave", "Erin"]


def request(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url, data=data, method=method, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            return res.status
    except urllib.error.HTTPError as exc:
        return exc.code


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--host", default="http://127.0.0.1:5000")
    args = parser.parse_args()
    host = args.host.rstrip("/")

    if request("GET", f"{host}/books/{COUNT}") == 200:
        print(f"Book id={COUNT} already exists, skipping seed.")
        return 0

    created = 0
    for i in range(COUNT):
        book = {
            "title": f"Seed book {i + 1}",
            "author": AUTHORS[i % len(AUTHORS)],
            # 50 sách rải trên 1990..2024 để mọi query ?year= có cơ hội khớp
            "year": 1990 + (i * 11) % 35,
        }
        status = request("POST", f"{host}/books", book)
        if status != 201:
            print(f"POST failed at book {i + 1}: HTTP {status}", file=sys.stderr)
            return 1
        created += 1
    print(f"Created {created} books.")
    return 0


if __name__ == "__main__":
    sys.exit(main())