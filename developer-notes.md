langchain-objectbox Developer Notes 
===================================
This document is intended for developers of the `langchain-objectbox` package,
e.g. to contribute to this project itself.

To use `langchain-objectbox` in your project, see the [README.md](README.md) file.

Setup
-----

### PipX

Python Developer Tools such as `poetry` and `tox` have their own dependencies and a standard command-line entry point.

[PipX](https://pipx.pypa.io/stable/) is very helpful for setting up such packages in their own environment and making
them available in your shell environment.

```bash
# Debian-based setup 
sudo apt-get install -y pipx
```

Ensure you have `$HOME/.local/bin` in your `$PATH`.

### Poetry

We choose poetry as build tool since it is the tool of choice for building langchain.

`poetry` should be installed isolated from rest of system and project's venv (see also https://python-poetry.org/docs/#installation)

We suggest to install it via `pipx` (but ofcourse, you can always use local virtual environments or conda at your will):

```bash
pipx install poetry
```

### Optional: Tox

Tox is helpful for testing locally against multiple Python versions.

```bash
pipx install tox
```

Helper setup script for Debian-Systems: Installs `pipx`, `tox` and multiple Python versions (3.8-3.12) - (May request password authorization as it uses `sudo`):

```bash
./scripts/setup-tox.sh
```

### Initial Setup

Checking out this repository.

#### Recommendation: Setup a virtual environment 

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Setup dependencies

```bash
cd libs/objectbox
poetry install
```

Development
-----------

### Opt-in: activate virtual environment

With the virtual environment in place (see above), you can activate it like that:

```bash
source .venv/bin/activate
```

### Test

```bash
cd libs/objectbox
poetry run pytest
```

### Build package

```bash
cd libs/objectbox
poetry build
```

### Update ObjectBox

```bash
cd libs/objectbox
poetry show objectbox
poetry update objectbox
```

### Tox: Run install and run tests for Python 3.8 - 3.12

```bash
cd libs/objectbox
tox
```

Misc: How this package was created
----------------------------------

```
python3 -m venv .venv
source .venv/bin/activate
mkdir -p libs/objectbox  # more-or-less blueprinted from other `langchain-<ext>` python projects
cd libs/objectbox
poetry init # answered some questions, added deps: langchain-core, objectbox
poetry add -G test pytest
poetry install
poetry add -G test langchain
```
