#!/bin/bash
# run-tests.sh - Universal test runner for AI Context Craft
# Works on: Linux, macOS, Windows (WSL2), CI/CD

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"
TEST_DIR="$PROJECT_ROOT/tests"
RESULTS_DIR="$TEST_DIR/test-results"

# Detect platform
detect_platform() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if grep -qi microsoft /proc/version 2>/dev/null; then
            echo "wsl2"
        else
            echo "linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

PLATFORM=$(detect_platform)

# Functions
print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}     🧪 AI Context Craft - Test Runner${NC}"
    echo -e "${BLUE}     Platform: ${PLATFORM}${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_help() {
    cat << EOF

Usage: ./run-tests.sh [COMMAND] [OPTIONS]

Commands:
    test        Run all tests (default)
    quick       Run quick tests only
    full        Run full test suite with coverage
    specific    Run specific test (use TEST=test_name)
    shell       Open interactive Python shell
    local       Run tests locally without Docker
    clean       Clean test results
    report      Show last test report

Examples:
    ./run-tests.sh                    # Run all tests
    ./run-tests.sh quick              # Quick tests only
    ./run-tests.sh specific TEST=test_basic_concatenation
    ./run-tests.sh local              # Use local Python

EOF
}

setup_environment() {
    echo -e "${BLUE}🔧 Setting up test environment...${NC}"
    
    # Create results directory
    mkdir -p "$RESULTS_DIR"
    
    # Check Docker (optional)
    if docker info > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Docker available${NC}"
        DOCKER_AVAILABLE=true
    else
        echo -e "${YELLOW}⚠ Docker not available, will use local Python${NC}"
        DOCKER_AVAILABLE=false
    fi
}

# Docker test runner with improved volume handling
run_tests_docker() {
    local test_args="$1"
    
    if [ "$DOCKER_AVAILABLE" != "true" ]; then
        echo -e "${YELLOW}Docker not available, falling back to local Python${NC}"
        run_tests_local "$test_args"
        return
    fi
    
    echo -e "${BLUE}🐳 Running tests in Docker...${NC}"
    
    # Create a temporary Dockerfile for testing
    cat > "$TEST_DIR/.dockerfile.test" << 'DOCKERFILE'
FROM python:3.11-slim
WORKDIR /app
# Install dependencies
RUN pip install --no-cache-dir pyyaml pathspec pytest pytest-html pytest-cov
RUN pip install --no-cache-dir tiktoken tree-sitter tree-sitter-languages
# Copy application code
COPY . /app
# Run tests
CMD ["python", "-m", "pytest", "tests/test_aicc_integration.py", "-v"]
DOCKERFILE
    
    # Build test image
    echo -e "${BLUE}Building test image...${NC}"
    docker build -f "$TEST_DIR/.dockerfile.test" -t aicc-test:latest . > /dev/null 2>&1
    
    # Run tests
    docker run --rm \
        -v "$RESULTS_DIR":/app/tests/test-results \
        aicc-test:latest \
        python -m pytest tests/test_aicc_integration.py \
            $test_args \
            --tb=short \
            --junit-xml=/app/tests/test-results/junit.xml \
            --html=/app/tests/test-results/report.html \
            --self-contained-html
    
    # Clean up
    rm -f "$TEST_DIR/.dockerfile.test"
}

# Local Python test runner (fallback and faster for development)
run_tests_local() {
    local test_args="$1"
    
    echo -e "${BLUE}🐍 Running tests with local Python...${NC}"
    
    # Check Python
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        echo -e "${RED}❌ Python not found. Please install Python 3.8+${NC}"
        exit 1
    fi
    
    # Use python3 if available, otherwise python
    PYTHON_CMD=$(command -v python3 || command -v python)
    
    # Check/Install dependencies
    echo -e "${BLUE}Checking dependencies...${NC}"
    $PYTHON_CMD -m pip install --quiet --user pyyaml pathspec pytest pytest-html pytest-cov 2>/dev/null || {
        echo -e "${YELLOW}Installing in virtual environment...${NC}"
        $PYTHON_CMD -m venv venv
        source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null || true
        pip install --quiet pyyaml pathspec pytest pytest-html pytest-cov
        pip install --quiet tiktoken tree-sitter tree-sitter-languages
    }
    
    # Run tests
    echo -e "${BLUE}Running tests...${NC}"
    $PYTHON_CMD -m pytest tests/test_aicc_integration.py \
        $test_args \
        --tb=short \
        --junit-xml="$RESULTS_DIR/junit.xml" \
        --html="$RESULTS_DIR/report.html" \
        --self-contained-html
}

