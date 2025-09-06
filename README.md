# 🤖 AI Context Craft

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://www.python.org/)
[![License: CC0](https://img.shields.io/badge/License-CC0-lightgrey.svg)](LICENSE)
<!-- [![Tests](https://img.shields.io/badge/Tests-Passing-green)](tests/README.md) -->

> 🚀 **Transform your entire codebase into AI-ready context with a single command**

AI Context Craft intelligently concatenates your project files into a single, optimized text file - perfect for feeding into Large Language Models like GPT-4, Claude, or Gemini. No more manual copy-pasting or token limit struggles!

<p align="center">
  <img src="https://img.shields.io/badge/Perfect_for-ChatGPT-74aa9c?logo=openai" />
  <img src="https://img.shields.io/badge/Perfect_for-Claude-cc9b7a?logo=anthropic" />
  <img src="https://img.shields.io/badge/Perfect_for-Gemini-4285F4?logo=google" />
</p>

## ✨ Why AI Context Craft?

When working with AI assistants, you often need to share your entire codebase for context. **AI Context Craft** solves this elegantly:

```bash
# One command to rule them all
./docker-run.sh /path/to/your/project

# 💫 Result: A perfectly formatted file ready for your AI assistant
```

### 🎯 Key Features

- **🐳 Docker-powered** - Zero dependencies, works everywhere
- **🎨 Smart Filtering** - `.gitignore`-style patterns to include/exclude files
- **🌳 Project Tree** - Visual structure for better AI comprehension  
- **💬 Comment Stripping** - Save tokens by removing comments
- **📊 Token Estimation** - Know if it fits in your model's context
- **📋 Clipboard Ready** - Copy directly to clipboard (Linux/X11)
- **🔄 Git-Aware** - Optionally filter by Git tracked files

## 🚀 Quick Start

### Prerequisites

- Docker ([Install Docker](https://docs.docker.com/get-docker/))
- That's it! 🎉

### Installation

```bash
# Clone the repository
git clone https://github.com/LaChouetteInformatique/AIContextCraft.git
cd AIContextCraft

# Make the script executable
chmod +x docker-run.sh

# Setup (first time only)
./docker-run.sh setup
```

### Basic Usage

```bash
# Process current directory
./docker-run.sh

# Process any project
./docker-run.sh /path/to/project

# Include project tree structure
./docker-run.sh . --with-tree

# Strip comments to save tokens
./docker-run.sh . --strip-comments

# Copy directly to clipboard
./docker-run.sh . --to-clipboard
```

## 📖 Real-World Examples

### 🔍 Code Review with AI

```bash
# Get your Python backend ready for review
./docker-run.sh backend/ --strip-comments --with-tree

# Then paste into ChatGPT: "Review this code for security issues"
```

### 🐛 Debug with Full Context

```bash
# Include everything except tests
echo "mode: exclude
exclude: ['**/tests/**', '**/*.test.*']" > concat-config.yaml

./docker-run.sh . --with-tree
# Paste into Claude: "Why is my API returning 500 errors?"
```

### 📚 Documentation Generation

```bash
# Extract all docstrings and comments
./docker-run.sh src/ --with-tree
# Ask Gemini: "Generate API documentation from this code"
```

## ⚙️ Configuration

Create a `concat-config.yaml` file in your project root:

```yaml
concat_project_files:
  mode: include  # or 'exclude'
  include:
    - '**/*.py'     # All Python files
    - '**/*.js'     # All JavaScript files
    - '**/*.md'     # All Markdown files
  exclude:
    - 'node_modules/**'
    - 'venv/**'
    - '**/*.min.js'
```

<details>
<summary>📋 More Configuration Examples</summary>

**Python Project**
```yaml
concat_project_files:
  mode: include
  include:
    - '**/*.py'
    - 'requirements.txt'
    - 'README.md'
  exclude:
    - '__pycache__/**'
    - '.pytest_cache/**'
```

**React/TypeScript Project**
```yaml
concat_project_files:
  mode: include
  include:
    - 'src/**/*.tsx'
    - 'src/**/*.ts'
    - 'package.json'
  exclude:
    - '**/*.test.tsx'
    - 'node_modules/**'
```

**Full Stack Project**
```yaml
concat_project_files:
  mode: exclude
  exclude:
    - 'node_modules/**'
    - 'venv/**'
    - '.git/**'
    - '**/*.log'
    - 'build/**'
    - 'dist/**'
```

</details>

## 🎯 Advanced Features

### Tree Modes

```bash
# Basic tree (same filters as concatenation)
./docker-run.sh . --with-tree

# Full tree (minimal exclusions)
./docker-run.sh . --with-tree-full

# Custom tree (using custom_tree_files config)
./docker-run.sh . --with-tree-custom

# Tree only (no file contents)
./docker-run.sh . --tree-only --tree-mode full
```

### Git Integration

```bash
# Only Git-tracked files
./docker-run.sh . --git-only

# Git-tracked + untracked (exclude ignored)
./docker-run.sh . --git-all
```

### Token Management

```bash
# See token estimation
./docker-run.sh . --stats

# Output shows:
# 🎯 Estimated tokens: 15,234
# ✅ gpt-4-turbo (11.9% of context)
# ✅ claude-3-opus (7.6% of context)
```

## 🧪 Testing

The project includes a comprehensive test suite:

```bash
# Run tests
make test        # Default tests (~2 min)
make test-quick  # Quick smoke tests (~30 sec)
make test-full   # Complete suite (~5 min)
```

📖 **[Full Testing Documentation →](tests/README.md)**

## 🐳 Docker Commands

<details>
<summary>🔧 Advanced Docker Usage</summary>

```bash
# Build image manually
docker build -t aicontextcraft .

# Run without wrapper script
docker run --rm \
  -v $(pwd):/workspace \
  aicontextcraft . --with-tree

# Interactive shell for debugging
./docker-run.sh shell

# Update and rebuild
./docker-run.sh update

# Clean everything
./docker-run.sh clean
```

</details>

## 🤝 Contributing

Contributions are welcome! This project is in the **public domain** (CC0).

### Development Setup

```bash
# Clone and setup
git clone https://github.com/LaChouetteInformatique/AIContextCraft.git
cd AIContextCraft

# Run tests
make test

# Make changes and test
make test-quick

# Open PR!
```

## 📝 Use Cases

- 🤖 **AI Development** - Share complete context with LLMs
- 🔍 **Code Reviews** - Get AI to review your entire codebase
- 📚 **Documentation** - Generate docs from code
- 🐛 **Debugging** - Give AI full context for troubleshooting
- 🎓 **Learning** - Understand new codebases quickly
- 🔄 **Refactoring** - Plan large-scale changes with AI

## 📜 License

This project is released into the **public domain** under the [CC0 1.0 Universal](LICENSE) dedication.

You can copy, modify, distribute, and perform the work, even for commercial purposes, all without asking permission.
