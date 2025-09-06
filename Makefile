# Makefile for AI Context Craft Tests - Universal version

.PHONY: help test test-quick test-full test-local test-docker clean setup check

# Colors
GREEN := \033[0;32m
BLUE := \033[0;34m
YELLOW := \033[1;33m
NC := \033[0m

help: ## Show this help
	@echo "$(BLUE)AI Context Craft - Test Commands$(NC)"
	@echo "================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-15s$(NC) %s\n", $1, $2}'

# Main test commands
test: ## Run all tests (auto-detect Docker/Local)
	@./run-tests.sh test

test-quick: ## Run quick tests (skip slow)
	@./run-tests.sh quick

test-full: ## Run full test suite with coverage
	@./run-tests.sh full

test-local: ## Force local Python tests
	@./run-tests.sh local

test-docker: ## Force Docker tests
	@FORCE_DOCKER=true ./run-tests.sh test

test-specific: ## Run specific test (use TEST=name)
	@./run-tests.sh specific

test-shell: ## Open interactive test shell
	@./run-tests.sh shell

# Utility commands
clean: ## Clean test results
	@./run-tests.sh clean

report: ## Show test report in browser
	@./run-tests.sh report

check: ## Check test environment
	@echo "$(BLUE)Checking test environment...$(NC)"
	@echo -n "Script executable: "; \
		if [ -x run-tests.sh ]; then echo "$(GREEN)✓$(NC)"; else echo "$(YELLOW)✗$(NC)"; fi
	@echo -n "Docker available: "; \
		if docker info >/dev/null 2>&1; then echo "$(GREEN)✓$(NC)"; else echo "$(YELLOW)✗ (will use Python)$(NC)"; fi
	@echo -n "Python available: "; \
		if python3 --version >/dev/null 2>&1; then echo "$(GREEN)✓$(NC)"; else echo "$(YELLOW)✗$(NC)"; fi
	@echo -n "Test file exists: "; \
		if [ -f tests/test_aicc_integration.py ]; then echo "$(GREEN)✓$(NC)"; else echo "$(YELLOW)✗$(NC)"; fi

setup: ## Setup test environment
	@echo "$(BLUE)Setting up test environment...$(NC)"
	@chmod +x run-tests.sh 2>/dev/null || true
	@chmod +x docker-run.sh 2>/dev/null || true
	@mkdir -p tests/test-results
	@if [ ! -f requirements-test.txt ]; then \
		echo "Creating requirements-test.txt..."; \
		echo "pytest>=7.4.0" > requirements-test.txt; \
		echo "pyyaml>=6.0" >> requirements-test.txt; \
		echo "pathspec>=0.11.0" >> requirements-test.txt; \
	fi
	@echo "$(GREEN)✅ Setup complete$(NC)"
	@echo "$(BLUE)Run 'make check' to verify environment$(NC)"

# CI/CD commands
ci: ## Run CI test suite (no Docker)
	@echo "$(BLUE)Running CI tests...$(NC)"
	@if [ -f /.dockerenv ]; then \
		echo "Already in Docker, using local Python..."; \
		pip install -q -r requirements-test.txt; \
		python -m pytest tests/test_aicc_integration.py -v; \
	else \
		python3 -m pip install -q -r requirements-test.txt; \
		python3 -m pytest tests/test_aicc_integration.py -v; \
	fi

# Installation helpers
install-deps: ## Install Python dependencies locally
	@echo "$(BLUE)Installing Python dependencies...$(NC)"
	@pip3 install -r requirements.txt -r requirements-test.txt
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

# Examples and help
examples: ## Show usage examples
	@echo "$(BLUE)Examples:$(NC)"
	@echo "  make setup                   # First time setup"
	@echo "  make check                   # Check environment"
	@echo "  make test                    # Run all tests"
	@echo "  make test-quick              # Quick tests only"
	@echo "  make test-local              # Force local Python"
	@echo "  make test-specific TEST=test_strip_comments"
	@echo "  make report                  # View HTML report"