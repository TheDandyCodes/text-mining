.ONESHELL:
.PHONY: install hooks hooks-update

SHELL := /usr/bin/env bash

# Install uv, pre-commit hooks and dependencies
# Note that `uv run` has an implicit `uv sync`, since it will (if necessary):
# - Download and install Python
# - Create a virtual environment
# - Update `uv.lock`
# - Sync the virtual env, installing and removing dependencies as required
install:
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv run pre-commit install

# Ejecuta todos los hooks en todos los archivos (opcional)
hooks:
	uv run pre-commit run --all-files

# Actualiza versiones de hooks (opcional)
hooks-update:
	uv run pre-commit autoupdate