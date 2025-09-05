#!/bin/bash

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check dependencies
check_dependencies() {
    if ! python3 -c "import yaml" 2>/dev/null; then
        echo "📦 Installing PyYAML..."
        pip3 install pyyaml --user
    fi
    
    if ! python3 -c "import pathspec" 2>/dev/null; then
        echo "📦 Installing pathspec..."
        pip3 install pathspec --user
    fi
}

# Special handling for validate command
if [[ "$1" == "validate" ]]; then
    shift
    check_dependencies
    python3 validate_config.py "$@"
    exit $?
fi

# Delegate help to Python argparse
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]] || [[ "$1" == "help" ]]; then
    # Add a nice header before Python help
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🤖 AI Context Craft - Prepare your code for LLMs"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    python3 main.py --help
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Special Commands:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ./run.sh validate           Validate configuration"
    echo "  ./run.sh validate --config FILE  Use custom config"
    echo ""
    echo "  Quick Examples:"
    echo "  ./run.sh                    Process current directory"
    echo "  ./run.sh ../project         Process another project"
    echo "  ./run.sh . --to-clipboard   Copy to clipboard"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    exit 0
fi

# Check dependencies before running
check_dependencies

# Launch the main program with all arguments
python3 main.py "$@"