.PHONY: help install install.dev generate-test-data lint test clean bump.patch bump.minor bump.major

.DEFAULT_GOAL := help

PACKAGE_NAME := whatstk
TEST_DIR := tests
REPORTS_DIR := reports

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install package in editable mode
	uv pip install -e .

install.dev: ## Install package with dev dependencies
	uv pip install -e .[dev]

generate-test-data: ## Generate test chat files
	mkdir -p $(TEST_DIR)/chats/hformats $(TEST_DIR)/chats/merge
	whatstk-generate-chat --size 500 -z --output-path $(TEST_DIR)/chats/hformats/
	whatstk-generate-chat --size 300 --last-timestamp 2019-09-01 \
		--hformats '%Y-%m-%d, %H:%M - %name:' \
		--output-path $(TEST_DIR)/chats/merge/ --filenames file1.txt
	whatstk-generate-chat --size 300 --last-timestamp 2020-01-01 \
		--hformats '%Y-%m-%d, %H:%M - %name:' \
		--output-path $(TEST_DIR)/chats/merge/ --filenames file2.txt

lint: ## Run flake8 linting
	flake8 \
		--max-complexity=10 \
		--docstring-convention=google \
		--format=html --htmldir=$(REPORTS_DIR)/flake-report \
		--max-line-length=120 \
		--ignore=ANN101,ANN102,ANN401 \
		$(PACKAGE_NAME)

test: ## Run tests with coverage
	mkdir -p $(REPORTS_DIR)
	uv run pytest \
		--html=$(REPORTS_DIR)/testreport.html \
		--cov-report html:$(REPORTS_DIR)/htmlcov \
		--cov-report term \
		--cov-report xml:$(REPORTS_DIR)/cov.xml \
		--cov=$(PACKAGE_NAME) $(TEST_DIR)

clean: ## Remove build and test artifacts
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf $(REPORTS_DIR) .pytest_cache .coverage htmlcov build dist *.egg-info .uv

bump.patch: ## Bump patch version (0.0.X)
	bump-my-version bump patch

bump.minor: ## Bump minor version (0.X.0)
	bump-my-version bump minor

bump.major: ## Bump major version (X.0.0)
	bump-my-version bump major


.sanity-check:
	@echo '==> Checking your Python setup'

	@if python -c "import sys; exit(0 if sys.platform.startswith('win32') else 1)"; then \
		echo 'ERROR: you are using a non-WSL Python interpreter, please consult the'; \
		echo '       docs on how to swich to WSL Python on windows'; \
		echo '       https://github.com/owid/etl/'; \
		exit 1; \
	fi
	touch .sanity-check

install-uv:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo '==> UV not found. Installing...'; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi

.venv: install-uv .sanity-check
	@echo '==> Installing packages'
	@if [ -n "$(PYTHON_VERSION)" ]; then \
		echo '==> Using Python version $(PYTHON_VERSION)'; \
		[ -f $$HOME/.cargo/env ] && . $$HOME/.cargo/env || true && UV_PYTHON=$(PYTHON_VERSION) uv sync --all-extras; \
	else \
		[ -f $$HOME/.cargo/env ] && . $$HOME/.cargo/env || true && uv sync --all-extras; \
	fi
