#!/bin/bash
# AI Context Craft - Test Launcher
# This script orchestrates the Python test runner with Docker

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TEST_DIR="$PROJECT_ROOT/tests"

# Helper functions
log() { echo -e "$1"; }
log_info() { log "${BLUE}ℹ️  $1${NC}"; }
log_success() { log "${GREEN}✅ $1${NC}"; }
log_error() { log "${RED}❌ $1${NC}"; }
log_warning() { log "${YELLOW}⚠️  $1${NC}"; }

# Show banner
show_banner() {
    echo -e "${BOLD}${CYAN}"
    echo "╔═══════════════════════════════════════╗"
    echo "║   AI Context Craft Test System       ║"
    echo "║         Python Test Runner            ║"
    echo "╚═══════════════════════════════════════╝"
    echo -e "${NC}"
}

# Check prerequisites
check_prerequisites() {
    local missing=()
    
    if ! command -v docker &> /dev/null; then
        missing+=("docker")
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        missing+=("docker-compose")
    fi
    
    if [ ${#missing[@]} -gt 0 ]; then
        log_error "Missing required tools: ${missing[*]}"
        exit 1
    fi
}

# Build test environment
build_environment() {
    log_info "Building test environment..."
    
    # Build main application image
    docker build -t aicontextcraft:test "$PROJECT_ROOT" || {
        log_error "Failed to build main application image"
        exit 1
    }
    
    # Build test runner image
    docker build -f "$TEST_DIR/Dockerfile.test" -t aicc-test-runner:latest "$PROJECT_ROOT" || {
        log_error "Failed to build test runner image"
        exit 1
    }
    
    log_success "Test environment built"
}

# Setup test project
setup_test_project() {
    if [ ! -d "$TEST_DIR/test-project" ]; then
        log_info "Creating test project..."
        
        if [ -f "$TEST_DIR/test-project-setup.sh" ]; then
            bash "$TEST_DIR/test-project-setup.sh"
        else
            log_warning "test-project-setup.sh not found, skipping test project creation"
        fi
    fi
}

# Run tests with docker-compose
run_tests() {
    local test_args="$@"
    
    log_info "Running tests..."
    
    # Start test runner
    docker-compose -f "$PROJECT_ROOT/docker-compose.test.yml" run --rm test-runner \
        python test_runner.py $test_args
    
    local exit_code=$?
    
    # Clean up
    docker-compose -f "$PROJECT_ROOT/docker-compose.test.yml" down 2>/dev/null
    
    return $exit_code
}

# Run tests directly in Docker
run_tests_direct() {
    local test_args="$@"
    
    log_info "Running tests directly in Docker..."
    
    docker run --rm \
        -v "$TEST_DIR:/app/tests" \
        -v "$PROJECT_ROOT/utils:/app/utils:ro" \
        -v "$PROJECT_ROOT/main.py:/app/main.py:ro" \
        -v "$PROJECT_ROOT/config.yaml:/app/config.yaml:ro" \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -e PYTHONPATH=/app \
        -e DOCKER_HOST=unix:///var/run/docker.sock \
        --network host \
        aicc-test-runner:latest \
        python /app/tests/test_runner.py $test_args
}

# Run with pytest
run_pytest() {
    log_info "Running with pytest..."
    
    docker run --rm \
        -v "$TEST_DIR:/app/tests" \
        -v "$PROJECT_ROOT/utils:/app/utils:ro" \
        -v "$PROJECT_ROOT/main.py:/app/main.py:ro" \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -e PYTHONPATH=/app \
        aicc-test-runner:latest \
        pytest /app/tests -v --html=/app/tests/test-results/report.html --self-contained-html
}

# Interactive shell for debugging
debug_shell() {
    log_info "Opening debug shell..."
    
    docker run --rm -it \
        -v "$TEST_DIR:/app/tests" \
        -v "$PROJECT_ROOT/utils:/app/utils:ro" \
        -v "$PROJECT_ROOT/main.py:/app/main.py:ro" \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -e PYTHONPATH=/app \
        --network host \
        --entrypoint /bin/bash \
        aicc-test-runner:latest
}

# Monitor tests
monitor_tests() {
    log_info "Starting test monitor..."
    
    docker-compose -f "$PROJECT_ROOT/docker-compose.test.yml" \
        --profile monitor up test-monitor
}

# View test results
view_results() {
    log_info "Starting test result viewer on http://localhost:8080"
    
    # Create basic nginx config if not exists
    if [ ! -f "$TEST_DIR/nginx.conf" ]; then
        cat > "$TEST_DIR/nginx.conf" << 'EOF'
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        root /usr/share/nginx/html;
        index index.html;
        
        location / {
            autoindex on;
            autoindex_format html;
            autoindex_localtime on;
        }
        
        types {
            text/html html;
            text/plain txt log;
            application/json json;
        }
    }
}
EOF
    fi
    
    docker-compose -f "$PROJECT_ROOT/docker-compose.test.yml" \
        --profile viewer up -d test-viewer
    
    log_success "Result viewer started at http://localhost:8080"
}

