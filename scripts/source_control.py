"""Explicitly pause/resume replay input for troubleshooting, without deleting data."""
from __future__ import annotations
import argparse
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def change_source(app:Path,action:str)->str:
    app=Path(app)
    flag=app/"state"/"pause.flag"
    if not (app/"src"/"monitor.py").exists():
        raise RuntimeError("Application is not prepared. Run scripts/prepare_application.py")
    if action=="pause":
        flag.parent.mkdir(exist_ok=True)
        if flag.exists():
            return "Replay was already paused; no change was made."
        flag.touch(exist_ok=False)
        return f"Replay PAUSED with {flag}. Watch dashboard enter DEGRADED after 8 s and FAILED after 18 s."
    if action=="resume":
        if not flag.exists():
            return "Replay was not paused; no change was made."
        flag.unlink()
        return "Replay RESUMED. Keep dashboard open until a NEW accepted reading returns HEALTHY."
    if action=="status":
        return "Replay flag: PAUSED" if flag.exists() else "Replay flag: NOT PAUSED"
    raise ValueError("Action must be pause, resume, or status")


def main():
    parser=argparse.ArgumentParser(description="Classroom replay interruption control (no DB deletion)")
    parser.add_argument("action",choices=("pause","resume","status"))
    args=parser.parse_args()
    try:
        print(change_source(ROOT/"application",args.action))
    except (RuntimeError,OSError) as exc:
        parser.exit(2,f"ERROR: {exc}\n")

if __name__=="__main__":
    main()
