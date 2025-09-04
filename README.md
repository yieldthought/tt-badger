<p align="center">
  <img src="logo.png" alt="tt-badger logo" width="180" />
</p>

Generate GitHub Actions badge Markdown for `tenstorrent/tt-metal` workflows and optionally run the tests.

## Install

- pip: `pip install tt-badger`
- pipx (recommended for CLIs): `pipx install tt-badger`

This installs the `tt-badger` command.

## Usage

- Interactive mode:
  - `tt-badger --branch main`
  - Press 0–9 to toggle workflows; press Enter to print selected badges
  - Press Esc at the menu to cancel and exit

- Non-interactive pre-selection (skips the menu):
  - `tt-badger -b main --select 1290`  (toggles 1, 2, 9, and last)
  - Press Esc at the branch prompt to cancel

- Auto-dispatch selected workflows (requires GitHub CLI):
  - `tt-badger -b my-feature --select 19 --run`
  - Uses `gh workflow run <workflow> -R tenstorrent/tt-metal --ref <branch>` for each selected workflow

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
- `--run`: After printing, dispatch selected workflows via the GitHub CLI (`gh`).

Requires `gh` installed and authenticated (`gh auth login`) to run workflows.

### Install GitHub CLI (gh)

macOS:

```
brew install gh
```

Linux (Debian/Ubuntu):

```
type -p curl >/dev/null || sudo apt update && sudo apt install -y curl
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
  sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | \
  sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install -y gh
```

Linux (Fedora/RHEL/CentOS):

```
sudo dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo
sudo dnf install -y gh
```

Then authenticate: `gh auth login`

## Development

- Editable install: `pip install -e .`
- Run from source:
  - `python -m tt_badger.cli -b main`
  - or `./badger -b main`

## Release (CI to PyPI)

- This repo publishes to PyPI via GitHub Actions using PyPI Trusted Publishing (OIDC) only — no secrets required.
- On PyPI, add a Trusted Publisher for this repo with workflow path `.github/workflows/publish.yml`.
- To release:
  1. Bump `__version__` in `src/tt_badger/__init__.py` and `pyproject.toml`.
  2. Create a Git tag like `v0.1.0` and draft a GitHub Release.
  3. Publish the Release to trigger the PyPI workflow.

License: Apache 2.0 (see `LICENSE`).
