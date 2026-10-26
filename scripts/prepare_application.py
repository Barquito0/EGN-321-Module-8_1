"""Fetch the course's existing Module 7.2 app without overwriting local data.

This is a first-run bootstrap helper, NOT a substitute for the original app.
It requires Internet and git, then pins the verified baseline commit so
operator steps remain stable even when upstream main is updated later.
"""
from __future__ import annotations
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "application"
SOURCE_URL = "https://github.com/Barquito0/EGN-321-Module-7_2.git"
# Verified Module 7.2 revision with source pause/resume logging and tests.
SOURCE_REVISION = "2f8fe29c21dc5c05496c622caa893a352d9420ce"
REQUIRED = ("app.py", "supervisor.py", "requirements.txt", "src/monitor.py",
            "src/storage.py", "data/module6_sample_sensor_history.csv")


def verify_app(path: Path) -> list[str]:
    return [f for f in REQUIRED if not (path / f).is_file()]


def prepare(root=ROOT, *, runner=subprocess.run) -> Path:
    root = Path(root)
    app = root / "application"
    if app.exists():
        missing = verify_app(app)
        if missing:
            raise RuntimeError("Existing application folder is incomplete: " + ", ".join(missing)
                               + ". Do not delete it if it contains data; rename/back it up first.")
        print("Existing application found. No clone and no history reset performed.")
        return app
    if not shutil.which("git"):
        raise RuntimeError("Git was not found. Install Git from https://git-scm.com/downloads, reopen the terminal, and retry.")
    print("Fetching the previously developed Module 7.2 application (first run only).")
    try:
        runner(["git", "clone", "--no-checkout", SOURCE_URL, str(app)], check=True,
               text=True, capture_output=True, timeout=180)
        # Checking out the recorded commit avoids an unannounced upstream change.
        runner(["git", "-C", str(app), "checkout", "--detach", SOURCE_REVISION],
               check=True, text=True, capture_output=True, timeout=45)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError("Could not download or pin the source application. Check internet, Git installation, "
                           "and whether the GitHub repository is available. The application was not started. "
                           f"Details: {exc}") from exc
    missing = verify_app(app)
    if missing:
        raise RuntimeError("Downloaded app lacks required files: " + ", ".join(missing))
    manifest = {"source": SOURCE_URL, "revision": SOURCE_REVISION,
                "method": "First-run checkout; preserved on later starts"}
    (root / "application-version.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("App prepared at", app)
    return app


def main():
    try:
        prepare()
    except RuntimeError as exc:
        print("SETUP ERROR:", exc, file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
