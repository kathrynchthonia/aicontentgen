# Use the official Python image as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"
    PYTHONPATH=/app

# Set the working directory in the container
WORKDIR /app/

# Install system dependencies required for bcrypt
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Copy the pyproject.toml and uv.lock files
COPY ./pyproject.toml ./uv.lock /app/

# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-cache

# Copy the application code
COPY ./app /app/app
COPY ./scripts /app/scripts
COPY ./alembic.ini /app/

# Compile Python bytecode
RUN uv sync

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
