## ------------------------------- Builder Stage ------------------------------ ## 
FROM python:3.13-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the latest installer, install it and then remove it
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

# Set up the UV environment path correctly
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY ./pyproject.toml .

RUN uv sync

## ------------------------------- Production Stage ------------------------------ ##
FROM python:3.13-slim-bookworm AS production

RUN useradd --create-home appuser
USER appuser

WORKDIR /app

COPY /src src
COPY --from=builder /app/.venv .venv
COPY ./alembic.ini /app/

# Set up environment variables for production
ENV PATH="/app/.venv/bin:$PATH"

# Expose the specified port for FastAPI
EXPOSE $PORT

# Start the application with Uvicorn in production mode, using environment variable references
CMD ["uvicorn", "src.web.main:app", "--log-level", "info", "--host", "0.0.0.0" , "--port", "8000"]




