FROM python:3.13-slim-trixie AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UC_LINK_MODE=copy

RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=/pyproject.toml \
    uv sync --locked --no-install-project --no-dev
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"


FROM builder AS testing

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --group test --no-group dev

ENTRYPOINT ["pytest", "-s", "-x", "--ff", "-vv", "--log-cli-level=DEBUG", "tests"]


FROM builder AS development

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --group dev --no-group test

ENTRYPOINT ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000", "main.py"]


FROM builder AS production

ENTRYPOINT ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "main.py"]
