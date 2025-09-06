# 🐳 Docker Guide - AI Context Craft

Complete Docker documentation for AI Context Craft - from installation to advanced usage.

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/LaChouetteInformatique/AIContextCraft.git
cd AIContextCraft

# 2. Make script executable
chmod +x docker-run.sh

# 3. Run with Docker
./docker-run.sh

# That's it! 🎉
```

## 📦 What's Included

- **Dockerfile**: Multi-stage build for optimized image (~180MB)
- **docker-compose.yml**: Complete orchestration with multiple services
- **docker-run.sh**: Convenient wrapper script for all operations
- **.dockerignore**: Optimizes build context

## 🎯 Usage Methods

### Method 1: Using the Wrapper Script (Recommended)

The `docker-run.sh` script provides the easiest way to use AI Context Craft:

```bash
# Setup (first time only)
./docker-run.sh setup

# Process current directory
./docker-run.sh

# Process specific directory
./docker-run.sh run /path/to/project

# With options
./docker-run.sh run . --strip-comments --to-clipboard

# Git integration
./docker-run.sh run . --git-only --with-tree

# Open shell in container
./docker-run.sh shell

# Clean up Docker resources
./docker-run.sh clean
```

### Method 2: Using Docker Directly

For more control or integration into other workflows:

```bash
# Build the image
docker build -t aicontextcraft .

# Run with current directory
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/build:/app/output \
  aicontextcraft .

# Run with options
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/build:/app/output \
  aicontextcraft . --strip-comments --git-only

# With custom config
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/build:/app/output \
  -v $(pwd)/my-config.yaml:/app/config.yaml:ro \
  aicontextcraft . --config /app/config.yaml
```

### Method 3: Using Docker Compose

For complex setups or development:

```bash
# Run default service
docker-compose up

# Run with arguments
docker-compose run --rm aicontextcraft . --strip-comments

# Run development mode (with hot reload)
docker-compose --profile dev up

# Run tests
docker-compose --profile test up
```

## 📁 Volume Mapping

The Docker setup uses these volume mappings:

| Host Path | Container Path | Purpose | Mode |
|-----------|---------------|---------|------|
| `.` (current dir) | `/app/input` | Source files to process | Read-only |
| `./build` | `/app/output` | Generated output files | Read-write |
| `./concat-config.yaml` | `/app/concat-config.yaml` | Configuration | Read-only |
| `~/.gitconfig` | `/home/aicraft/.gitconfig` | Git config | Read-only |
| `/tmp/.X11-unix` | `/tmp/.X11-unix` | X11 for clipboard (Linux) | Read-only |

## ⚙️ Configuration

### Using Custom Configuration

1. **Local config in project** (auto-detected):
```bash
# Create concat-config.yaml in your project
cat > concat-config.yaml << 'EOF'
concat_project_files:
  mode: exclude
  exclude:
    - 'node_modules/**'
    - 'venv/**'
    - '**/*.log'
EOF

# Run - config will be automatically detected
./docker-run.sh
```

2. **Specify config location**:
```bash
./docker-run.sh run . --config /path/to/custom-config.yaml
```

3. **Override via Docker directly**:
```bash
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/build:/app/output \
  -v /path/to/config.yaml:/app/config.yaml:ro \
  aicontextcraft . --config /app/config.yaml
```

### Environment Variables

```bash
# Set Git author for operations
export GIT_AUTHOR_NAME="Your Name"
export GIT_AUTHOR_EMAIL="your@email.com"

# Set display for clipboard (Linux)
export DISPLAY=:0

# Run with environment
docker-compose up
```

## 🎯 Advanced Features

### Git-Aware Filtering

The Docker image includes Git for repository-aware filtering:

```bash
# Process only version-controlled files
./docker-run.sh . --git-only

# Include untracked files (but not ignored)
./docker-run.sh . --git-all

# Why use this?
# - Automatically respects .gitignore
# - Ensures only committed code is shared
# - Perfect for code reviews and AI analysis
```

### Tree Generation Modes

Three tree modes for different levels of detail:

```bash
# Normal - uses concat configuration
./docker-run.sh . --with-tree

