.PHONY: help setup install-dev lint format test dev build build-no-cache docker-run docker-down clean

# Variables
PYTHON := python3.12
UV := uv
DOCKER_COMPOSE := docker-compose

# Colors for output
CYAN := \033[0;36m
GREEN := \033[0;32m
RESET := \033[0m

help: ## Show this help message
	@echo "$(CYAN)Available commands:$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(RESET) %s\n", $$1, $$2}'

# ============================================================================
# Setup & Dependencies
# ============================================================================

setup: ## Complete development setup (installs uv, creates venv, installs deps)
	@echo "$(CYAN)Setting up development environment...$(RESET)"
	@command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
	@$(UV) venv .venv --python $(PYTHON)
	@$(UV) pip install -e ".[dev]"
	@pre-commit install
	@echo "$(GREEN)Setup complete! Run 'source .venv/bin/activate' to activate$(RESET)"

install-dev: ## Install/update development dependencies
	@echo "$(CYAN)Installing development dependencies...$(RESET)"
	@$(UV) pip install -e ".[dev]"
	@echo "$(GREEN)Dependencies installed!$(RESET)"

# ============================================================================
# Code Quality
# ============================================================================

lint: install-dev ## Run all linting checks (ruff, black, mypy)
	@echo "$(CYAN)Running linting checks...$(RESET)"
	@$(UV) run ruff check src/
	@$(UV) run black --check src/
	@$(UV) run mypy src/
	@echo "$(GREEN)All checks passed!$(RESET)"

format: install-dev ## Auto-format code with ruff and black
	@echo "$(CYAN)Formatting code...$(RESET)"
	@$(UV) run ruff check --fix src/
	@$(UV) run black src/
	@echo "$(GREEN)Code formatted!$(RESET)"

# ============================================================================
# Testing
# ============================================================================

test: ## Run tests (use COVERAGE=1 for coverage report)
	@echo "$(CYAN)Running tests...$(RESET)"
	@if [ "$(COVERAGE)" = "1" ]; then \
		$(UV) run pytest tests/ --cov=src --cov-report=term-missing --cov-report=html -v --tb=short; \
		echo "$(GREEN)Coverage report generated in htmlcov/$(RESET)"; \
	else \
		$(UV) run pytest tests/ -v --tb=short; \
	fi
	@echo "$(GREEN)Tests complete!$(RESET)"

# ============================================================================
# Development
# ============================================================================

dev: ## Run server locally with hot reload
	@echo "$(CYAN)Starting development server...$(RESET)"
	@$(UV) run uvicorn server:app --host 0.0.0.0 --port 8080 --reload --app-dir src/

# ============================================================================
# Docker
# ============================================================================

build: ## Build Docker image
	@echo "$(CYAN)Building Docker image...$(RESET)"
	@$(DOCKER_COMPOSE) build
	@echo "$(GREEN)Image built!$(RESET)"

build-no-cache: ## Build Docker image without cache
	@echo "$(CYAN)Building Docker image (no cache)...$(RESET)"
	@$(DOCKER_COMPOSE) build --no-cache
	@echo "$(GREEN)Image rebuilt from scratch!$(RESET)"

docker-run: ## Run in Docker (use MODE=dev|prod, default=dev)
	@echo "$(CYAN)Starting Docker container (mode: $(or $(MODE),dev))...$(RESET)"
	@if [ "$(MODE)" = "prod" ]; then \
		$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml up -d; \
		echo "$(GREEN)Prod server started in background$(RESET)"; \
	else \
		$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.dev.yml up -d; \
		echo "$(GREEN)Dev server started in background$(RESET)"; \
	fi

docker-down: ## Stop and remove Docker containers
	@echo "$(CYAN)Stopping Docker containers...$(RESET)"
	@$(DOCKER_COMPOSE) down -v --remove-orphans
	@echo "$(GREEN)Containers stopped and removed!$(RESET)"

# ============================================================================
# Cleanup
# ============================================================================

clean: ## Clean all generated files and Docker containers
	@echo "$(CYAN)Cleaning up...$(RESET)"
	@rm -rf .venv __pycache__ .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov
	@rm -rf *.egg-info build dist
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@$(DOCKER_COMPOSE) down -v --remove-orphans 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete!$(RESET)"
