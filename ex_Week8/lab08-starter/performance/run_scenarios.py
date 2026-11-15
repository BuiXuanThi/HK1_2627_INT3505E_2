"""Lab 4: run the three Locust scenarios (A, B, C) and save reports.

Usage (API must be running and seeded, see performance/seed.py):
    python performance/run_scenarios.py                 # run A, B and C
    python performance/run_scenarios.py --only B        # run one scenario
    python performance/run_scenarios.py --dry-run       # print commands only

Outputs per scenario X: reports/X.html (Locust report) and reports/X_*.csv
(raw stats used to fill performance/analysis.md).
"""
import argparse
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCUSTFILE = ROOT / "performance" / "locustfile.py"
REPORTS = ROOT / "reports"

# name: (users, spawn rate, duration) - khớp bảng trong analysis.md
SCENARIOS = {
    "A": (10, 2, "30s"),
    "B": (50, 5, "60s"),
    "C": (200, 50, "30s"),
}


def http_status(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as res:
            return res.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except OSError:
        return None


def build_command(name, host):
    users, rate, duration = SCENARIOS[name]
    return [
        sys.executable, "-m", "locust",
        "-f", str(LOCUSTFILE),
        "--headless",
        "-H", host,
        "-u", str(users),
        "-r", str(rate),
        "-t", duration,
        "--html", str(REPORTS / f"{name}.html"),
        "--csv", str(REPORTS / name),
        # Locust mặc định thoát với code 1 nếu có request fail; lab này
        # cố tình có 1% fail giả lập nên không coi đó là lỗi chạy.
        "--exit-code-on-error", "0",
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--host", default="http://127.0.0.1:5000")
    parser.add_argument("--only", choices=sorted(SCENARIOS), help="run a single scenario")
    parser.add_argument("--dry-run", action="store_true", help="print commands only")
    args = parser.parse_args()
    host = args.host.rstrip("/")
    names = [args.only] if args.only else sorted(SCENARIOS)

    if not args.dry_run:
        if http_status(f"{host}/health") != 200:
            print(f"API is not reachable at {host}/health. Start it first.", file=sys.stderr)
            return 1
        if http_status(f"{host}/books/50") != 200:
            print("Warning: book id=50 not found. Run performance/seed.py first "
                  "for meaningful results.", file=sys.stderr)
        REPORTS.mkdir(exist_ok=True)

    for name in names:
        cmd = build_command(name, host)
        users, rate, duration = SCENARIOS[name]
        print(f"\n=== Scenario {name}: {users} users, spawn rate {rate}/s, {duration} ===")
        print(" ".join(cmd))
        if args.dry_run:
            continue
        result = subprocess.run(cmd, cwd=ROOT)
        if result.returncode != 0:
            print(f"Locust exited with code {result.returncode} in scenario {name}.",
                  file=sys.stderr)
            return result.returncode
    print(f"\nDone. Reports are in {REPORTS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())