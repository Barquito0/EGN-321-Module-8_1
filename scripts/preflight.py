"""Repeatable, non-destructive operator diagnostic for the Module 7 monitor."""
from __future__ import annotations
import csv
import importlib.util
import os
import shutil
import socket
import sys
from pathlib import Path
try:
    from scripts.prepare_application import verify_app, ROOT
except ModuleNotFoundError:
    from prepare_application import verify_app, ROOT

REQUIRED_COLS = {"sample_number", "timestamp", "temperature_c", "temperature_status"}


def source_csv_check(path: Path):
    try:
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            missing = REQUIRED_COLS.difference(reader.fieldnames or [])
            if missing:
                return False, "CSV missing required columns: " + ", ".join(sorted(missing))
            first = next(reader, None)
            if not first:
                return False, "CSV has a header but no readings"
            return True, f"CSV recognized (first sample #{first['sample_number']}, unit C)"
    except (OSError, UnicodeError, csv.Error) as exc:
        return False, f"Unable to read input CSV: {type(exc).__name__}: {exc}"


def port_free(port=5000, host="127.0.0.1"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, int(port))) != 0


def evaluate(root=ROOT, *, check_port=True):
    root=Path(root)
    result=[]
    def note(ok, test, resolution):
        result.append((bool(ok), test, resolution))
    note(sys.version_info >= (3, 11), f"Python {sys.version_info.major}.{sys.version_info.minor}", "Install Python 3.11 or newer")
    note(importlib.util.find_spec("flask") is not None, "Flask importable", "Run: python -m pip install -r requirements.txt")
    note(shutil.which("git") is not None, "Git installed", "Install Git and reopen terminal")
    app=root/"application"
    note(app.is_dir() and not verify_app(app), "Previous-course application present", "Run: python scripts/prepare_application.py")
    csv_path = app / "data" / "module6_sample_sensor_history.csv" if app.exists() else root/"data"/"module6_sample_sensor_history.csv"
    ok,detail=source_csv_check(csv_path)
    note(ok, "Source CSV: " + detail, "Restore the original CSV; do not invent missing readings")
    note(not check_port or port_free(os.environ.get("PORT","5000")), "Dashboard port available", "Stop the other service using the port or set PORT to another free port")
    state=app/"state"
    if app.exists():
        try:
            state.mkdir(exist_ok=True)
            file=state/".preflight_write_test"
            file.write_text("ok",encoding="utf-8")
            file.unlink()
            writable=True
        except OSError:
            writable=False
        note(writable,"State folder writable","Fix folder permissions; do not delete the SQLite DB")
    return result


def main():
    problems=0
    print("EGN 321 MODULE 8.1 — OPERATOR PREFLIGHT\n")
    for ok,label,remedy in evaluate():
        print(("PASS" if ok else "FAIL") + " | " + label)
        if not ok:
            problems+=1
            print("     Fix: " + remedy)
    print("\n"+("READY: start the app with scripts/start_monitor.py" if not problems
                else f"STOP: {problems} issue(s). Resolve the FAIL items before starting."))
    raise SystemExit(1 if problems else 0)


if __name__ == "__main__":
    main()
