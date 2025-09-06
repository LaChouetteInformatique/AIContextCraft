# 🤖 AI Context Craft

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://www.python.org/)
[![License: CC0](https://img.shields.io/badge/License-CC0-lightgrey.svg)](LICENSE)

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
- **🌳 Advanced Tree Generation** - Visual structure with multiple modes for better AI comprehension  
- **💬 Comment Stripping** - Save tokens by removing comments with AST parsing
- **📊 Token Estimation** - Know exactly if it fits in your model's context (tiktoken)
- **📋 Clipboard Ready** - Copy directly to clipboard (Linux/X11)
- **🔄 Git-Aware** - Filter by Git tracked/untracked files automatically

## 🚀 Quick Start

### Prerequisites

- Docker ([Install Docker](https://docs.docker.com/get-docker/))
- That's it! 🎉

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/LaChouetteInformatique/AIContextCraft.git
cd AIContextCraft

# 2. Make the script executable
chmod +x docker-run.sh

# 3. Setup (first time only)
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

### 🔀 Git-Filtered Code Review

```bash
# Only review committed code (exclude WIP files)
./docker-run.sh . --git-only --with-tree --strip-comments

# Include untracked files for full context
./docker-run.sh . --git-all --with-tree
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

> **💡 Tip**: If using Git, consider `--git-only` instead of manual exclusions!

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

**Multiple Tree Configurations**
```yaml
# Different configurations for different purposes
concat_project_files:
  mode: include
  include: ['**/*.py', '**/*.js']

tree_project_files:  # For --with-tree-full
  mode: exclude
  exclude: ['node_modules/**', '.git/**']

custom_tree_files:  # For --with-tree-custom
  mode: include
  include: ['src/**', 'docs/**']
```

</details>

## 🎯 Advanced Features

### Git Integration

Perfect for sharing only versioned code, excluding test/temporary files automatically:

```bash
# Only include Git-tracked files (exclude untracked/ignored)
./docker-run.sh . --git-only

# Include Git-tracked + untracked files (exclude only ignored)
./docker-run.sh . --git-all

# Combine with other options
./docker-run.sh . --git-only --strip-comments --with-tree
```

### Tree Modes

Different levels of detail for project structure:

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

### Token Management

Know exactly how much context you're using:

```bash
# Output shows:
# 🎯 Estimated tokens: 15,234 (using tiktoken/cl100k_base)
# ✅ gpt-4-turbo (11.9% of context)
# ✅ claude-3-opus (7.6% of context)
# ⚠️  gemini-pro (46.5% of context)
```

## 🔧 Technical Details

### Architecture

AI Context Craft uses a modular architecture:

```
main.py                      # Entry point with argparse
├── utils/
│   ├── app.py              # Main application logic
│   ├── config_manager.py   # YAML configuration handling
│   ├── file_processor.py   # File filtering and processing
│   ├── tree_generator.py   # Tree generation with anytree
│   ├── pattern_matcher.py  # Gitignore-style patterns (pathspec)
│   ├── git_manager.py      # Git integration
│   ├── comment_stripper.py # AST-based comment removal
│   ├── token_estimator.py  # Token counting (tiktoken)
│   └── clipboard_manager.py # Clipboard operations
```

### Pattern Matching

Uses `pathspec` library for gitignore-compatible patterns:
- `**/*.py` - All Python files recursively
- `src/**` - Everything under src/
- `!*.test.js` - Exclude test files (with `!`)
- Complex patterns like `./**/[!.]*.{js,jsx}`

### Token Estimation

Employs `tiktoken` for accurate OpenAI token counts:
- GPT-4/3.5: Uses `cl100k_base` encoding
- Fallback: Character/word-based heuristic estimation
- Shows model compatibility with context usage percentage

### Comment Stripping

Uses `tree-sitter` for language-aware AST parsing:
- Preserves code structure
- Removes comments while keeping line numbers
- Supports Python, JavaScript, TypeScript, Go, Rust, and more

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
  -v $(pwd):/app/input:ro \
  -v $(pwd)/build:/app/output \
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

# Install dependencies (for local development)
pip install -r requirements.txt
pip install -r requirements-test.txt

# Run tests
make test

# Make changes and test
make test-quick

# Open PR!
```

### Dependencies

The project uses several Python libraries:
- `pyyaml` - YAML configuration parsing
- `pathspec` - Gitignore-style pattern matching  
- `anytree` - Tree structure generation
- `tiktoken` - OpenAI token counting
- `tree-sitter` - AST-based comment removal

## 📝 Use Cases

- 🤖 **AI Development** - Share complete context with LLMs
- 🔍 **Code Reviews** - Get AI to review your entire codebase
- 📚 **Documentation** - Generate docs from code
- 🐛 **Debugging** - Give AI full context for troubleshooting
- 🎓 **Learning** - Understand new codebases quickly
- 🔄 **Refactoring** - Plan large-scale changes with AI

## 📊 Performance

- **Image size**: ~180MB (includes Git and Python libraries)
- **Build time**: ~30 seconds (first time)
- **Startup time**: <1 second
- **Memory usage**: ~50-200MB depending on project size
- **Processing speed**: ~1000 files/second

## 🔐 Security

- Runs as non-root user (uid 1000)
- Input mounted read-only by default
- No unnecessary packages installed
- Official Python slim base image
- No network access required (except for building)

## 🏗️ CI/CD Integration

### GitHub Actions

```yaml
name: Build and Test
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and test
        run: |
          docker build -t aicontextcraft .
          docker run --rm aicontextcraft --help
```

### GitLab CI

```yaml
test:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t aicontextcraft .
    - docker run --rm aicontextcraft --help
```

## 💡 Tips & Tricks

### Aliases for Convenience

```bash
# Add to ~/.bashrc or ~/.zshrc
alias aicraft='~/AIContextCraft/docker-run.sh run'

# Usage
aicraft . --strip-comments
aicraft ~/project --git-only
```

### Global Installation

```bash
sudo ln -s $(pwd)/docker-run.sh /usr/local/bin/aicraft
# Now use from anywhere:
aicraft . --with-tree
```

### Custom Output Directory

```bash
mkdir my-output
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/my-output:/app/output \
  aicontextcraft .
```

### Batch Processing

```bash
# Process multiple projects
for dir in project1 project2 project3; do
  echo "Processing $dir..."
  ./docker-run.sh $dir --git-only --with-tree
done
```

## 🆘 Support

- **Check logs**: `cat build/*.log`
- **Debug mode**: `./docker-run.sh run . --debug`
- **Interactive shell**: `./docker-run.sh shell`
- **Clean restart**: `./docker-run.sh clean && ./docker-run.sh setup`

## 📜 License

This project is released into the **public domain** under the [CC0 1.0 Universal](LICENSE) dedication.

You can copy, modify, distribute, and perform the work, even for commercial purposes, all without asking permission.
