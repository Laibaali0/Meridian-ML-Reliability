# Publish the existing Git history to GitHub

Create a **new empty public repository** named `meridian-ml-reliability` in the GitHub account that should own it. Do not initialize it with a README or starter commit.

To preserve the complete sequence of commits in the supplied Git bundle:

```bash
git clone meridian-ml-reliability-history.bundle meridian-ml-reliability
cd meridian-ml-reliability
git remote set-url origin https://github.com/Laibaali0/meridian-ml-reliability.git
git push -u origin main
```

The bundle is a Git-native archive and can be cloned directly; GitHub's browser `Upload files` will **not** preserve earlier local commit history. Extracting the source ZIP and uploading it as files creates a new upload history instead.

## Before sharing the repository

- Run `python -m pip install -e '.[dev]'` and `python -m pytest -q`.
- Inspect the modules and examples, and understand their limitations.
- Do not imply synthetic evaluations were conducted on real customer data or company infrastructure.
- Commit history was created during an AI-assisted development session. It is not an historical record of months of personal work.

If the target GitHub repository is not yet created, these commands cannot push to it. The GitHub Projects tab is separate from repository code.
