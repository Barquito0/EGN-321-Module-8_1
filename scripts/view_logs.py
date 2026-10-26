"""Explain recent structured log entries without needing Unix tail commands."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def last_events(path:Path,limit:int=12)->list[dict]:
    path=Path(path)
    if not path.exists():
        return []
    lines=path.read_text(encoding="utf-8",errors="replace").splitlines()
    out=[]
    for line in lines[-max(limit,1):]:
        try:out.append(json.loads(line))
        except json.JSONDecodeError:out.append({"event":"UNPARSEABLE_LINE","message":line[:200]})
    return out


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--last",type=int,default=12)
    args=parser.parse_args()
    logfile=ROOT/"application"/"logs"/"monitor.jsonl"
    if not logfile.exists():
        print("No runtime log yet. Start the application first. Expected:",logfile)
        raise SystemExit(1)
    for event in last_events(logfile,args.last):
        print(f"{event.get('timestamp_utc','?')} | {event.get('event','?'):20} | {event.get('message','')}")

if __name__=="__main__":
    main()