# Full - minimal exclusions for complete view  
./docker-run.sh . --with-tree-full

# Custom - uses custom_tree_files config section
./docker-run.sh . --with-tree-custom

# Tree only (no file contents)
./docker-run.sh . --tree-only --tree-mode full
```

### Comment Stripping

AST-based comment removal using tree-sitter:

```bash
# Strip comments to save tokens
./docker-run.sh . --strip-comments

# Combine with other features
./docker-run.sh . --strip-comments --git-only --with-tree
```

### Clipboard Integration

Works on Linux with X11:

```bash
# Copy output directly to clipboard
./docker-run.sh . --to-clipboard

# Requirements:
# - Linux with X11 (or WSL2 with X server)
# - DISPLAY environment variable set
# - xclip installed in container (included)
```

## 🖥️ Platform-Specific Notes

### Linux

Full feature support including clipboard:

```bash
# Clipboard works automatically if DISPLAY is set
./docker-run.sh run . --to-clipboard
```

### macOS

Docker Desktop required. Clipboard support limited:

```bash
# Use file output instead of clipboard
./docker-run.sh run .
# Then: cat build/project_files_*.txt | pbcopy
```

### Windows

Best with Docker Desktop + WSL2:

```bash
# In WSL2 terminal
./docker-run.sh run .

# Or in PowerShell (if Docker Desktop installed)
docker run --rm -v ${PWD}:/app/input:ro aicontextcraft .
```

For clipboard support in WSL2, install an X server like VcXsrv.

## 🛠️ Development Mode

### Interactive Development

```bash
# Mount source code for live development
docker-compose --profile dev up

# Or manually
docker run --rm -it \
  -v $(pwd):/app \
  -w /app \
  --entrypoint /bin/bash \
  aicontextcraft
```

### Running Tests

```bash
# Using docker-compose
docker-compose --profile test up

# Or directly
docker run --rm \
  -v $(pwd):/app:ro \
  -v $(pwd)/tests/test-results:/app/tests/test-results \
  aicontextcraft \
  python -m pytest tests/ -v

# Quick test
./docker-run.sh run . --help
```

### Building Multi-Architecture Images

```bash
# Setup buildx
docker buildx create --use

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t aicontextcraft:latest \
  --push .
```

## 📊 Performance & Resources

### Resource Limits

Modify `docker-compose.yml` to set limits:

```yaml
services:
  aicontextcraft:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          memory: 512M
```

### Performance Metrics

- **Image size**: ~180MB (optimized multi-stage build)
- **Build time**: ~30 seconds (first time, then cached)
- **Startup time**: <1 second
- **Memory usage**: 50-200MB typical
- **Processing speed**: ~1000 files/second

### Optimization Tips

1. **Use .dockerignore**: Already configured to exclude unnecessary files
2. **Mount as read-only**: Input is mounted `:ro` for safety
3. **Use specific paths**: Process only needed directories
4. **Enable BuildKit**: `export DOCKER_BUILDKIT=1`

## 🔧 Troubleshooting

### Docker not installed

```bash
# Linux
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Log out and back in

# macOS/Windows
# Download Docker Desktop from https://www.docker.com/products/docker-desktop
```

### Permission denied

```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER
# Then log out and back in

# Or run with sudo (not recommended)
sudo ./docker-run.sh
```

### Build fails

```bash
# Clean and rebuild
./docker-run.sh clean
docker system prune -a  # Warning: removes all unused images
./docker-run.sh build
```

### Container can't access files

```bash
# Check file permissions
ls -la

# Ensure files are readable
chmod -R 644 your_files
chmod -R 755 your_directories
```

### Out of space

```bash
# Check Docker space usage
docker system df

# Clean up
docker system prune -a --volumes
```

### Clipboard not working

```bash
# Linux: Check X11
echo $DISPLAY  # Should show :0 or similar

# WSL2: Start X server on Windows first
# Then: export DISPLAY=host.docker.internal:0
```

## 🔐 Security Considerations

### Default Security Features

- ✅ Runs as non-root user (`aicraft`, uid 1000)
- ✅ Input mounted read-only (`:ro`)
- ✅ No unnecessary packages or services
- ✅ Official Python slim base image
- ✅ No network access required after build

### Additional Security Options

```bash
# Run with security options
docker run --rm \
  --security-opt=no-new-privileges \
  --cap-drop=ALL \
  --read-only \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/build:/app/output \
  aicontextcraft .
