# GitHub Publishing — Local Fallback

**Target:** https://github.com/Barquito0/EGN-321-Module-8_1

The final handoff project is ready to commit, but a GitHub write action was not accessible inside the producing ChatGPT session. The link above is the **intended destination**, not proof that files have been uploaded.

If the GitHub connector becomes available, the files can be committed directly. Otherwise, from an extracted copy of this package with Git installed and your own GitHub credentials already configured:

```bash
python scripts/publish_repository.py
```

For Windows, `py scripts\publish_repository.py` also works.

The helper clones the named repository, **refuses to overwrite a nonempty repository**, prepares three meaningful commits, and pushes `main` without `--force`. It does not send or store passwords. When the repository is nonempty, merge the prepared package manually rather than force pushing.

After publishing, verify GitHub contains the README, `data/`, `scripts/`, `docs/`, `tests/`, `.github/workflows/tests.yml`, and a successful Actions test run.

**Important:** Publishing does not complete the partner-observation portion of Assignment 8.1. The observation table, genuine handoff evidence, two *post*-handoff improvements, and reflection must be completed after the classmate's silent test.