# Main test runner that chooses the best method
run_tests() {
    local test_args="$1"
    
    # Prefer Docker if available, but allow override
    if [ "$FORCE_LOCAL" == "true" ] || [ "$2" == "local" ]; then
        run_tests_local "$test_args"
    elif [ "$DOCKER_AVAILABLE" == "true" ]; then
        # Try Docker first, fallback to local if it fails
        run_tests_docker "$test_args" || {
            echo -e "${YELLOW}Docker failed, trying local Python...${NC}"
            run_tests_local "$test_args"
        }
    else
        run_tests_local "$test_args"
    fi
}

run_quick_tests() {
    echo -e "${YELLOW}⚡ Running quick tests only...${NC}"
    run_tests "-v -m 'not slow'"
}

run_full_tests() {
    echo -e "${YELLOW}📋 Running full test suite with coverage...${NC}"
    run_tests "-v --cov=utils --cov-report=html:$RESULTS_DIR/coverage --cov-report=term"
}

run_specific_test() {
    local test_name="${TEST:-test_basic_concatenation}"
    echo -e "${YELLOW}🎯 Running specific test: $test_name${NC}"
    run_tests "-v -k $test_name"
}

open_shell() {
    echo -e "${BLUE}🐍 Opening Python shell for debugging...${NC}"
    
    if [ "$DOCKER_AVAILABLE" == "true" ]; then
        docker run --rm -it \
            -v "$PROJECT_ROOT":/app \
            -w /app \
            python:3.11-slim \
            bash -c "
                pip install --quiet pyyaml pathspec pytest ipython
                pip install --quiet tiktoken tree-sitter tree-sitter-languages
                echo ''
                echo 'Python test environment ready!'
                echo 'Try: python -m pytest tests/test_aicc_integration.py -v'
                echo ''
                /bin/bash
            "
    else
        echo "Starting local Python shell..."
        python3 -i -c "
import sys
sys.path.insert(0, '.')
from utils.app import AIContextCraft
print('AIContextCraft loaded. Try: aicc = AIContextCraft()')
"
    fi
}

show_report() {
    if [ -f "$RESULTS_DIR/report.html" ]; then
        echo -e "${GREEN}📊 Test report available at:${NC}"
        echo "file://$RESULTS_DIR/report.html"
        
        # Try to open in browser
        if [[ "$PLATFORM" == "wsl2" ]]; then
            # WSL2: use Windows browser
            cmd.exe /c start "$RESULTS_DIR/report.html" 2>/dev/null || true
        elif command -v xdg-open > /dev/null; then
            xdg-open "$RESULTS_DIR/report.html" 2>/dev/null || true
        elif command -v open > /dev/null; then
            open "$RESULTS_DIR/report.html" 2>/dev/null || true
        fi
    else
        echo -e "${YELLOW}No report found. Run tests first.${NC}"
    fi
}

clean_results() {
    echo -e "${BLUE}🧹 Cleaning test results...${NC}"
    rm -rf "$RESULTS_DIR"
    rm -f "$TEST_DIR/.dockerfile.test"
    mkdir -p "$RESULTS_DIR"
    echo -e "${GREEN}✅ Cleaned${NC}"
}

# Main execution
print_header
setup_environment

# Parse command
case "${1:-test}" in
    test)
        run_tests "-v"
        ;;
    quick)
        run_quick_tests
        ;;
    full)
        run_full_tests
        ;;
    specific)
        run_specific_test
        ;;
    local)
        FORCE_LOCAL=true run_tests "-v"
        ;;
    shell|debug)
        open_shell
        ;;
    report)
        show_report
        ;;
    clean)
        clean_results
        ;;
    help|--help|-h)
        print_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        print_help
        exit 1
        ;;
esac

# Show summary if tests were run
if [[ "$1" == "test" || "$1" == "quick" || "$1" == "full" || "$1" == "specific" || "$1" == "local" ]]; then
    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    if [ -f "$RESULTS_DIR/report.html" ]; then
        echo -e "${GREEN}✅ Tests completed!${NC}"
        echo -e "📊 HTML Report: ${BLUE}$RESULTS_DIR/report.html${NC}"
        echo -e "📄 JUnit XML: ${BLUE}$RESULTS_DIR/junit.xml${NC}"
        if [ -d "$RESULTS_DIR/coverage" ]; then
            echo -e "📈 Coverage: ${BLUE}$RESULTS_DIR/coverage/index.html${NC}"
        fi
    fi
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
fi