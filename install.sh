#!/bin/bash
# ============================================================
# AI Context Craft - Installation Script
# Automatically checks and installs Python dependencies
# ============================================================

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
MIN_PYTHON_VERSION="3.8"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# ============================================================
# Helper Functions
# ============================================================

print_header() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  🚀 AI Context Craft - Installation Script${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

version_ge() {
    # Check if version $1 >= version $2
    [ "$(printf '%s\n' "$2" "$1" | sort -V | head -n1)" = "$2" ]
}

check_python() {
    echo -e "${BLUE}🐍 Checking Python installation...${NC}"
    
    # Try different Python commands
    for cmd in python3 python; do
        if command -v $cmd &> /dev/null; then
            PYTHON_VERSION=$($cmd --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
            if version_ge "$PYTHON_VERSION" "$MIN_PYTHON_VERSION"; then
                PYTHON_CMD=$cmd
                echo -e "${GREEN}✓ Found Python $PYTHON_VERSION ($cmd)${NC}"
                return 0
            else
                echo -e "${YELLOW}⚠ Found Python $PYTHON_VERSION but need >= $MIN_PYTHON_VERSION${NC}"
            fi
        fi
    done
    
    echo -e "${RED}❌ Python $MIN_PYTHON_VERSION+ not found${NC}"
    return 1
}

install_python_prompt() {
    echo ""
    echo -e "${YELLOW}Python $MIN_PYTHON_VERSION+ is required but not found.${NC}"
    echo ""
    echo "Installation options:"
    echo "  1. Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-venv python3-pip"
    echo "  2. RHEL/CentOS:   sudo yum install python3 python3-pip"
    echo "  3. macOS:         brew install python3"
    echo "  4. Windows:       Download from https://www.python.org/downloads/"
    echo ""
    
    read -p "Would you like to attempt automatic installation? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        install_python_auto
    else
        echo -e "${RED}Please install Python manually and run this script again.${NC}"
        exit 1
    fi
}

install_python_auto() {
    echo -e "${BLUE}Attempting automatic Python installation...${NC}"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt &> /dev/null; then
            echo "Detected Debian/Ubuntu system"
            sudo apt update
            sudo apt install -y python3 python3-venv python3-pip
        elif command -v yum &> /dev/null; then
            echo "Detected RHEL/CentOS system"
            sudo yum install -y python3 python3-pip
        else
            echo -e "${RED}Unknown Linux distribution. Please install Python manually.${NC}"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            echo "Detected macOS with Homebrew"
            brew install python3
        else
            echo -e "${RED}Homebrew not found. Please install Python manually.${NC}"
            echo "Visit: https://www.python.org/downloads/"
            exit 1
        fi
    else
        echo -e "${RED}Unsupported OS. Please install Python manually.${NC}"
        exit 1
    fi
    
    # Recheck after installation
    if check_python; then
        echo -e "${GREEN}✓ Python installed successfully!${NC}"
    else
        echo -e "${RED}Installation failed. Please install Python manually.${NC}"
        exit 1
    fi
}

check_venv() {
    echo -e "${BLUE}🔧 Checking virtual environment...${NC}"
    
    # Check if venv module is available
    if ! $PYTHON_CMD -m venv --help &> /dev/null; then
        echo -e "${YELLOW}⚠ Python venv module not found${NC}"
        
        read -p "Install python3-venv? (Y/n): " -n 1 -r
        echo
        
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            if command -v apt &> /dev/null; then
                sudo apt install -y python3-venv
            elif command -v yum &> /dev/null; then
                sudo yum install -y python3-venv
            else
                echo -e "${YELLOW}Please install python3-venv manually${NC}"
                return 1
            fi
        else
            echo -e "${YELLOW}Proceeding without virtual environment (not recommended)${NC}"
            return 1
        fi
    fi
    
    # Check if venv exists
    if [ -d "venv" ]; then
        echo -e "${GREEN}✓ Virtual environment exists${NC}"
        
        # Check if it's working
        if [ -f "venv/bin/activate" ] || [ -f "venv/Scripts/activate" ]; then
            echo -e "${GREEN}✓ Virtual environment is valid${NC}"
            return 0
        else
            echo -e "${YELLOW}⚠ Virtual environment seems corrupted${NC}"
            read -p "Recreate virtual environment? (Y/n): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Nn]$ ]]; then
                rm -rf venv
                create_venv
            fi
        fi
    else
        echo -e "${YELLOW}Virtual environment not found${NC}"
        read -p "Create virtual environment? (Y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            create_venv
        else
            echo -e "${YELLOW}Proceeding without virtual environment (not recommended)${NC}"
            USE_GLOBAL=true
        fi
    fi
}

create_venv() {
    echo -e "${BLUE}Creating virtual environment...${NC}"
    $PYTHON_CMD -m venv venv
    
    if [ -f "venv/bin/activate" ] || [ -f "venv/Scripts/activate" ]; then
        echo -e "${GREEN}✓ Virtual environment created successfully${NC}"
    else
        echo -e "${RED}Failed to create virtual environment${NC}"
        exit 1
    fi
}

install_dependencies() {
    echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
    
    # Ensure we use the correct pip
    if [ -f "venv/bin/pip" ]; then
        PIP_CMD="venv/bin/pip"
        PYTHON_FOR_DEPS="venv/bin/python"
    elif [ -f "venv/Scripts/pip.exe" ]; then
        PIP_CMD="venv/Scripts/pip.exe"
        PYTHON_FOR_DEPS="venv/Scripts/python.exe"
    else
        PIP_CMD="$PYTHON_CMD -m pip"
        PYTHON_FOR_DEPS="$PYTHON_CMD"
    fi
    
    # Upgrade pip first
    echo "Upgrading pip..."
    $PIP_CMD install --upgrade pip
    
    # Install main dependencies
    if [ -f "requirements.txt" ]; then
        echo "Installing requirements.txt..."
        $PIP_CMD install -r requirements.txt
        echo -e "${GREEN}✓ Main dependencies installed${NC}"
    else
        echo -e "${YELLOW}⚠ requirements.txt not found${NC}"
    fi
    
    # Install test dependencies
    if [ -f "requirements-test.txt" ]; then
        read -p "Install test dependencies? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Installing requirements-test.txt..."
            $PIP_CMD install -r requirements-test.txt
            echo -e "${GREEN}✓ Test dependencies installed${NC}"
        fi
    fi
    
    # Install tree-sitter grammars
    echo -e "${BLUE}Installing tree-sitter grammars...${NC}"
    $PYTHON_FOR_DEPS << 'EOF'
try:
    from tree_sitter_languages import get_language, get_parser
    languages = ['python', 'javascript', 'typescript', 'bash', 'go', 'rust', 'java', 'c', 'cpp', 'html', 'css']
    installed = []
    failed = []
    
    for lang in languages:
        try:
            get_parser(lang)
            installed.append(lang)
        except:
            failed.append(lang)
    
    if installed:
        print(f"✓ Installed grammars: {', '.join(installed)}")
    if failed:
        print(f"⚠ Failed grammars: {', '.join(failed)}")
except ImportError:
    print("⚠ tree-sitter-languages not installed")
EOF
}

check_docker() {
    echo -e "${BLUE}🐳 Checking Docker (optional)...${NC}"
    
    if command -v docker &> /dev/null; then
        if docker ps &> /dev/null; then
            echo -e "${GREEN}✓ Docker is installed and running${NC}"
            DOCKER_AVAILABLE=true
        else
            echo -e "${YELLOW}⚠ Docker installed but not running${NC}"
            echo "  Start Docker Desktop or run: sudo systemctl start docker"
            DOCKER_AVAILABLE=false
        fi
    else
        echo -e "${YELLOW}⚠ Docker not installed (optional)${NC}"
        echo "  Install from: https://docs.docker.com/get-docker/"
        DOCKER_AVAILABLE=false
    fi
}

setup_scripts() {
    echo -e "${BLUE}🔧 Setting up scripts...${NC}"
    
    # Make scripts executable
    chmod +x main.py 2>/dev/null || true
    chmod +x run-tests.sh 2>/dev/null || true
    chmod +x docker-run.sh 2>/dev/null || true
    
    echo -e "${GREEN}✓ Scripts are executable${NC}"
}

test_installation() {
    echo -e "${BLUE}🧪 Testing installation...${NC}"
    
    # Use venv Python if available
    if [ -f "venv/bin/python" ]; then
        TEST_PYTHON="venv/bin/python"
    elif [ -f "venv/Scripts/python.exe" ]; then
        TEST_PYTHON="venv/Scripts/python.exe"
    else
        TEST_PYTHON="$PYTHON_CMD"
    fi
    
    # Test basic import
    $TEST_PYTHON -c "from utils.app import AIContextCraft; print('✓ Basic import works')" || {
        echo -e "${RED}❌ Import test failed${NC}"
        return 1
    }
    
    # Test help command
    $TEST_PYTHON main.py --help > /dev/null 2>&1 && {
        echo -e "${GREEN}✓ Help command works${NC}"
    } || {
        echo -e "${RED}❌ Help command failed${NC}"
        return 1
    }
    
    # Create test directory
    TEST_DIR="test_install_$$"
    mkdir -p "$TEST_DIR"
    echo "# Test file" > "$TEST_DIR/test.py"
    
    # Test basic concatenation
    $TEST_PYTHON main.py "$TEST_DIR" --no-timestamp > /dev/null 2>&1 && {
        echo -e "${GREEN}✓ Basic concatenation works${NC}"
        rm -rf "$TEST_DIR"
        rm -rf build/project_files_concatenated.txt
    } || {
        echo -e "${RED}❌ Concatenation test failed${NC}"
        rm -rf "$TEST_DIR"
        return 1
    }
    
    return 0
}

print_summary() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ Installation Complete!${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    # Create wrapper script if it doesn't exist
    if [ ! -f "aicc" ]; then
        echo -e "${BLUE}Creating smart wrapper script...${NC}"
        cat > aicc << 'WRAPPER'
#!/bin/bash
# AI Context Craft - Smart Wrapper
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
if [ -d "venv" ]; then
    VENV_DIR="venv"
elif [ -d ".venv" ]; then
    VENV_DIR=".venv"
else
    exec python3 main.py "$@"
fi
if [ -f "$VENV_DIR/bin/python" ]; then
    PYTHON="$VENV_DIR/bin/python"
elif [ -f "$VENV_DIR/Scripts/python.exe" ]; then
    PYTHON="$VENV_DIR/Scripts/python.exe"
else
    echo "❌ Virtual environment seems corrupted. Run: ./install.sh"
    exit 1
fi
exec "$PYTHON" main.py "$@"
WRAPPER
        chmod +x aicc
        echo -e "${GREEN}✓ Created './aicc' wrapper script${NC}"
    fi
    
    echo "You can now use AI Context Craft:"
    echo ""
    
    echo "  # EASY WAY (auto-activates venv):"
    echo "  ./aicc ."
    echo "  ./aicc . --with-tree --strip-comments"
    echo ""
    
    echo "  # Manual way (if you prefer):"
    echo "  source venv/bin/activate"
    echo "  python main.py ."
    echo ""
    
    if [ "$DOCKER_AVAILABLE" = true ]; then
        echo "  # Or use Docker:"
        echo "  ./docker-run.sh"
        echo ""
    fi
    
    echo "For more options: ./aicc --help"
    echo ""
}

# ============================================================
# Main Installation Flow
# ============================================================

main() {
    print_header
    
    # Check Python
    if ! check_python; then
        install_python_prompt
    fi
    
    # Setup virtual environment
    check_venv
    
    # Install dependencies (no need to activate, we use direct paths)
    install_dependencies
    
    # Check Docker (optional)
    check_docker
    
    # Setup scripts
    setup_scripts
    
    # Test installation
    if test_installation; then
        print_summary
    else
        echo -e "${RED}Installation completed with errors. Please check the output above.${NC}"
        exit 1
    fi
}

# Run main installation
main "$@"
