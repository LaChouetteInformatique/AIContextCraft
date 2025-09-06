# AI Context Craft - Python Test System Makefile
# Simplified Makefile for Python-based testing

.PHONY: help test test-quick test-full test-watch setup clean docker-build \
        pytest coverage report shell monitor view-results ci

# Configuration
PROJECT_NAME := aicontextcraft
TEST_IMAGE := $(PROJECT_NAME):test
RUNNER_IMAGE := aicc-test-runner:latest
TEST_DIR := tests

# Colors
RED := \033[0;31m
GREEN := \033[0;32m
BLUE := \033[0;34m
NC := \033[0m

# Default target
.DEFAULT_GOAL := help

help: ## Show this help
	@echo "$(BLUE)AI Context Craft - Python Test System$(NC)"
	@echo "======================================"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

# Setup and build
setup: ## Initial setup of test environment
	@echo "$(BLUE)Setting up test environment...$(NC)"
	@bash $(TEST_DIR)/test-project-setup.sh 2>/dev/null || echo "Test project setup script not found"
	@$(MAKE) docker-build
	@echo "$(GREEN)✓ Setup complete$(NC)"

docker-build: ## Build Docker images for testing
	@echo "$(BLUE)Building Docker images...$(NC)"
	@docker build -t $(TEST_IMAGE) .
	@docker build -f $(TEST_DIR)/Dockerfile.test -t $(RUNNER_IMAGE) .
	@echo "$(GREEN)✓ Images built$(NC)"

# Main test commands
test: docker-build ## Run default test suite
	@./run-tests.sh test

test-quick: docker-build ## Run quick smoke tests
	@./run-tests.sh test --quick

test-full: docker-build ## Run complete test suite
	@./run-tests.sh test --full

pytest: docker-build ## Run tests with pytest
	@./run-tests.sh pytest

coverage: docker-build ## Run tests with coverage report
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/app/tests \
		-v $(PWD)/utils:/app/utils:ro \
		-v $(PWD)/main.py:/app/main.py:ro \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-e PYTHONPATH=/app \
		$(RUNNER_IMAGE) \
		pytest /app/tests --cov=/app/utils --cov-report=html:/app/tests/test-results/coverage

# Specific test groups
test-basic: docker-build ## Run basic functionality tests
	@./run-tests.sh test --groups basic

test-config: docker-build ## Run configuration tests
	@./run-tests.sh test --groups config

test-patterns: docker-build ## Run pattern matching tests
	@./run-tests.sh test --groups patterns

test-edge: docker-build ## Run edge case tests
	@./run-tests.sh test --groups edge

test-features: docker-build ## Run advanced feature tests
	@./run-tests.sh test --groups features

# Development tools
shell: docker-build ## Open interactive shell for debugging
	@./run-tests.sh debug

monitor: ## Monitor test execution in real-time
	@./run-tests.sh monitor

view-results: ## View test results in browser (http://localhost:8080)
	@./run-tests.sh view

test-watch: ## Watch for changes and run tests automatically
	@echo "$(BLUE)Watching for changes...$(NC)"
	@while true; do \
		inotifywait -qre modify utils/ main.py 2>/dev/null && \
		echo "$(BLUE)Changes detected, running tests...$(NC)" && \
		$(MAKE) test-quick; \
	done

# Reports and analysis
report: ## Generate and display test report
	@if [ -d "$(TEST_DIR)/test-results" ]; then \
		echo "$(BLUE)Latest Test Results:$(NC)"; \
		ls -lt $(TEST_DIR)/test-results/*.json 2>/dev/null | head -5; \
		echo ""; \
		if [ -f "$(TEST_DIR)/test-results/report.html" ]; then \
			echo "HTML report: file://$(PWD)/$(TEST_DIR)/test-results/report.html"; \
		fi; \
	else \
		echo "$(RED)No test results found$(NC)"; \
	fi

# Continuous Integration
ci: docker-build ## Run CI test suite
	@echo "$(BLUE)Running CI tests...$(NC)"
	@./run-tests.sh test --quick || exit 1
	@./run-tests.sh test --groups basic config patterns || exit 1
	@echo "$(GREEN)✓ CI tests passed$(NC)"

ci-full: docker-build ## Run full CI test suite with coverage
	@echo "$(BLUE)Running full CI suite...$(NC)"
	@$(MAKE) coverage
	@$(MAKE) test-full
	@echo "$(GREEN)✓ Full CI tests passed$(NC)"

# Cleanup
clean: ## Clean test artifacts and results
	@echo "$(BLUE)Cleaning test artifacts...$(NC)"
	@rm -rf $(TEST_DIR)/test-results
	@rm -rf $(TEST_DIR)/scenario-results
	@rm -rf $(TEST_DIR)/__pycache__
	@rm -rf $(TEST_DIR)/.pytest_cache
	@find $(TEST_DIR) -name "*.pyc" -delete 2>/dev/null || true
	@docker-compose -f docker-compose.test.yml down -v 2>/dev/null || true
	@echo "$(GREEN)✓ Cleaned$(NC)"

clean-all: clean ## Clean everything including Docker images
	@echo "$(BLUE)Cleaning all test data...$(NC)"
	@rm -rf $(TEST_DIR)/test-project
	@docker rmi $(TEST_IMAGE) 2>/dev/null || true
	@docker rmi $(RUNNER_IMAGE) 2>/dev/null || true
	@echo "$(GREEN)✓ All cleaned$(NC)"

# Docker compose commands
compose-up: ## Start test environment with docker-compose
	@docker-compose -f docker-compose.test.yml up -d

compose-down: ## Stop test environment
	@docker-compose -f docker-compose.test.yml down

compose-logs: ## Show docker-compose logs
	@docker-compose -f docker-compose.test.yml logs -f

# Validation
validate: ## Validate test setup
	@echo "$(BLUE)Validating test setup...$(NC)"
	@echo -n "Docker: "
	@if command -v docker >/dev/null 2>&1; then echo "$(GREEN)✓$(NC)"; else echo "$(RED)✗$(NC)"; fi
	@echo -n "Test project: "
	@if [ -d "$(TEST_DIR)/test-project" ]; then echo "$(GREEN)✓$(NC)"; else echo "$(RED)✗$(NC)"; fi
	@echo -n "Test runner: "
	@if [ -f "run-tests.sh" ]; then echo "$(GREEN)✓$(NC)"; else echo "$(RED)✗$(NC)"; fi
	@echo -n "Docker image: "
	@if docker image inspect $(TEST_IMAGE) >/dev/null 2>&1; then echo "$(GREEN)✓$(NC)"; else echo "$(RED)✗$(NC)"; fi

# Performance testing
perf: docker-build ## Run performance benchmarks
	@echo "$(BLUE)Running performance tests...$(NC)"
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/app/tests \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-e PYTHONPATH=/app \
		$(RUNNER_IMAGE) \
		pytest /app/tests/test_aicc_integration.py::TestPerformance -v

# Quick commands for development
q: test-quick ## Alias for test-quick
f: test-full ## Alias for test-full
s: shell ## Alias for shell
c: clean ## Alias for clean

.SILENT: help validate report