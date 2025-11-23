.PHONY: help install install.dev generate-test-data check.format check.lint check.type test unittest clean bump.patch bump.minor bump.major docs docs.serve

.DEFAULT_GOAL := help

PACKAGE_NAME := whatstk
TEST_DIR := tests
REPORTS_DIR := reports
TEST_CHATS_DIR := $(TEST_DIR)/chats

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

##################################################
## INSTALLATION / PREP
install: ## Install package in editable mode
	uv pip install -e .

install.dev: ## Install package with dev dependencies
	uv pip install -e .[dev]

.sanity-check:
	@echo '==> Checking your Python setup'
	@# Skip sanity check in CI environments (GitHub Actions, etc.)
	@if [ -z "$$CI" ]; then \
		if python -c "import sys; exit(0 if sys.platform.startswith('win32') else 1)"; then \
			echo 'ERROR: you are using a non-WSL Python interpreter, please consult the'; \
			echo '       docs on how to switch to WSL Python on windows'; \
			echo '       https://github.com/lucasrodes/whatstk/'; \
			exit 1; \
		fi; \
	fi
	@touch .sanity-check

install-uv:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo '==> UV not found. Installing...'; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi

.venv: install-uv .sanity-check
	@echo '==> Installing packages'
	@if [ -n "$(PYTHON_VERSION)" ]; then \
		echo '==> Using Python version $(PYTHON_VERSION)'; \
		[ -f $$HOME/.cargo/env ] && . $$HOME/.cargo/env || true && UV_PYTHON=$(PYTHON_VERSION) uv sync --all-extras --prerelease=if-necessary; \
	else \
		[ -f $$HOME/.cargo/env ] && . $$HOME/.cargo/env || true && uv sync --all-extras --prerelease=if-necessary; \
	fi

##################################################
# TESTING
test: check.format check.lint check.type unittest  ## Run formatting, linting, type-checking, and unit tests

check.format: ## Format code with ruff
	uv run ruff format --check $(PACKAGE_NAME) $(TEST_DIR)

format: ## Format code with ruff
	uv run ruff format $(PACKAGE_NAME) $(TEST_DIR)

check.lint: ## Run ruff linting
	mkdir -p $(REPORTS_DIR)
	uv run ruff check $(PACKAGE_NAME) $(TEST_DIR)

check.type: ## Run pyright type checking
	uv run pyright $(PACKAGE_NAME)

unittest: $(TEST_CHATS_DIR) ## Run tests with coverage (use N=4 or N=auto for parallel execution)
	mkdir -p $(REPORTS_DIR)
	uv run pytest \
		--html=$(REPORTS_DIR)/testreport.html \
		--cov-report html:$(REPORTS_DIR)/htmlcov \
		--cov-report term \
		--cov-report xml:$(REPORTS_DIR)/cov.xml \
		--cov=$(PACKAGE_NAME) $(TEST_DIR)


unittest-parallel: $(TEST_CHATS_DIR) ## Run tests with coverage (use N=4 or N=auto for parallel execution)
	mkdir -p $(REPORTS_DIR)
	uv run pytest -n auto \
		--html=$(REPORTS_DIR)/testreport.html \
		--cov-report html:$(REPORTS_DIR)/htmlcov \
		--cov-report term \
		--cov-report xml:$(REPORTS_DIR)/cov.xml \
		--cov=$(PACKAGE_NAME) $(TEST_DIR)

################################################
# MAINTENANCE
clean: ## Remove build and test artifacts
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf $(REPORTS_DIR) .pytest_cache .coverage htmlcov build dist *.egg-info .uv

# Build analytics DuckDB snapshot
$(TEST_CHATS_DIR):
	@make generate-test-data

generate-test-data: ## Generate test chat files
	mkdir -p $(TEST_DIR)/chats/hformats $(TEST_DIR)/chats/merge
	uv run whatstk-generate-chat --size 500 -z --output-path $(TEST_DIR)/chats/hformats/
	uv run whatstk-generate-chat --size 300 --last-timestamp 2019-09-01 \
		--hformats '%Y-%m-%d, %H:%M - %name:' \
		--output-path $(TEST_DIR)/chats/merge/ --filenames file1.txt
	uv run whatstk-generate-chat --size 300 --last-timestamp 2020-01-01 \
		--hformats '%Y-%m-%d, %H:%M - %name:' \
		--output-path $(TEST_DIR)/chats/merge/ --filenames file2.txt


##################################################
# VERSION BUMPING
bump.patch: ## Bump patch version (0.0.X)
	uv run bump-my-version bump patch

bump.minor: ## Bump minor version (0.X.0)
	uv run bump-my-version bump minor

bump.major: ## Bump major version (X.0.0)
	uv run bump-my-version bump major


##################################################
# DOCUMENTATION
docs: ## Build documentation
	uv run make -C docs html

docs.serve: docs ## Build and serve documentation
	cd docs/_build/html && python -m http.server

