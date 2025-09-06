#!/bin/bash
# ============================================================
# AI Context Craft - Update Script
# Updates the project and its dependencies
# ============================================================

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

print_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  🔄 AI Context Craft - Update Script${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

check_git() {
    if [ -d ".git" ]; then
        echo -e "${GREEN}✓ Git repository detected${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ Not a Git repository${NC}"
        return 1
    fi
}

update_git() {
    echo -e "${BLUE}📥 Pulling latest changes from Git...${NC}"
    
    # Check for uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        echo -e "${YELLOW}⚠ Uncommitted changes detected${NC}"
        read -p "Stash changes and continue? (Y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            git stash push -m "Auto-stash before update $(date +%Y%m%d-%H%M%S)"
            echo -e "${GREEN}✓ Changes stashed${NC}"
            STASHED=true
        else
            echo -e "${RED}Update cancelled. Please commit or stash your changes.${NC}"
            exit 1
        fi
    fi
    
    # Pull latest changes
    git pull origin main || git pull origin master || git pull
    
    echo -e "${GREEN}✓ Git updated${NC}"
    
    # Restore stashed changes if any
    if [ "$STASHED" = true ]; then
        echo -e "${BLUE}Restoring stashed changes...${NC}"
        git stash pop || {
            echo -e "${YELLOW}⚠ Could not restore stashed changes automatically${NC}"
            echo "Your changes are saved in: git stash list"
        }
    fi
}

update_dependencies() {
    echo -e "${BLUE}📦 Updating Python dependencies...${NC}"
    
    # Check for virtual environment
    if [ -d "venv" ]; then
        if [ -f "venv/bin/activate" ]; then
            source venv/bin/activate
        elif [ -f "venv/Scripts/activate" ]; then
            source venv/Scripts/activate
        fi
        PIP_CMD="pip"
        echo -e "${GREEN}✓ Virtual environment activated${NC}"
    else
        echo -e "${YELLOW}⚠ No virtual environment found, using global pip${NC}"
        PIP_CMD="python3 -m pip"
    fi
    
    # Upgrade pip
    echo "Upgrading pip..."
    $PIP_CMD install --upgrade pip
    
    # Update dependencies
    if [ -f "requirements.txt" ]; then
        echo "Updating main dependencies..."
        $PIP_CMD install --upgrade -r requirements.txt
        echo -e "${GREEN}✓ Main dependencies updated${NC}"
    fi
    
    if [ -f "requirements-test.txt" ]; then
        read -p "Update test dependencies? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Updating test dependencies..."
            $PIP_CMD install --upgrade -r requirements-test.txt
            echo -e "${GREEN}✓ Test dependencies updated${NC}"
        fi
    fi
}

update_docker() {
    echo -e "${BLUE}🐳 Checking Docker...${NC}"
    
    if command -v docker &> /dev/null && docker ps &> /dev/null; then
        echo -e "${GREEN}✓ Docker is available${NC}"
        
        read -p "Rebuild Docker image? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${BLUE}Building Docker image...${NC}"
            docker build -t aicontextcraft:latest . --no-cache
            echo -e "${GREEN}✓ Docker image rebuilt${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ Docker not available or not running${NC}"
    fi
}

run_tests() {
    echo -e "${BLUE}🧪 Running tests...${NC}"
    
    read -p "Run tests to verify update? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        # Try Docker first
        if command -v docker &> /dev/null && docker ps &> /dev/null; then
            ./run-tests.sh quick || {
                echo -e "${YELLOW}⚠ Some tests failed${NC}"
            }
        else
            # Fallback to Python
            if [ -d "venv" ] && [ -f "venv/bin/python" ]; then
                venv/bin/python -m pytest tests/test_aicc_integration.py -v --tb=short || {
                    echo -e "${YELLOW}⚠ Some tests failed${NC}"
                }
            else
                python3 -m pytest tests/test_aicc_integration.py -v --tb=short || {
                    echo -e "${YELLOW}⚠ Some tests failed${NC}"
                }
            fi
        fi
    fi
}

show_changelog() {
    echo -e "${BLUE}📋 Recent changes:${NC}"
    
    if [ -d ".git" ]; then
        # Show last 5 commits
        git log --oneline -5 2>/dev/null || echo "No commit history available"
    else
        echo "No Git history available"
    fi
}

print_summary() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ Update Complete!${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    # Show version if available
    if [ -f "venv/bin/python" ]; then
        VERSION=$(venv/bin/python main.py --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "unknown")
    else
        VERSION=$(python3 main.py --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "unknown")
    fi
    
    echo "Current version: $VERSION"
    echo ""
    echo "Next steps:"
    echo "  • Run 'python main.py --help' to see new features"
    echo "  • Check README.md for updated documentation"
    echo "  • Report issues at: https://github.com/LaChouetteInformatique/AIContextCraft/issues"
    echo ""
}

# Main update flow
main() {
    print_header
    
    # Update from Git if available
    if check_git; then
        update_git
        show_changelog
    fi
    
    # Update Python dependencies
    update_dependencies
    
    # Update Docker if available
    update_docker
    
    # Run tests
    run_tests
    
    # Show summary
    print_summary
}

# Run main update
main "$@"