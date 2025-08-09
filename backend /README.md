# MuseAIka Backend

Flask-based API server for emotion-driven music recommendations and generation.

## Quick Start

1. Clone repository and navigate to backend
2. Create virtual environment: `python -m venv .venv`
3. Activate environment: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy environment file: `cp .env.example .env`
6. Edit `.env` with your configuration
7. Start services: `docker-compose up -d`
8. Initialize database: `python scripts/init_db.py`
9. Run server: `flask run --host=0.0.0.0 --port=8000`

## API Endpoints

- `GET /api/v1/health` - Health check
- `POST /api/v1/detect/emotion` - Detect emotion from image
- `POST /api/v1/detect/sentiment` - Analyze text sentiment
- `GET /api/v1/recommendations` - Get mood-based recommendations
- `POST /api/v1/generate` - Generate music

## Development

```bash
# Run tests
python -m pytest

# Format code
black .
isort .

# Run development server
flask run --debug
```

## Documentation

See `/docs` for detailed API documentation and architecture overview.
