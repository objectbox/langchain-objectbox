langchain-objectbox Developer Notes 
===================================
This document is intended for developers of the `langchain-objectbox` package,
e.g. to contribute to this project itself.

To use `langchain-objectbox` in your project, see the [README.md](README.md) file.

Setup
-----
### Recommendation: PipX

Python Developer Tools such as `poetry` and `tox` have their own dependencies and a standard command-line entry point.

[PipX](https://pipx.pypa.io/stable/) is very helpful for setting up such packages in their own environment and making

them available in your shell environment.

```bash
# Debian-based Setup of poetry (should be external to venv)
sudo apt-get install -y pipx
```

Ensure you have `$HOME/.local/bin` in your `$PATH`.

### Requirement: Poetry

We choose poetry as build tool as it is the tool of choice for building langchain.

Should be installed isolated from rest of system and project's venv (see also https://python-poetry.org/docs/#installation)

We suggest to install it via pipx (but ofcourse, you can always use local virtual environments or conda at your will):

```bash
pipx install poetry
```

### Tox

Tox is helpful for testing locally against multiple python versions.

```bash
pipx install tox
```

### Initial Setup

Checking out this repository.

#### Recommendation: Setup a virtual environment 

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies and this package, then run the tests:

```bash
cd libs/objectbox
poetry install
poetry run pytest
```

### Start Developer Sessions

```bash
source .venv/bin/activate
```

### Test

```bash
pytest
```

### Build package

```bash
poetry build
```

### Update ObjectBox

```bash
cd libs/objectbox
poetry show objectbox
poetry update objectbox
```

Misc: How this package was created
----------------------------------

```
mkdir -p libs/objectbox  # more-or-less blueprinted from other `langchain-<ext>` python projects
cd libs/objectbox
poetry init # answered some questions, added deps: langchain-core, objectbox
poetry add -G test pytest
python3 -m venv .venv
source .venv/bin/activate
poetry install
poetry add -G test langchain
```

- From `objectbox-langchain/libs/community`, copied
  - `langchain_community/vectorstores/objectbox.py` to `langchain_objectbox/vectorstores.py`
  - `tests/integration_tests/vectorstores/test_objectbox.py` to `tests/integration_tests/test_objectbox.py`
    - Deactivated integration tests that use HuggingFace... TODO: Can we have simpler Embeddings (it wanted to download nvidia packages, can ollama be an option here?)