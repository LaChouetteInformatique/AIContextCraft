# 🐳 Docker Guide - AI Context Craft

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-context-craft.git
cd ai-context-craft

# 2. Run with Docker
./docker-run.sh

# That's it! 🎉
```

## 📦 What's Included

- **Dockerfile**: Multi-stage build for optimized image (~150MB)
- **docker-compose.yml**: Complete orchestration with multiple services
- **docker-run.sh**: Convenient wrapper script
- **.dockerignore**: Optimizes build context

## 🎯 Usage Methods

### Method 1: Using the Wrapper Script (Recommended)

```bash
# Setup (first time only)
./docker-run.sh setup

# Process current directory
./docker-run.sh

# Process specific directory
./docker-run.sh run /path/to/project

# With options
./docker-run.sh run . --strip-comments --to-clipboard

# Open shell in container
./docker-run.sh shell

# Clean up Docker resources
./docker-run.sh clean
```

### Method 2: Using Docker Directly

```bash
# Build the image
docker build -t aicontextcraft .

# Run with current directory
docker run --rm -v $(pwd):/app/input:ro -v $(pwd)/build:/app/output aicontextcraft .

# Run with options
docker run --rm -v $(pwd):/app/input:ro -v $(pwd)/build:/app/output aicontextcraft . --strip-comments
```

### Method 3: Using Docker Compose

```bash
# Run default service
docker-compose up

# Run with arguments
docker-compose run --rm aicontextcraft . --strip-comments

# Run development mode
docker-compose --profile dev up

# Run tests
docker-compose --profile test up
```

## 📁 Volume Mapping

The Docker setup uses these volume mappings:

| Host Path | Container Path | Purpose |
|-----------|---------------|---------|
| `.` (current dir) | `/app/input` | Source files (read-only) |
| `./build` | `/app/output` | Generated output files |
| `./concat-config.yaml` | `/app/concat-config.yaml` | Configuration (optional) |

## ⚙️ Configuration

### Using Custom Configuration

1. **Local config in project**:
```bash
# Create concat-config.yaml in your project
vim concat-config.yaml

# Run - it will be automatically detected
./docker-run.sh
```

2. **Override config location**:
```bash
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/build:/app/output \
  -v /path/to/config.yaml:/app/config.yaml:ro \
  aicontextcraft .
```

### Environment Variables

```bash
# Set Git author for operations
export GIT_AUTHOR_NAME="Your Name"
export GIT_AUTHOR_EMAIL="your@email.com"

# Run with environment
docker-compose up
```

## 🖥️ Platform-Specific Notes

### Linux

Clipboard support works through X11:
```bash
# Clipboard will work automatically if DISPLAY is set
./docker-run.sh run . --to-clipboard
```

### macOS

- Docker Desktop required
- Clipboard support limited (use file output instead)
- Performance optimized with Docker Desktop's virtualization

### Windows

- Use Docker Desktop with WSL2 backend (recommended)
- Or use Git Bash to run the scripts
- Clipboard support through file output

## 🛠️ Advanced Usage

### Development Mode

```bash
# Mount source code for live development
docker-compose --profile dev up

# Or manually
docker run --rm -it \
  -v $(pwd):/app \
  -w /app \
  aicontextcraft:dev \
  /bin/bash
```

### Running Tests

```bash
# Using docker-compose
docker-compose --profile test up

# Or directly
docker run --rm \
  -v $(pwd):/app:ro \
  aicontextcraft \
  python -m pytest tests/
```

### Building Multi-Architecture Images

```bash
# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t aicontextcraft:latest \
  --push .
```

### Resource Limits

Modify `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 2G
```

## 🔧 Troubleshooting

### Docker not installed

```bash
# Linux
curl -fsSL https://get.docker.com | sh

# macOS/Windows
# Download Docker Desktop from https://www.docker.com/products/docker-desktop
```

### Permission denied

```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER
# Log out and back in
```

### Build fails

```bash
# Clean and rebuild
./docker-run.sh clean
./docker-run.sh build
```

### Container can't access files

```bash
# Check file permissions
ls -la

# Ensure files are readable
chmod -R 644 your_files
```

### Out of space

```bash
# Clean up Docker resources
docker system prune -a
```

## 📊 Performance

- **Image size**: ~150MB (optimized multi-stage build)
- **Build time**: ~30 seconds (first time)
- **Startup time**: <1 second
- **Memory usage**: ~50-200MB depending on project size

## 🔐 Security

- Runs as non-root user (uid 1000)
- Input mounted read-only by default
- No unnecessary packages installed
- Official Python slim base image

## 🔄 Updating

```bash
# Pull latest changes
git pull

# Rebuild image
./docker-run.sh update

# Or manually
docker-compose build --pull
```

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

## 📝 Examples

### Process Python project, strip comments
```bash
./docker-run.sh run . --strip-comments --with-tree
```

### Process with custom config
```bash
echo "mode: exclude
exclude: ['tests/**', 'docs/**']" > concat-config.yaml
./docker-run.sh
```

### Process remote repository
```bash
git clone https://github.com/some/repo temp_repo
cd temp_repo
../ai-context-craft/docker-run.sh
```

### Batch processing
```bash
for dir in project1 project2 project3; do
  cd $dir
  ../ai-context-craft/docker-run.sh
  cd ..
done
```

## 💡 Tips

1. **Alias for convenience**:
```bash
alias aicraft='~/ai-context-craft/docker-run.sh run'
# Usage: aicraft . --strip-comments
```

2. **Global installation**:
```bash
sudo ln -s $(pwd)/docker-run.sh /usr/local/bin/aicraft
# Usage: aicraft . --strip-comments
```

3. **Custom output directory**:
```bash
mkdir my-output
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/my-output:/app/output \
  aicontextcraft .
```

## 🆘 Support

- Check logs: `./docker-run.sh logs`
- Debug mode: `./docker-run.sh run . --debug`
- Interactive shell: `./docker-run.sh shell`
- Clean restart: `./docker-run.sh clean && ./docker-run.sh setup`

---

**Note**: Docker ensures consistent behavior across all platforms. Once the image is built, it will work identically everywhere!