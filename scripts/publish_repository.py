"""Publish the prepared handoff to an *empty* GitHub repository with three commits.

Requires installed git and an existing Git credential helper / SSH session.
No credentials are stored here. Never force pushes or overwrites a nonempty repo.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = "https://github.com/Barquito0/EGN-321-Module-8_1.git"

LAYERS = [
    ("docs: publish operator README and AI transparency",
     ["README.md", "AI_LOG.md", ".gitignore", "requirements.txt"]),
    ("feat: add sample data and safer operator diagnostics",
     ["data", "scripts"]),
    ("test: add handoff checklists, observation templates and CI",
     ["docs", "tests", ".github"]),
]


def git(*args, cwd=None, capture=False):
    result = subprocess.run(["git", *args], cwd=cwd, check=True,
                            text=True, capture_output=capture)
    return result.stdout.strip() if capture else None


def main():
    if not shutil.which("git"):
        raise SystemExit("Git not found; install Git before publishing.")
    with tempfile.TemporaryDirectory(prefix="egn321-handoff-publish-") as tmp:
        destination = Path(tmp) / "repository"
        print("Cloning target repository (existing Git authentication required) ...", flush=True)
        git("clone", URL, str(destination))
        existing = git("ls-files", cwd=destination, capture=True)
        if existing:
            raise SystemExit("STOP: target repository is not empty. Refusing to overwrite files or force-push."
                             " Review and merge changes manually instead.")
        for message, items in LAYERS:
            for item in items:
                original = ROOT / item
                target = destination / item
                if not original.exists():
                    raise SystemExit(f"Missing package item: {item}")
                if original.is_dir():
                    shutil.copytree(original, target, ignore=shutil.ignore_patterns(
                        "__pycache__", ".pytest_cache", "*.pyc", ".DS_Store"))
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(original, target)
                git("add", item, cwd=destination)
            git("commit", "-m", message, cwd=destination)
            print("Prepared commit:", message, flush=True)
        git("branch", "-M", "main", cwd=destination)
        git("push", "-u", "origin", "main", cwd=destination)
        print("Published: https://github.com/Barquito0/EGN-321-Module-8_1")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        raise SystemExit("Publishing stopped after a Git error. Your local handoff files remain unchanged. "
                         "Check the displayed Git error and your GitHub authentication.") from exc
