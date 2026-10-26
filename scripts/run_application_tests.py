"""Run original Module 7 application tests from the correct working directory.

Running pytest from the handoff folder may not import the app's `src` package.
Use the current interpreter in application/ so the original source stays intact.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    app = ROOT / "application"
    if not (app / "src" / "monitor.py").is_file() or not (app / "tests").is_dir():
        print("Application tests unavailable: first run scripts/prepare_application.py", file=sys.stderr)
        raise SystemExit(2)
    print("Running original application regression tests from application/", flush=True)
    raise SystemExit(subprocess.call([sys.executable, "-m", "pytest", "-q"], cwd=app))


if __name__ == "__main__":
    main()