# Clean test environment
clean_environment() {
    log_info "Cleaning test environment..."
    
    # Stop all containers
    docker-compose -f "$PROJECT_ROOT/docker-compose.test.yml" down -v 2>/dev/null || true
    
    # Remove test results
    rm -rf "$TEST_DIR/test-results"
    rm -rf "$TEST_DIR/scenario-results"
    rm -rf "$TEST_DIR/__pycache__"
    find "$TEST_DIR" -name "*.pyc" -delete 2>/dev/null || true
    
    # Remove test project
    if [ "$1" == "--all" ]; then
        rm -rf "$TEST_DIR/test-project"
        docker rmi aicc-test-runner:latest 2>/dev/null || true
        docker rmi aicontextcraft:test 2>/dev/null || true
    fi
    
    log_success "Environment cleaned"
}

# Show usage
show_usage() {
    cat << EOF
${BOLD}AI Context Craft - Python Test System${NC}

${BOLD}Usage:${NC}
  $0 [COMMAND] [OPTIONS]

${BOLD}Commands:${NC}
  test [OPTIONS]     Run tests (default)
  build             Build test environment
  setup             Setup test project
  pytest            Run with pytest
  debug             Open debug shell
  monitor           Monitor test execution
  view              View test results (web)
  clean             Clean test environment
  clean --all       Clean everything including images

${BOLD}Test Options:${NC}
  --quick           Run quick tests only
  --full            Run all tests
  --groups GROUP    Run specific test groups
  --report FORMAT   Report format (json, html)
  --verbose         Verbose output

${BOLD}Examples:${NC}
  $0                      # Run default tests
  $0 test --quick         # Run quick tests
  $0 test --groups basic  # Run basic tests only
  $0 pytest              # Run with pytest
  $0 debug               # Open debug shell
  $0 monitor             # Monitor tests in another terminal

${BOLD}Test Groups:${NC}
  basic      Basic functionality tests
  config     Configuration tests
  patterns   Pattern matching tests
  edge       Edge cases tests
  features   Advanced features tests

EOF
}

# Main execution
main() {
    show_banner
    check_prerequisites
    
    # Parse command
    local command="${1:-test}"
    shift || true
    
    case "$command" in
        test)
            build_environment
            setup_test_project
            run_tests "$@"
            ;;
        build)
            build_environment
            ;;
        setup)
            setup_test_project
            ;;
        pytest)
            build_environment
            setup_test_project
            run_pytest
            ;;
        debug)
            build_environment
            debug_shell
            ;;
        monitor)
            monitor_tests
            ;;
        view)
            view_results
            ;;
        clean)
            clean_environment "$@"
            ;;
        help|--help|-h)
            show_usage
            exit 0
            ;;
        *)
            # Assume it's test options if not a recognized command
            build_environment
            setup_test_project
            run_tests "$command" "$@"
            ;;
    esac
    
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        log_success "Tests completed successfully!"
    else
        log_error "Tests failed with exit code $exit_code"
    fi
    
    exit $exit_code
}

# Run main
main "$@"