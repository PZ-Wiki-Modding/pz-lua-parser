.ONESHELL:
.PHONY: help run

SHELL := /bin/bash

help:
	@echo "PZ Lua Parser"
	@echo "Available targets:"
	@echo "  run:   Run the parser"

run:
	@echo "Fetch distributions"
	./.venv/bin/python ./scripts/distributions.py

	@echo "Fetch items translations"
	./.venv/bin/python ./scripts/items_translations.py

	@echo "Fetch procedural distributions"
	./.venv/bin/python ./scripts/procedural_distributions.py