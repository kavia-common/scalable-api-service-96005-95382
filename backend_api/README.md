# Grafana Proxy API (FastAPI)

Modern, modular FastAPI backend that proxies CRUD operations to Grafana's REST API.

Features:
- Modular structure (routers, services, auth, utils)
- CRUD for Dashboards, Data Sources, Alerts (unified alerting), and Users
- Bearer authentication for all endpoints (TOKEN_SECRET)
- All outbound calls use Grafana API Key
- Typed Pydantic models and examples in Swagger
- Centralized logging and exception handling
- Environment-based configuration via `.env`
- Basic unit tests (pytest)

## Structure

```
backend_api/
  src/api/
    main.py
    auth/
      dependencies.py
    routers/
      dashboards.py
      datasources.py
      alerts.py
      users.py
    services/
      grafana_client.py
    utils/
      config.py
      logging_config.py
      errors.py
      examples.py
  tests/
    conftest.py
    test_health.py
    test_dashboards.py
    test_datasources.py
    test_alerts.py
    test_users.py
  requirements.txt
  .env.example
  README.md
```

## Environment Variables

Create a `.env` file from `.env.example` and set:
- GRAFANA_BASE_URL: Base URL of Grafana (e.g., http://localhost:3000)
- GRAFANA_API_KEY: Grafana API key with required permissions
- TOKEN_SECRET: Bearer token expected by this API
- LOG_LEVEL: Logging level (INFO, DEBUG, etc.)

Note: Do not commit your `.env`.

## Install & Run

1. Python 3.10+ recommended.
2. Create venv and install dependencies:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Configure environment:
   - Copy `.env.example` to `.env`
   - Set values for your environment

4. Run the server:

```
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

5. Open docs: http://localhost:8000/docs

All endpoints require a header:
```
Authorization: Bearer <TOKEN_SECRET>
```

## Testing

```
pytest -q
```

## Notes

- This service does not store data; it proxies requests to Grafana using your configured API key.
- Ensure the Grafana API key has sufficient privileges for the operations you intend to perform.