```

## 🔄 Updating

### Update to Latest Version

```bash
# Pull latest changes
git pull

# Rebuild image
./docker-run.sh update

# Or manually
docker-compose build --pull --no-cache
```

### Version Management

```bash
# Tag specific version
docker build -t aicontextcraft:1.0.0 .

# Use specific version
docker run --rm aicontextcraft:1.0.0 --version
```

## 📝 Examples

### Process Python project, strip comments

```bash
./docker-run.sh . --strip-comments --with-tree
```

### Process with custom config

```bash
cat > my-config.yaml << 'EOF'
concat_project_files:
  mode: include
  include: ['**/*.py', '**/*.md']
EOF

./docker-run.sh . --config my-config.yaml
```

### Process only Git-tracked files

```bash
./docker-run.sh . --git-only --with-tree-full
```

### Process remote repository

```bash
# Clone and process
git clone https://github.com/some/repo temp_repo
./docker-run.sh temp_repo --strip-comments
```

### Batch processing

```bash
#!/bin/bash
for dir in */; do
  echo "Processing $dir..."
  ./docker-run.sh "$dir" --git-only
done
```

### Custom output location

```bash
# Create custom output directory
mkdir -p outputs/project1

# Run with custom output
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/outputs/project1:/app/output \
  aicontextcraft .
```

## 🏗️ CI/CD Integration

### GitHub Actions

```yaml
name: Generate Context
on:
  push:
    branches: [main]

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Generate AI context
        run: |
          docker build -t aicontextcraft .
          docker run --rm \
            -v ${{ github.workspace }}:/app/input:ro \
            -v ${{ github.workspace }}/output:/app/output \
            aicontextcraft . --git-only --with-tree
      
      - name: Upload context
        uses: actions/upload-artifact@v3
        with:
          name: ai-context
          path: output/
```

### GitLab CI

```yaml
generate-context:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t aicontextcraft .
    - docker run --rm -v $CI_PROJECT_DIR:/app/input:ro aicontextcraft .
  artifacts:
    paths:
      - build/
    expire_in: 1 week
```

### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('Generate Context') {
            steps {
                sh '''
                    docker build -t aicontextcraft .
                    docker run --rm \
                        -v ${WORKSPACE}:/app/input:ro \
                        -v ${WORKSPACE}/output:/app/output \
                        aicontextcraft . --git-only
                '''
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'output/*', fingerprint: true
        }
    }
}
```

## 💡 Pro Tips

### 1. Create Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias aicraft='docker run --rm -v $(pwd):/app/input:ro -v $(pwd)/build:/app/output aicontextcraft'

# Usage
aicraft . --strip-comments
```

### 2. Use Docker BuildKit

```bash
# Enable BuildKit for faster builds
export DOCKER_BUILDKIT=1
docker build -t aicontextcraft .
```

### 3. Persistent Cache

```bash
# Mount cache directory for tiktoken models
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/build:/app/output \
  -v ~/.cache:/home/aicraft/.cache \
  aicontextcraft .
```

### 4. Debug Mode

```bash
# Run with debug output
./docker-run.sh . --debug

# Or inspect the container
docker run --rm -it --entrypoint /bin/bash aicontextcraft
```

### 5. Custom Entry Point

```bash
# Run with custom command
docker run --rm \
  -v $(pwd):/app/input:ro \
  --entrypoint python \
  aicontextcraft -c "from utils.app import AIContextCraft; print('Ready!')"
```

## 🆘 Support

- **Documentation**: This file and README.md
- **Issues**: GitHub Issues
- **Logs**: Check `build/*.log` for detailed output
- **Debug**: Use `--debug` flag for verbose output
- **Shell**: Use `./docker-run.sh shell` for investigation

---

**Note**: Docker ensures consistent behavior across all platforms. Once the image is built, it will work identically everywhere - that's the Docker promise! 🐳