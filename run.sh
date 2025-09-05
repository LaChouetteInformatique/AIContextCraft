#!/bin/bash

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Help function
show_help() {
    echo "AI Context Craft - Prepare your code for LLMs"
    echo "===================================================="
    echo ""
    echo "Usage: ./run.sh [source] [options]"
    echo ""
    echo "Arguments:"
    echo "  source              Source directory (default: .)"
    echo ""
    echo "Main Options:"
    echo "  -h, --help          Show this help"
    echo "  -o, --output FILE   Output file"
    echo "  --with-tree         Include tree with the same config"
    echo "  --with-full-tree    Include full tree (separate config)"
    echo "  --strip-comments    Remove comments"
    echo "  --no-timestamp      No timestamp in the filename"
    echo "  --debug             Detailed debug mode"
    echo "  --tree-only         Generate only the tree"
    echo ""
    echo "Advanced Options:"
    echo "  --mode MODE         Force the mode (include/exclude)"
    echo "  --config FILE       Use a custom config file"
    echo "  --legacy            Force the old filtering system"
    echo ""
    echo "Special Commands:"
    echo "  validate [--config FILE]    Validate the configuration"
    echo ""
    echo "Examples:"
    echo "  ./run.sh                    # Process the current directory"
    echo "  ./run.sh ../project         # Process another project"
    echo "  ./run.sh . --with-tree      # Include the tree"
    echo "  ./run.sh . --strip-comments # Remove comments"
    echo "  ./run.sh validate           # Validate the config"
}

# Check dependencies
check_dependencies() {
    if ! python3 -c "import yaml" 2>/dev/null; then
        echo "📦 Installing PyYAML..."
        pip3 install pyyaml --user
    fi
}

# Handle the validate command
if [[ "$1" == "validate" ]]; then
    shift
    check_dependencies
    python3 validate_config.py "$@"
    exit $?
fi

# Handle help
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]] || [[ "$1" == "help" ]]; then
    show_help
    exit 0
fi

# Check dependencies
check_dependencies

# Launch the main program
python3 main.py "$@"