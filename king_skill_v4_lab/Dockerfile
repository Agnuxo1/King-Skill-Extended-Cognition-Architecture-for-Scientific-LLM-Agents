# EXP-01 — reproducible environment (Ubuntu packages + Python 3.12)
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    git \
    curl \
    ca-certificates \
    build-essential \
    pkg-config \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# EXP-03 optional: Lean 4 toolchain (set LEAN_DOCKER=1 at build for full layer)
ARG LEAN_DOCKER=0
RUN if [ "$LEAN_DOCKER" = "1" ]; then \
    curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain stable && \
    . "$HOME/.elan/env" && lean --version; \
    else echo "Lean layer skipped (build with --build-arg LEAN_DOCKER=1)"; fi

ENV PATH="/root/.elan/bin:${PATH}"

CMD ["python", "run_all_tests.py"]
