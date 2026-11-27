ARG UV_VERSION=0.11.23
FROM ghcr.io/astral-sh/uv:$UV_VERSION AS uv

# Copy frontend libraries out of node_modules into app/static/vendor/
FROM node:26-slim AS assets

WORKDIR /app

COPY package.json package-lock.json .npmrc ./
RUN npm ci --omit=dev

COPY scripts/vendor.mjs scripts/
RUN npm run vendor

FROM python:3.12

WORKDIR /app

# Install uv
COPY --from=uv /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . /app
COPY --from=assets /app/app/static/vendor /app/app/static/vendor

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:5001", "wsgi:app"]
