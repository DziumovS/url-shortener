# URL Shortener

A minimal URL shortener service built with **FastAPI**. It stores mappings in **PostgreSQL** and uses **Redis** for caching to speed up redirects.

## Features

- **Create short links** — Submit a long URL and receive a short slug (e.g. `aB3xYz`).
- **Redirect by slug** — Visiting `/g/{slug}` redirects to the original URL (302).
- **Caching** — Recent lookups are served from Redis to reduce database load.
- **Validation** — URLs are validated before storage (length and format).

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- PostgreSQL 17
- Redis 7

## Quick Start

### 1. Environment

Copy the example env file and adjust if needed:

```bash
cp .env_public .env
```

Required variables:

| Variable | Description |
|----------|-------------|
| `POSTGRES_DB` | PostgreSQL database name |
| `POSTGRES_USER` | PostgreSQL user |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `POSTGRES_HOST` | Host (use `database` when using Docker Compose) |
| `POSTGRES_EXTERNAL_PORT` | Port exposed on host |
| `POSTGRES_INTERNAL_PORT` | Port inside container (usually `5432`) |
| `REDIS_DB` | Redis DB number (e.g. `0`) |
| `REDIS_HOST` | Redis host (use `redis` when using Docker Compose) |
| `REDIS_EXTERNAL_PORT` | Redis port on host |
| `REDIS_INTERNAL_PORT` | Redis port in container (usually `6379`) |
| `REDIS_TTL_SECONDS` | Cache TTL in seconds (e.g. `3600`) |

### 2. Run with Docker Compose

```bash
docker compose up --build
```

The API is available at **http://localhost:8000**. The app creates database tables on startup.

### 3. Run locally (with Postgres and Redis already running)

```bash
uv sync
uv run uvicorn src.main:app --reload --port 8000
```

Ensure `.env` points to your local Postgres and Redis (e.g. `POSTGRES_HOST=localhost`, `REDIS_HOST=localhost` and the correct ports).

## API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Serves the web UI (index page). |
| `POST` | `/c` | Create a short link. |
| `GET` | `/g/{slug}` | Redirect to the original URL for the given slug. |

### Create a short link

**Request**

```http
POST /c
Content-Type: application/json

{"original_url": "https://example.com/very/long/url"}
```

**Response**

```json
{"data": "aB3xYz"}
```

The response contains only the **slug**. The full short URL is: `http://<your-host>/g/aB3xYz`.

### Redirect

**Request**

```http
GET /g/aB3xYz
```

**Response**

- **302** — Redirect to the original URL.
- **404** — Slug not found.

## Project structure

```
src/
├── api/
│   ├── deps.py           # FastAPI dependencies (DB session)
│   └── routes/
│       └── short_url.py  # /c and /g/{slug} endpoints
├── db/
│   ├── database.py      # Async SQLAlchemy engine
│   ├── models.py        # ORM models
│   ├── crud.py          # DB operations
│   ├── redis_client.py  # Redis connection
│   └── redis_cache.py   # Cache get/set for slugs
├── services/
│   └── short_url_service.py  # Create slug & resolve URL
├── schemas/
│   └── url.py           # Pydantic request/response
├── validators/
│   └── url_validator.py # URL validation
├── utils/
│   └── shortener.py     # Random slug generation
├── decorators/
│   └── decorators.py    # Retry on slug collision
├── exceptions/
│   └── exceptions.py    # Custom errors
├── config.py            # Settings from .env
└── main.py              # FastAPI app & lifespan
```

## Development

- **Tests:** `uv run pytest`
- **Linting/formatting:** Use your preferred tools (e.g. Ruff, Black) on the `src/` and `tests/` directories.

## License

See repository license if applicable.
