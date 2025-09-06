# AI Context Craft - Makefile with selective testing

.PHONY: help test setup clean docker-build shell

# Configuration
PROJECT_NAME := aicontextcraft
DOCKER_IMAGE := $(PROJECT_NAME):test
TEST_DIR := tests
TEST_FILE := test_aicontextcraft.py

# Colors
GREEN := \033[0;32m
BLUE := \033[0;34m
YELLOW := \033[1;33m
NC := \033[0m

help: ## Show this help
	@echo "$(BLUE)AI Context Craft - Test System$(NC)"
	@echo "=============================="
	@echo ""
	@echo "$(GREEN)Basic commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		grep -v "^test-" | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Selective test commands:$(NC)"
	@grep -E '^test-[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

# ========== SETUP ==========
setup: docker-build ## Setup test environment
	@echo "$(BLUE)Setting up test environment...$(NC)"
	@bash $(TEST_DIR)/test-project-setup.sh 2>/dev/null || true
	@echo "$(GREEN)✓ Setup complete$(NC)"

docker-build: ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(NC)"
	@docker build -t $(DOCKER_IMAGE) .
	@echo "$(GREEN)✓ Image built$(NC)"

# ========== MAIN TEST COMMANDS ==========
test: setup ## Run all tests
	@echo "$(BLUE)Running all tests...$(NC)"
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/tests \
		-v /var/run/docker.sock:/var/run/docker.sock \
		$(DOCKER_IMAGE) \
		python -m pytest /tests/$(TEST_FILE) -v

test-quick: setup ## Run quick tests (skip slow)
	@echo "$(BLUE)Running quick tests...$(NC)"
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/tests \
		-v /var/run/docker.sock:/var/run/docker.sock \
		$(DOCKER_IMAGE) \
		python -m pytest /tests/$(TEST_FILE) -v -m "not slow"

# ========== SELECTIVE TEST COMMANDS ==========
test-basic: setup ## Run basic tests only
	@echo "$(BLUE)Running basic tests...$(NC)"
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/tests \
		-v /var/run/docker.sock:/var/run/docker.sock \
		$(DOCKER_IMAGE) \
		python -m pytest /tests/$(TEST_FILE) -v -m basic

test-config: setup ## Run configuration tests
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/tests \
		-v /var/run/docker.sock:/var/run/docker.sock \
		$(DOCKER_IMAGE) \
		python -m pytest /tests/$(TEST_FILE) -v -m config

test-features: setup ## Run feature tests
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/tests \
		-v /var/run/docker.sock:/var/run/docker.sock \
		$(DOCKER_IMAGE) \
		python -m pytest /tests/$(TEST_FILE) -v -m features

test-git: setup ## Run git integration tests
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/tests \
		-v /var/run/docker.sock:/var/run/docker.sock \
		$(DOCKER_IMAGE) \
		python -m pytest /tests/$(TEST_FILE) -v -m git

test-edge: setup ## Run edge case tests
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/tests \
		-v /var/run/docker.sock:/var/run/docker.sock \
		$(DOCKER_IMAGE) \
		python -m pytest /tests/$(TEST_FILE) -v -m edge

test-performance: setup ## Run performance tests
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/tests \
		-v /var/run/docker.sock:/var/run/docker.sock \
		$(DOCKER_IMAGE) \
		python -m pytest /tests/$(TEST_FILE) -v -m performance

test-regression: setup ## Run regression tests
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/tests \
		-v /var/run/docker.sock:/var/run/docker.sock \
		$(DOCKER_IMAGE) \
		python -m pytest /tests/$(TEST_FILE) -v -m regression

# ========== SPECIFIC TEST PATTERNS ==========
test-one: setup ## Run one specific test (use TEST=test_name)
	@echo "$(BLUE)Running test: $(TEST)$(NC)"
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/tests \
		-v /var/run/docker.sock:/var/run/docker.sock \
		$(DOCKER_IMAGE) \
		python -m pytest /tests/$(TEST_FILE) -v -k "$(TEST)"

test-class: setup ## Run tests from a class (use CLASS=TestBasic)
	@echo "$(BLUE)Running class: $(CLASS)$(NC)"
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/tests \
		-v /var/run/docker.sock:/var/run/docker.sock \
		$(DOCKER_IMAGE) \
		python -m pytest /tests/$(TEST_FILE)::$(CLASS) -v

# ========== DEBUG & DEVELOPMENT ==========
test-debug: setup ## Run tests with debug output
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/tests \
		-v /var/run/docker.sock:/var/run/docker.sock \
		$(DOCKER_IMAGE) \
		python -m pytest /tests/$(TEST_FILE) -vv -s

test-list: setup ## List all available tests
	@echo "$(BLUE)Available tests:$(NC)"
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/tests \
		$(DOCKER_IMAGE) \
		python -m pytest /tests/$(TEST_FILE) --collect-only -q

test-markers: ## Show available test markers
	@echo "$(BLUE)Available markers:$(NC)"
	@echo "  basic       - Basic functionality tests"
	@echo "  config      - Configuration tests"
	@echo "  features    - Feature tests"
	@echo "  git         - Git integration tests"
	@echo "  edge        - Edge case tests"
	@echo "  performance - Performance tests"
	@echo "  regression  - Regression tests"
	@echo "  slow        - Slow tests (excluded by test-quick)"

shell: ## Open shell in test container
	@docker run --rm -it \
		-v $(PWD):/app \
		-v $(PWD)/$(TEST_DIR)/test-project:/workspace \
		--entrypoint /bin/bash \
		$(DOCKER_IMAGE)

# ========== CLEANUP ==========
clean: ## Clean test artifacts
	@echo "$(BLUE)Cleaning...$(NC)"
	@rm -rf $(TEST_DIR)/test-results
	@rm -rf $(TEST_DIR)/__pycache__
	@rm -rf $(TEST_DIR)/.pytest_cache
	@find $(TEST_DIR) -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Cleaned$(NC)"

clean-all: clean ## Clean everything including Docker images
	@docker rmi $(DOCKER_IMAGE) 2>/dev/null || true
	@rm -rf $(TEST_DIR)/test-project
	@echo "$(GREEN)✓ All cleaned$(NC)"

# ========== CI/CD ==========
ci: setup ## Run CI test suite
	@echo "$(BLUE)Running CI tests...$(NC)"
	@docker run --rm \
		-v $(PWD)/$(TEST_DIR):/tests \
		-v /var/run/docker.sock:/var/run/docker.sock \
		$(DOCKER_IMAGE) \
		python -m pytest /tests/$(TEST_FILE) -v -m "not slow and not performance"