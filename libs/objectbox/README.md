# langchain-objectbox

## About

This package contains the [ObjectBox](https://objectbox.io) integrations for [LangChain](https://www.langchain.com).

## Development Notes

### Setup

#### Poetry
Should be installed isolated from rest of system and project's venv (see also https://python-poetry.org/docs/#installation)

```
# Debian-based Setup of poetry (should be external to venv)
apt-get install -y pipx
pipx install poetry
```

Ensure your `$HOME/.local/bin` is in `$PATH`.

#### Tox

```
pipx install tox
```

#### Initial Package Setup

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

### Initial Setup

```
cd libs/objectbox
poetry install
poetry run pytest
```

### Start Developer Sessions

```
source .venv/bin/activate
```

### Test

```
pytest
```

### Build package

```
poetry build
```


