#!/bin/sh
# setup script for ubuntu 22.04
# installs tox and multiple python interpreters locally to check multiple python versions locally.
# we use pipx to isolate python-based dev tools (e.g. poetry, tox) from the rest.
apt-get install -y pipx
pipx install tox

# ubuntu22.04 (tuxedo): needed for: python 3.9-distutils and python3.12
add-apt-repository ppa:deadsnakes/ppa
apt-get update

apt-get install -y python3.8-distutil python3.9-distutil python3.10 python3.11 python3.12
