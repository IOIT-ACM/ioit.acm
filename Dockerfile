FROM python:3.12

WORKDIR /app

# Install uv
ENV UV_VERSION=0.11.23
RUN pip install uv==$UV_VERSION

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . /app

CMD ["uv", "run", "python", "run.py"]