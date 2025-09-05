#!/bin/bash

echo "🚀 Installing AI Context Craft"
echo "=============================="

# Checking for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it first."
    exit 1
fi

echo "✅ Python 3 detected: $(python3 --version)"

# Creating virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Error creating the virtual environment."
        exit 1
    fi
else
    echo "✅ Virtual environment already exists."
fi

# Activating virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Updating pip and installing dependencies from requirements.txt
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Error installing Python dependencies."
    deactivate
    exit 1
fi

# Installing tree-sitter grammars dynamically
echo "🌳 Installing grammars for code analysis..."

# Extract supported languages from comment_stripper.py
python3 << 'EOF'
import sys
import re
from pathlib import Path

# Read the comment_stripper.py file
stripper_path = Path("utils/comment_stripper.py")
if not stripper_path.exists():
    print("Warning: comment_stripper.py not found")
    sys.exit(0)

content = stripper_path.read_text()

# Extract language mappings using regex
pattern = r"'\.[\w]+': '([\w]+)'"
languages = set(re.findall(pattern, content))

# Remove duplicates and try to install each grammar
installed = []
failed = []

for lang in sorted(languages):
    try:
        from tree_sitter_languages import get_parser
        get_parser(lang)
        installed.append(lang)
        print(f"  ✅ {lang}")
    except Exception as e:
        failed.append(lang)
        print(f"  ⚠️  {lang} (not available or already installed)")

if installed:
    print(f"\n✨ Successfully prepared {len(installed)} language grammars")
if failed:
    print(f"📝 Note: {len(failed)} grammars were not available (this is normal)")
EOF

# Creating build directory if it doesn't exist
if [ ! -d "build" ]; then
    echo "📁 Creating build directory..."
    mkdir build
fi

# Making scripts executable
chmod +x run.sh
chmod +x validate_config.py

echo ""
echo "✨ Installation completed successfully!"
echo ""
echo "📖 Usage (make sure to activate the virtual environment with 'source venv/bin/activate'):"
echo "  ./run.sh              # Process the current directory"
echo "  ./run.sh --help       # Display help"
echo "  ./validate_config.py  # Validate the configuration"
echo ""
echo "💡 Tip: Activate your environment with 'source venv/bin/activate' before running the commands."

# Deactivating the environment so as not to leave the user's terminal activated
deactivate