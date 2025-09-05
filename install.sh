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

# Installing tree-sitter grammars
echo "🌳 Installing grammars for code analysis..."
python -c "from tree_sitter_languages import get_parser; get_parser('python')"
# You can add other languages here if needed, e.g., get_parser('javascript')

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