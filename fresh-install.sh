#!/bin/bash
# Complete fresh installation script

echo "🧹 FRESH INSTALLATION - AI Context Craft"
echo "========================================="
echo ""
echo "This will:"
echo "  1. Remove existing venv"
echo "  2. Create new venv"
echo "  3. Install all dependencies"
echo "  4. Create the aicc wrapper"
echo "  5. Test everything"
echo ""

read -p "Continue? [Y/n]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Step 1: Clean up
echo -e "\n${BLUE}Step 1: Cleaning up...${NC}"
rm -rf venv/ .venv/ __pycache__/ .pytest_cache/
echo "✅ Cleaned"

# Step 2: Create venv
echo -e "\n${BLUE}Step 2: Creating virtual environment...${NC}"
python3 -m venv venv || {
    echo -e "${RED}❌ Failed to create venv${NC}"
    echo "Make sure python3-venv is installed:"
    echo "  sudo apt install python3-venv  # Ubuntu/Debian"
    exit 1
}
echo "✅ Virtual environment created"

# Step 3: Install dependencies
echo -e "\n${BLUE}Step 3: Installing dependencies...${NC}"
venv/bin/pip install --upgrade pip
venv/bin/pip install pyyaml pathspec anytree

# Install from requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    venv/bin/pip install -r requirements.txt
fi

echo "✅ Dependencies installed"

# Step 4: Fix main.py (remove any syntax errors)
echo -e "\n${BLUE}Step 4: Fixing main.py...${NC}"
# Fix double colon if it exists
sed -i 's/def check_venv()::/def check_venv():/g' main.py 2>/dev/null || true

# Replace main.py with a simple working version
cat > main.py << 'MAIN_PY'
#!/usr/bin/env python3
"""
AI Context Craft - Main Module
Simplified version that works with the aicc wrapper
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

def check_dependencies():
    """Check if dependencies are installed"""
    missing = []
    try:
        import yaml
    except ImportError:
        missing.append('pyyaml')
    try:
        import pathspec
    except ImportError:
        missing.append('pathspec')
    try:
        import anytree
    except ImportError:
        missing.append('anytree')
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("\nPlease run: ./fresh-install.sh")
        sys.exit(1)

def main():
    """Main entry point"""
    # Check dependencies
    check_dependencies()
    
    # Import the main app
    from utils.app import AIContextCraft
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AI Context Craft - Prepare your code for LLMs",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("source", nargs='?', default=".", help="Source directory")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("--git-only", action="store_true", help="Only Git-tracked files")
    parser.add_argument("--git-all", action="store_true", help="Git tracked + untracked")
    parser.add_argument("--with-tree", action="store_true", help="Include tree structure")
    parser.add_argument("--with-tree-full", action="store_true", help="Full tree")
    parser.add_argument("--with-tree-custom", action="store_true", help="Custom tree")
    parser.add_argument("--tree-only", action="store_true", help="Tree only")
    parser.add_argument("--tree-mode", choices=['normal', 'full', 'custom'], default='normal')
    parser.add_argument("--strip-comments", action="store_true", help="Remove comments")
    parser.add_argument("--to-clipboard", action="store_true", help="Copy to clipboard")
    parser.add_argument("--no-timestamp", action="store_true", help="No timestamp")
    parser.add_argument("--config", help="Config file path")
    parser.add_argument("--mode", choices=['include', 'exclude'])
    parser.add_argument("--debug", action="store_true", help="Debug output")
    parser.add_argument("--version", action="version", version="%(prog)s 2.0.0")
    
    args = parser.parse_args()
    
    # Initialize and run
    craft = AIContextCraft(args.config, args.source)
    
    if args.mode:
        craft.config.set_mode(args.mode)
    
    if args.tree_only:
        craft.generate_tree(output_file=args.output, mode=args.tree_mode)
    else:
        tree_mode = 'none'
        if args.with_tree:
            tree_mode = 'normal'
        elif args.with_tree_full:
            tree_mode = 'full'
        elif args.with_tree_custom:
            tree_mode = 'custom'

        git_mode = None
        if args.git_only:
            git_mode = 'tracked'
        elif args.git_all:
            git_mode = 'all'
        
        craft.concat_files(
            output_file=args.output, 
            tree_mode=tree_mode,
            debug=args.debug,
            strip_comments=args.strip_comments,
            no_timestamp=args.no_timestamp,
            to_clipboard=args.to_clipboard,
            git_mode=git_mode
        )

if __name__ == "__main__":
    main()
MAIN_PY

echo "✅ main.py updated"

# Step 5: Create the aicc wrapper
echo -e "\n${BLUE}Step 5: Creating aicc wrapper...${NC}"
cat > aicc << 'WRAPPER'
#!/bin/bash
# AI Context Craft - Smart Wrapper
# This script always uses the venv Python

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if venv exists
if [ ! -f "venv/bin/python" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: ./fresh-install.sh"
    exit 1
fi

# Run with venv Python
exec venv/bin/python main.py "$@"
WRAPPER

chmod +x aicc
echo "✅ aicc wrapper created"

# Step 6: Test
echo -e "\n${BLUE}Step 6: Testing...${NC}"
echo -n "Testing import... "
venv/bin/python -c "from utils.app import AIContextCraft; print('✅ OK')" || {
    echo "❌ FAILED"
    exit 1
}

echo -n "Testing help... "
./aicc --help > /dev/null 2>&1 && echo "✅ OK" || {
    echo "❌ FAILED"
    exit 1
}

# Step 7: Summary
echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ INSTALLATION COMPLETE!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "You can now use AI Context Craft:"
echo ""
echo "  ./aicc .                    # Process current directory"
echo "  ./aicc . --with-tree        # With tree structure"
echo "  ./aicc . --strip-comments   # Remove comments"
echo "  ./aicc --help               # Show all options"
echo ""
echo "🎯 IMPORTANT: Always use './aicc' instead of 'python main.py'"
echo ""