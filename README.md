# tt-badger

Generate GitHub Actions badge Markdown for `tenstorrent/tt-metal` workflows.

- Numbering: 1–9, with 0 mapped to the last item (10th)
- Instant toggling: press digits to toggle; Enter to finish
- Persists selection in `~/.tt-badges.json` unless `--select` is provided
- Always includes `?branch=<branch>` in `badge.svg` URLs

## Install

- pip: `pip install tt-badger`
- pipx (recommended for CLIs): `pipx install tt-badger`

This installs the `tt-badger` command.

## Usage

- Interactive mode:
  - `tt-badger --branch main`
  - Press 0–9 to toggle workflows; press Enter to print selected badges

- Non-interactive pre-selection (skips the menu):
  - `tt-badger -b main --select 1290`  (toggles 1, 2, 9, and last)

If no `--select` is given, the previously saved selection (from
`~/.tt-badges.json`) is used as a starting point.

Example output (Markdown):

```
[![All post-commit tests](https://github.com/tenstorrent/tt-metal/actions/workflows/all-post-commit-workflows.yaml/badge.svg?branch=main)](https://github.com/tenstorrent/tt-metal/actions/workflows/all-post-commit-workflows.yaml)
[![Blackhole post-commit tests](https://github.com/tenstorrent/tt-metal/actions/workflows/blackhole-post-commit.yaml/badge.svg?branch=main)](https://github.com/tenstorrent/tt-metal/actions/workflows/blackhole-post-commit.yaml)
```

## CLI Options

- `-b, --branch <name>`: Branch name (e.g., `main` or `feature/foo`). Required.
- `-s, --select <digits>`: Digits `1–9` (and `0` for the last) to pre-toggle and skip interaction.

## Development

- Editable install: `pip install -e .`
- Run from source:
  - `python -m tt_badger.cli -b main`
  - or `./badger -b main`

## Release (CI to PyPI)

- This repo includes GitHub Actions to publish:
  - `Publish to TestPyPI`: on pre-releases (or manual dispatch)
  - `Publish to PyPI`: on published GitHub Releases (or manual dispatch)

- Recommended: enable PyPI Trusted Publishing (OIDC) for the `tt-badger` project.
  - Configure the project on PyPI/TestPyPI to trust this GitHub repo.
  - The workflows will authenticate via OIDC (no token needed).

- Alternative: use API tokens (if not using OIDC):
  - Add repo secrets `PYPI_API_TOKEN` and/or `TEST_PYPI_API_TOKEN`.

- To release:
  1. Bump `__version__` in `src/tt_badger/__init__.py` and `pyproject.toml`.
  2. Create a Git tag like `v0.1.0` and draft a GitHub Release.
  3. Publish the Release to trigger the PyPI workflow.

License: Apache 2.0 (see `LICENSE`).
