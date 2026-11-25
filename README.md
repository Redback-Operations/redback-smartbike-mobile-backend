# redback-smartbike-mobile-backend
new separated backend repo set up in 2025T3 as the frontend moved from flutter to react over 2025, and the main mobile repo contains both past frontend and backend. this will be used to establish the new connected backend

## Setup

Requires [mise](https://mise.jdx.dev/getting-started.html), which installs the pinned
Python version and creates `.venv` from `mise.toml`.

```bash
mise trust && mise install   # Python + .venv
mise run install             # pip install -r requirements-dev.txt
cp backend/.env.example backend/.env   # then set SECRET_KEY (generate command is in the file)
cd backend
python manage.py migrate
python manage.py runserver
```

Without mise: create a Python 3.15 venv, activate it, then `pip install -r requirements-dev.txt`
and run the commands in `mise.toml` by hand.

## Tasks

| Command          | What it does                                               |
| ---------------- | ---------------------------------------------------------- |
| `mise run test`  | Django checks, missing-migration check, test suite         |
| `mise run lint`  | Ruff lint + format check (what CI enforces)                |
| `mise run fmt`   | Auto-fix lint issues and format code                       |
| `mise run audit` | Scan dependencies for known vulnerabilities (pip-audit)    |

CI (`.github/workflows/tests.yml`) runs `lint`, `audit` and `test` on every pull request.

## Code style

We follow the [Django coding style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)
(PEP 8, Black formatting, isort import order), enforced by [Ruff](https://docs.astral.sh/ruff/)
with the rules in `pyproject.toml`. Ruff also runs bugbear and Bandit security checks.
Pull requests that fail `mise run lint` can't pass CI.

- Editor: install the Ruff extension (VS Code `charliermarsh.ruff`, PyCharm "Ruff" plugin) and
  enable format on save. It uses the Ruff version in `.venv`.
- Run `mise run fmt` before committing, or install a pre-commit hook that runs the lint check:
  `mise generate git-pre-commit --write --task=lint`
- Run `git config blame.ignoreRevsFile .git-blame-ignore-revs` once so `git blame` skips
  mass-reformat commits.
