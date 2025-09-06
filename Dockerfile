# Multi-stage build for optimized image size
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    xclip \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create non-root user
RUN useradd -m -u 1000 aicraft && \
    mkdir -p /app /app/build /app/output && \
    chown -R aicraft:aicraft /app

WORKDIR /app

# Copy application code
COPY --chown=aicraft:aicraft . .

# Create mount points for input/output
VOLUME ["/app/input", "/app/output"]

# Switch to non-root user
USER aicraft

# FIX: Use absolute path for main.py
ENTRYPOINT ["python", "/app/main.py"]
CMD ["--help"]