# Grafana Integration API (FastAPI)

Modern, modular FastAPI backend that securely integrates with Grafana's REST API (Dashboards, Data Sources, Alerts, Users).

## Features

- Modular structure: routers, services, models, core (auth, config, logging, errors)
- Secure FastAPI endpoints with Bearer token authentication
- Configurable Grafana base URL and API key for outgoing requests
- Robust logging and exception handling
- Auto-generated OpenAPI docs with examples
- Sample pytest tests

## Requirements

- Python 3.11+
- Grafana instance accessible from the service
- Environment variables configured (see `.env.example`)

## Quickstart

1. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -e .
pip install -r <(python - <<'PY'\nimport tomllib,sys\nprint('\\n'.join(tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']))\nPY\n)
```

Alternatively:

```bash
pip install fastapi uvicorn[standard] httpx pydantic pydantic-settings pytest pytest-asyncio anyio
```

3. Copy environment

```bash
cp .env.example .env
```

Edit `.env` and set:

- API_BEARER_TOKEN to a secure value
- GRAFANA_URL to your Grafana base URL (e.g., http://localhost:3000)
- GRAFANA_API_KEY to a Grafana API key with required permissions

4. Run

```bash
python run.py
```

Visit docs:

- Swagger UI: http://localhost:8080/docs
- OpenAPI JSON: http://localhost:8080/openapi.json

## Authentication

All endpoints require an `Authorization: Bearer <API_BEARER_TOKEN>` header. Set `API_BEARER_TOKEN` in your `.env`.

Outgoing requests to Grafana use `GRAFANA_API_KEY` as `Authorization: Bearer <GRAFANA_API_KEY>`.

## Endpoints (Summary)

- GET /api/health
- Dashboards: /api/dashboards (GET, POST), /api/dashboards/{uid} (GET, PUT, DELETE)
- Data Sources: /api/datasources (GET, POST), /api/datasources/{id_or_name} (GET), /api/datasources/{id} (PUT, DELETE)
- Alerts: /api/alerts (GET, POST), /api/alerts/{id} (GET, PUT, DELETE)
- Users: /api/users (GET, POST), /api/users/{id} (GET, PUT, DELETE)

## Tests

Run tests:

```bash
pytest
```

## Project Structure

```
backend_api/
  app/
    core/ (auth, config, errors, logging_config)
    models/ (pydantic schemas)
    routers/ (health, dashboards, datasources, alerts, users)
    services/ (grafana_client)
    main.py
  .env.example
  pyproject.toml
  run.py
  tests/
```

## Notes

- The Alerts routes target Grafana's legacy endpoints for demonstration and may need aligning with your Grafana version/unified alerting model.
- The service denies access if API auth is not configured. Ensure `API_BEARER_TOKEN` is set.
