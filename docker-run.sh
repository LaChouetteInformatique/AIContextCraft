#!/bin/bash

# ============================================================
# AI Context Craft - Docker Wrapper Script
# Simplifies Docker usage with convenient commands
# ============================================================

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

IMAGE_NAME="aicontextcraft"
CONTAINER_NAME="aicraft"
OUTPUT_DIR="./build"

# ============================================================
# Helper Functions
# ============================================================

print_header() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🐳 AI Context Craft - Docker Edition"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

print_help() {
    cat << EOF
Usage: ./docker-run.sh [COMMAND] [OPTIONS]

Commands:
    build           Build the Docker image
    run [args]      Run AI Context Craft (default)
    shell           Open a shell in the container
    clean           Remove containers and images
    logs            Show container logs
    setup           Initial setup (build + test)
    update          Update and rebuild the image
    
Examples:
    ./docker-run.sh                    # Run with default settings
    ./docker-run.sh run . --to-clipboard
    ./docker-run.sh run /path/to/project --strip-comments
    ./docker-run.sh shell               # Interactive shell
    ./docker-run.sh build               # Build/rebuild image
    
Docker Compose Commands:
    docker-compose up                   # Run default service
    docker-compose run --rm aicontextcraft [args]
    docker-compose --profile dev up     # Run development mode
    docker-compose --profile test up    # Run tests
    
EOF
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed${NC}"
        echo "Please install Docker from: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! docker ps &> /dev/null; then
        echo -e "${YELLOW}Warning: Docker daemon is not running${NC}"
        echo "Please start Docker Desktop or the Docker service"
        exit 1
    fi
}

build_image() {
    echo -e "${BLUE}Building Docker image...${NC}"
    docker build -t ${IMAGE_NAME}:latest .
    echo -e "${GREEN}✓ Image built successfully${NC}"
}

check_image() {
    if ! docker image inspect ${IMAGE_NAME}:latest &> /dev/null; then
        echo -e "${YELLOW}Docker image not found. Building...${NC}"
        build_image
    fi
}

run_container() {
    check_image
    
    # Create output directory if it doesn't exist
    mkdir -p "$OUTPUT_DIR"
    
    # Prepare Docker run command
    DOCKER_CMD="docker run --rm"
    
    # Add volume mounts
    DOCKER_CMD="$DOCKER_CMD -v $(pwd):/app/input:ro"
    DOCKER_CMD="$DOCKER_CMD -v $(pwd)/build:/app/output"
    
    # Add config file if it exists
    if [ -f "concat-config.yaml" ]; then
        DOCKER_CMD="$DOCKER_CMD -v $(pwd)/concat-config.yaml:/app/concat-config.yaml:ro"
    elif [ -f "config.yaml" ]; then
        DOCKER_CMD="$DOCKER_CMD -v $(pwd)/config.yaml:/app/config.yaml:ro"
    fi
    
    # Add clipboard support for Linux
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -n "$DISPLAY" ]; then
            DOCKER_CMD="$DOCKER_CMD -e DISPLAY=$DISPLAY"
            DOCKER_CMD="$DOCKER_CMD -v /tmp/.X11-unix:/tmp/.X11-unix:ro"
            DOCKER_CMD="$DOCKER_CMD --network host"
        fi
    fi
    
    # Add Git config if available
    if [ -f "$HOME/.gitconfig" ]; then
        DOCKER_CMD="$DOCKER_CMD -v $HOME/.gitconfig:/home/aicraft/.gitconfig:ro"
    fi
    
    # Set working directory
    DOCKER_CMD="$DOCKER_CMD -w /app/input"
    
    # Add image name
    DOCKER_CMD="$DOCKER_CMD ${IMAGE_NAME}:latest"
    
    # Add user arguments
    if [ $# -eq 0 ]; then
        DOCKER_CMD="$DOCKER_CMD ."
    else
        DOCKER_CMD="$DOCKER_CMD $@"
    fi
    
    # Execute
    echo -e "${BLUE}Running AI Context Craft...${NC}"
    eval $DOCKER_CMD
}

run_shell() {
    check_image
    echo -e "${BLUE}Opening shell in container...${NC}"
    docker run --rm -it \
        -v $(pwd):/app/input \
        -v $(pwd)/build:/app/output \
        -w /app/input \
        --entrypoint /bin/bash \
        ${IMAGE_NAME}:latest
}

clean_docker() {
    echo -e "${YELLOW}Cleaning Docker resources...${NC}"
    
    # Stop and remove containers
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
    
    # Remove image
    docker rmi ${IMAGE_NAME}:latest 2>/dev/null || true
    
    echo -e "${GREEN}✓ Cleanup complete${NC}"
}

show_logs() {
    docker logs ${CONTAINER_NAME} 2>/dev/null || echo "No logs available"
}

setup() {
    echo -e "${BLUE}Setting up AI Context Craft with Docker...${NC}"
    
    # Check Docker
    check_docker
    
    # Build image
    build_image
    
    # Test run
    echo -e "${BLUE}Testing installation...${NC}"
    docker run --rm ${IMAGE_NAME}:latest --help > /dev/null
    
    echo -e "${GREEN}✓ Setup complete!${NC}"
    echo ""
    echo "You can now use:"
    echo "  ./docker-run.sh              # Process current directory"
    echo "  ./docker-run.sh run . --help # Show options"
    echo ""
}

update() {
    echo -e "${BLUE}Updating AI Context Craft...${NC}"
    
    # Pull latest code if in git repo
    if [ -d .git ]; then
        echo "Pulling latest changes..."
        git pull
    fi
    
    # Rebuild image
    build_image
    
    echo -e "${GREEN}✓ Update complete!${NC}"
}

# ============================================================
# Main Execution
# ============================================================

print_header

# Check Docker availability
check_docker

# Parse command
COMMAND=${1:-run}
shift || true

case "$COMMAND" in
    build)
        build_image
        ;;
    run)
        run_container "$@"
        ;;
    shell)
        run_shell
        ;;
    clean)
        clean_docker
        ;;
    logs)
        show_logs
        ;;
    setup)
        setup
        ;;
    update)
        update
        ;;
    help|--help|-h)
        print_help
        ;;
    *)
        # Default: treat as arguments to run
        run_container "$COMMAND" "$@"
        ;;
esac