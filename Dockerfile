ARG UV_VERSION=0.11.23
FROM ghcr.io/astral-sh/uv:$UV_VERSION AS uv

FROM python:3.12

WORKDIR /app

# Install uv
COPY --from=uv /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . /app

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:5001", "wsgi:app"]
