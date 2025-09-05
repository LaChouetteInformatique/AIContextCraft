![Public Domain Dedication](https://img.shields.io/badge/Public%20Domain-CC0%201.0-blue)

# AI Context Craft 🤖

**AI Context Craft** is a powerful and configurable command-line tool for aggregating source code files into a single text file. It is designed to easily prepare complete project contexts to be fed into large language models (LLMs) like Gemini, GPT, etc.

## ✨ Features

-   **File Concatenation**: Selectively combines your project's files into a single context.
-   **Advanced Filtering**: Uses `.gitignore`-style patterns to finely include or exclude files and folders (thanks to `pathspec`).
-   **Tree Generation**: Automatically includes a tree representation of your project structure to give the LLM more context.
-   **Multiple Tree Modes**:
    -   `--with-tree`: Tree based on the same filters as the concatenation.
    -   `--with-tree-full`: Full project tree (with minimal exclusions).
    -   `--with-tree-custom`: Tree based on a custom configuration.
-   **Comment Stripping**: `--strip-comments` option to clean up code and save tokens (thanks to `tree-sitter`).
-   **Flexible Configuration**: Manage your filters via a `concat-config.yaml` file for easy reuse.
-   **Configuration Validation**: A command to check that your configuration is valid.

## 🚀 Installation

The installation script will set up a Python virtual environment and install all necessary dependencies.

```bash
# Clone the project (if you haven't already)
git clone https://github.com/YOUR_USERNAME/ai-context-craft.git
cd ai-context-craft

# Run the installation script
bash install.sh
```

## 📖 Usage

After installation, make sure to activate the virtual environment before using the tool.

```bash
source venv/bin/activate
```

### Basic Commands

```bash
# Concatenate files in the current directory (output in build/)
./run.sh

# Process another directory
./run.sh ../my-other-project

# Specify an output file
./run.sh -o ./output/project_context.txt
```

### Popular Options

```bash
# Include a project tree in the output
./run.sh --with-tree

# Include a more complete tree
./run.sh --with-tree-full

# Strip all comments from the code
./run.sh --strip-comments

# Combine options
./run.sh --with-tree --strip-comments
```

### Generate Tree Only

```bash
# Generate the tree only using the 'full' configuration
./run.sh --tree-only --tree-mode full -o project-tree.txt
```

### Validate Configuration

Before running a large concatenation, you can validate your `concat-config.yaml` file.

```bash
./validate_config.py
```

## ⚙️ Configuration (`concat-config.yaml`)

Create a `concat-config.yaml` file at the root of your project to precisely control which files are included.

**Example Configuration (exclude mode):**

```yaml
# File: concat-config.yaml

concat_project_files:
  # In 'exclude' mode, everything is included except what is listed below.
  mode: exclude
  exclude:
    # Entire folders
    - 'node_modules/'
    - 'build/'
    - 'dist/'
    - '.venv/'
    - '__pycache__/'
    - '.git/'
    # Files by name or pattern
    - '*.log'
    - '*.lock'
    - '.env'
    - 'data/*'
```

**Example Configuration (include mode):**

```yaml
# File: concat-config.yaml

concat_project_files:
  # In 'include' mode, nothing is included except what is listed below.
  mode: include
  include:
    - 'src/**/*.py'      # All Python files in src
    - 'src/**/*.js'       # All JS files in src
    - 'tests/*.py'        # Test files at the root of tests/
    - 'README.md'         # The main README
    - 'requirements.txt'
```


## 📜 License

This project is dedicated to the **public domain** via the [Creative Commons Zero (CC0) 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) license.

You are free to copy, modify, distribute, and perform the work, even for commercial purposes, all without asking permission.

---