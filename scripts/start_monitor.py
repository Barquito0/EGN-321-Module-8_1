"""One-command operator entrypoint for the preserved 7.2 process supervisor."""
from __future__ import annotations
import os
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main():
    app=ROOT/"application"
    if not (app/"supervisor.py").is_file():
        print("APP MISSING: Run `python scripts/prepare_application.py` first.",file=sys.stderr)
        raise SystemExit(2)
    # Do not overwrite user-set configuration. Default to a safe loopback service.
    env=os.environ.copy()
    for key,value in {"HOST":"127.0.0.1","PORT":"5000","CLASSROOM_DEMO":"0",
                      "REPLAY_SECONDS":"2","STALE_DEGRADED_SECONDS":"8",
                      "STALE_FAILED_SECONDS":"18","PYTHONUNBUFFERED":"1"}.items():
        env.setdefault(key,value)
    print(f"Starting supervised monitor. Open http://127.0.0.1:{env['PORT']}",flush=True)
    print("Press Ctrl+C once to stop. Do not delete application/state/monitor.db.",flush=True)
    try:
        subprocess.run([sys.executable,"-u","supervisor.py"],cwd=app,env=env,check=False)
    except KeyboardInterrupt:
        print("Shutdown requested.")


if __name__ == "__main__":
    main()
