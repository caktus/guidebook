---
name: upgrade-python-and-packages
description: 'Upgrades a uv project to the latest Python version and upgrades all packages to their latest compatible versions. Use when upgrading Python, removing pinned versions, refreshing uv.lock, or updating CI to a newer Python.'
argument-hint: 'Optional: target Python version (default: latest stable)'
---

# Upgrade Python and Packages

Upgrades the Python version pin and all package dependencies to their latest versions in a uv-managed project.

## Purpose

Given a uv project with a `.python-version` pin and locked `pyproject.toml` dependencies, upgrade to the latest Python and latest package versions, update `uv.lock`, and keep CI in sync.

## Directives & Constraints

- **Do not change application code** — only dependency management and CI files.
- **Detect, don't assume** — check `.python-version`, `pyproject.toml`, and workflow files before acting.
- **Verify before committing** — only commit after `uv sync` succeeds and the project runs.
- **Match Python version everywhere** — `.python-version`, `requires-python`, and CI workflows must all agree.

## Workflow

Copy this checklist and track your progress as you work:

```text
Task Progress:
- [ ] Step 1: Check current state
- [ ] Step 2: Choose target Python version
- [ ] Step 3: Update Python pin
- [ ] Step 4: Remove version pins from pyproject.toml
- [ ] Step 5: Upgrade all packages
- [ ] Step 6: Verify
- [ ] Step 7: Update GitHub Actions workflows
- [ ] Step 8: Commit
```

### Step 1: Check current state

```bash
cat .python-version
cat pyproject.toml
uv python list --only-installed
```

Note the current Python version and any existing version specifiers on dependencies.

### Step 2: Choose target Python version

List available stable Python versions:

```bash
uv python list
```

Default to the latest stable release unless the user specifies a version. Avoid pre-release versions unless explicitly requested.

### Step 3: Update Python pin

```bash
uv python pin <version>
```

Then update `requires-python` in `pyproject.toml` to match:

```toml
requires-python = ">=<version>"
```

### Step 4: Remove version pins from pyproject.toml

Edit `pyproject.toml` to remove all version specifiers from the `dependencies` list. Each dependency should be listed by name only:

```toml
# Before
dependencies = [
    "mypackage>=9.1.4",
]

# After
dependencies = [
    "mypackage",
]
```

Do the same for any `[dependency-groups]` (dev/test deps).

### Step 5: Upgrade all packages

Resolve and lock the latest compatible versions:

```bash
uv lock --upgrade
uv sync
```

If `uv lock --upgrade` fails due to conflicts, read the error carefully. Try upgrading conflicting packages individually with `uv add <package>` to see resolution details.

### Step 6: Verify

```bash
uv run python --version
uv tree --depth 1
```

Confirm:
- Python version matches the pin from Step 3.
- All top-level dependencies are present.
- No resolution errors.

If the project has a runnable entry point (e.g., `mkdocs serve`, a test suite, a CLI command), run it to confirm nothing is broken:

```bash
uv run <entry-point> --version   # or equivalent smoke test
```

Check for deprecation warnings in the output. If any deprecated APIs are flagged, note them for the user — they may require config file updates (not dependency changes).

### Step 7: Update GitHub Actions workflows

Check whether `.github/workflows/` has any workflow files referencing a Python version:

```bash
grep -r "python-version" .github/workflows/
```

For each match, update the `python-version` value to match the pin from Step 3:

```yaml
      - name: Install uv
        uses: astral-sh/setup-uv@v7
        with:
          python-version: "<version>"   # ← update this
          enable-cache: true
          cache-dependency-glob: "uv.lock"
```

### Step 8: Commit

```bash
git add pyproject.toml uv.lock .python-version .github/workflows/
git commit -m "chore: upgrade Python to <version> and update dependencies"
```
