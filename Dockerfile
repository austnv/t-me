FROM ghcr.io/astral-sh/uv:python3.14-bookworm

WORKDIR /app

COPY pyproject.toml .
COPY . app/

EXPOSE 1234

CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "1234"]
