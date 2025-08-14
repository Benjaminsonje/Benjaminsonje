## E-commerce Backend (FastAPI)

### Quickstart

- Create a virtual environment and install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

- Run the API:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API docs: http://localhost:8000/docs

### Environment variables

- `SECRET_KEY`: secret for JWT signing (default auto-generated, but override in production)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: token expiry in minutes (default: 60)
- `SQLALCHEMY_DATABASE_URI`: database URL (default: sqlite:///./ecommerce.db)
- `CORS_ORIGINS`: comma-separated list of allowed origins (default: *)

Create a `.env` file in the project root to override defaults.

### Project structure

```
ecommerce-backend/
  app/
    core/
    db/
    models/
    routers/
    schemas/
    main.py
  requirements.txt
  README.md
```