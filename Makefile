.PHONY: help setup lint test docker-up docker-down clean format check

# Default target
help: ## Show this help message
	@echo "Insider Threat Detection System — Developer Commands"
	@echo "===================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Set up development environment
	python -m pip install --upgrade pip
	pip install -e ".[dev]"
	cd frontend && npm install

format: ## Format all Python code
	black backend/ ai/ graph/ tests/ scripts/
	isort backend/ ai/ graph/ tests/ scripts/

lint: ## Run all linters
	black --check backend/ ai/ graph/ tests/
	isort --check-only backend/ ai/ graph/ tests/
	flake8 backend/ ai/ graph/ tests/
	mypy backend/ ai/ graph/

test: ## Run all tests
	pytest tests/ -v --tb=short

test-unit: ## Run unit tests only
	pytest tests/unit/ -v --tb=short

test-integration: ## Run integration tests only
	pytest tests/integration/ -v --tb=short

docker-up: ## Start all Docker services
	docker-compose -f deployment/docker-compose.yml \
		-f deployment/docker-compose.dev.yml up -d --build

docker-down: ## Stop all Docker services
	docker-compose -f deployment/docker-compose.yml \
		-f deployment/docker-compose.dev.yml down

clean: ## Clean generated files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage coverage.xml
	rm -rf frontend/dist frontend/node_modules/.cache

check: lint test ## Run lint + test
