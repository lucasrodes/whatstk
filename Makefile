.PHONY: help install install-dev test-data lint test clean

.DEFAULT_GOAL := help

PACKAGE_NAME := whatstk
TEST_DIR := tests
REPORTS_DIR := reports

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install package in editable mode
	pip install -e .

install-dev: ## Install package with dev dependencies
	pip install -e .[dev]

test-data: ## Generate test chat files
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
	pytest \
		--html=$(REPORTS_DIR)/testreport.html \
		--cov-report html:$(REPORTS_DIR)/htmlcov \
		--cov-report term \
		--cov-report xml:$(REPORTS_DIR)/cov.xml \
		--cov=$(PACKAGE_NAME) $(TEST_DIR)

clean: ## Remove build and test artifacts
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf $(REPORTS_DIR) .pytest_cache .coverage htmlcov build dist *.egg-info
