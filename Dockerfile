FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY skillsbary ./skillsbary

RUN uv sync --frozen --no-dev

ENV SKILLSBARY_TRANSPORT=streamable-http \
    SKILLSBARY_HOST=0.0.0.0 \
    SKILLSBARY_PORT=8765 \
    SKILLSBARY_DB=/data/skills.db

EXPOSE 8765

CMD ["uv", "run", "skillsbary"]
