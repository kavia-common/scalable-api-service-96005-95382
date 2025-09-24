# Backend API

FastAPI-based backend for the Scalable API Service.

## Features
- FastAPI with automatic OpenAPI (Swagger) docs
- Health check endpoint at `/health`
- Documentation helper at `/websocket-usage`

## Requirements
- Python 3.10 or later (recommended)
- pip

## Setup
1. (Optional) Create and activate a virtual environment.
2. Install dependencies:
   ```
   pip install --no-cache-dir -r requirements.txt
   ```

3. Create a `.env` file if needed for environment-specific values. Do not commit secrets.

Supported env variables:
- `ENVIRONMENT`: environment name, e.g., `development`, `staging`, `production`.

## Run
Run with Uvicorn:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Visit:
- OpenAPI docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

## Project Structure
```
backend_api/
├─ app/
│  └─ main.py        # FastAPI app entrypoint (app.main:app)
├─ requirements.txt  # Python dependencies
├─ README.md
└─ .env              # environment variables (not committed)
```
