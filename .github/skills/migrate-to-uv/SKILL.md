---
name: migrate-to-uv
description: 'Migrates a Python project from pip/requirements.txt to uv. Use when converting a project to uv, replacing requirements.txt with pyproject.toml, or setting up uv.lock for dependency locking.'
argument-hint: 'Optional: python version (default: 3.9)'
---

# Migrate Project to uv

Converts a pip-based project to uv with a locked `pyproject.toml` and `uv.lock`.

## Purpose

Migrate an existing pip-based Python project to `uv`, replacing `requirements.txt` files and manual `venv` management with a unified `pyproject.toml`, reproducible `uv.lock`, and optional CI updates.

## Directives & Constraints

- **Do not change application code** — only dependency management and CI files.
- **Detect, don't assume** — check for requirements files and workflow files before acting on them.
- **Verify before cleanup** — only delete legacy files after `uv sync` succeeds.
- **Match pinned Python version** — use the same version everywhere (`.python-version`, CI workflows).

## Workflow

Copy this checklist and track your progress as you work:

```text
Task Progress:
- [ ] Step 1: Initialize uv workspace
- [ ] Step 2: Pin Python version
- [ ] Step 3: Import dependencies
- [ ] Step 4: Sync environment
- [ ] Step 5: Verify
- [ ] Step 6: Clean up legacy files
- [ ] Step 7: Update GitHub Actions workflows
- [ ] Step 8: Update .gitignore and commit
```

### Step 1: Initialize uv workspace

Run in the project root. Safe to run over existing files.

```bash
uv init --bare
```

### Step 2: Pin Python version

```bash
uv python pin 3.9
```

Replace `3.9` with the target version if different. This writes `.python-version`.

### Step 3: Import dependencies

Check for any `requirements*.txt` or `*-requirements.txt` files. Files with `dev` or `test` in the name are imported as dev dependencies.

```bash
[ -f requirements.txt ] && uv add -r requirements.txt

[ -f requirements-dev.txt ] && uv add -r requirements-dev.txt --dev
[ -f dev-requirements.txt ] && uv add -r dev-requirements.txt --dev
```

### Step 4: Sync environment

Resolves all dependencies, writes `uv.lock`, and creates `.venv`.

```bash
uv sync
```

### Step 5: Verify

```bash
uv run python --version
uv tree
```

Confirm the Python version matches the pin and the dependency tree looks correct. Stop and fix any errors before continuing.

### Step 6: Clean up legacy files

Only run after Step 5 passes:

```bash
rm -f requirements.txt requirements-dev.txt dev-requirements.txt
```

### Step 7: Update GitHub Actions workflows

Check whether `.github/workflows/` contains any workflow files. If none exist, skip this step.

For each workflow file found, replace the `actions/setup-python` + pip install pattern with the `astral-sh/setup-uv` equivalent:

1. Remove the `actions/setup-python` step and any `pip install` run steps
2. Replace with:

```yaml
      - name: Install uv
        uses: astral-sh/setup-uv@v7
        with:
          python-version: "3.9"
          enable-cache: true
          cache-dependency-glob: "uv.lock"

      - name: Install Python dependencies
        run: uv sync --locked
```

Set `python-version` to match the version pinned in Step 2.

### Step 8: Update .gitignore and commit

Ensure `.venv/` is in `.gitignore`, then commit all migration artifacts:

```bash
grep -qxF '.venv/' .gitignore || echo '.venv/' >> .gitignore
git add pyproject.toml uv.lock .python-version .gitignore
git commit -m "chore: migrate to uv"
```
