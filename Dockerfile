# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as base

# Install required system dependencies for Tkinter
RUN apt-get update && apt-get install -y \
    xvfb \
    python3-tk \
    tcl8.6 \
    tk8.6 \
    fontconfig \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create directory for fontconfig cache and adjust permissions
RUN mkdir -p /usr/local/var/cache/fontconfig && \
    chmod 777 /usr/local/var/cache/fontconfig

# Set environment variables to prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Create a non-privileged user that the app will run under
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download Python dependencies and leverage caching
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application
USER appuser

# Copy the source code into the container
COPY . .

# Set the display environment variable to point to the virtual display created by Xvfb
ENV DISPLAY=:99

# Expose the port that the application listens on
EXPOSE 8000

# Run the application with Xvfb
CMD ["Xvfb", ":99", "-screen", "0", "1024x768x24", "-ac", "+extension", "GLX", "+render", "-noreset", "&", "python", "-m", "snake_game.SnakeGame"]