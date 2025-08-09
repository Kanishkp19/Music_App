# MuseAIka Backend

> **Flask-based API server for emotion-driven music recommendations and generation**
>
> **Stack**: Flask + TensorFlow/Magenta + Hugging Face Transformers + Spotify Web API + MongoDB + Redis + Socket.IO

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture Overview](#architecture-overview)
3. [API Endpoints](#api-endpoints)
4. [WebSocket Events](#websocket-events)
5. [Database Models](#database-models)
6. [Environment Configuration](#environment-configuration)
7. [Development Setup](#development-setup)
8. [Production Deployment](#production-deployment)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)

---

## Quick Start

```bash
# 1. Clone and navigate to backend
cd backend

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# 5. Start services (requires MongoDB and Redis)
docker-compose up -d mongo redis  # Or install locally

# 6. Initialize database
python scripts/init_db.py

# 7. Run development server
flask run --host=0.0.0.0 --port=8000

# Backend will be available at http://localhost:8000
```

---

## Architecture Overview

```
backend/
├── app.py                    # Flask application factory
├── wsgi.py                   # Production WSGI entry point
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── scripts/
│   ├── init_db.py           # Database initialization
│   └── setup.py             # Automated setup script
├── modules/
│   ├── __init__.py
│   ├── emotion_detection.py # Computer vision emotion analysis
│   ├── sentiment_analysis.py# Text sentiment processing
│   ├── music_generator.py   # Magenta-based music generation
│   ├── spotify_service.py   # Spotify Web API integration
│   └── playlist_manager.py  # Playlist CRUD operations
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py       # Authentication endpoints
│   ├── music_routes.py      # Music-related endpoints
│   ├── mood_routes.py       # Emotion/mood endpoints
│   └── user_routes.py       # User management endpoints
├── websocket/
│   ├── __init__.py
│   └── mood_socket.py       # Real-time mood updates
├── db/
│   ├── __init__.py
│   ├── mongo.py             # MongoDB connection
│   └── redis_client.py      # Redis connection
├── utils/
│   ├── __init__.py
│   ├── audio_utils.py       # Audio processing utilities
│   ├── auth_utils.py        # Authentication helpers
│   └── validators.py        # Input validation
├── workers/
│   ├── __init__.py
│   └── generator_worker.py  # Background music generation
└── tests/
    ├── test_emotion.py
    ├── test_spotify.py
    └── test_api.py
```

---

## API Endpoints

### Base URL: `http://localhost:8000/api/v1`

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/auth/spotify/login` | Redirect to Spotify OAuth |
| GET | `/auth/spotify/callback` | Handle Spotify OAuth callback |
| GET | `/auth/me` | Get current user info |
| POST | `/auth/logout` | Logout user |

### Emotion Detection

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| POST | `/detect/emotion` | Detect emotion from image | `multipart/form-data` with image |
| POST | `/detect/sentiment` | Analyze text sentiment | `{"text": "I feel happy today"}` |
| GET | `/detect/history` | Get user's mood history | - |

### Music & Playlists

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| GET | `/recommendations` | Get mood-based recommendations | Query: `?mood=happy&limit=20` |
| POST | `/playlists` | Create new playlist | `{"title": "My Mood", "tracks": []}` |
| GET | `/playlists` | Get user's playlists | - |
| PUT | `/playlists/{id}` | Update playlist | `{"title": "Updated", "tracks": [...]}` |
| DELETE | `/playlists/{id}` | Delete playlist | - |

### Music Generation

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| POST | `/generate` | Start music generation | `{"mood": "happy", "tempo": 120, "length": 30}` |
| GET | `/generate/{job_id}` | Get generation status/result | - |
| GET | `/generate/{job_id}/download` | Download generated audio | - |

### Health & Monitoring

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/metrics` | Application metrics |

---

## WebSocket Events

### Namespace: `/realtime`

**Client → Server:**
```javascript
// Subscribe to mood updates
socket.emit('subscribe_mood', {user_id: 'user123'});

// Collaborative playlist editing
socket.emit('playlist_edit', {
    playlist_id: 'playlist123',
    action: 'add_track',
    data: {track_id: 'spotify:track:...'}
});
```

**Server → Client:**
```javascript
// Mood update broadcast
socket.on('mood_update', (data) => {
    // {user_id, mood, scores, timestamp}
});

// Music generation complete
socket.on('generate_complete', (data) => {
    // {job_id, download_url, metadata}
});

// Playlist update
socket.on('playlist_update', (data) => {
    // {playlist_id, action, data, user}
});
```

---

## Database Models

### MongoDB Collections

#### Users
```javascript
{
    "_id": ObjectId("..."),
    "spotify_id": "spotify_user_123",
    "display_name": "John Doe",
    "email": "john@example.com",
    "tokens": {
        "access_token": "encrypted_token",
        "refresh_token": "encrypted_refresh_token",
        "expires_at": 1640995200
    },
    "preferences": {
        "privacy_level": "standard",
        "auto_generate": true
    },
    "created_at": ISODate("2024-01-01T00:00:00Z"),
    "updated_at": ISODate("2024-01-01T00:00:00Z")
}
```

#### Playlists
```javascript
{
    "_id": ObjectId("..."),
    "owner_id": ObjectId("..."),
    "title": "Happy Vibes",
    "description": "Auto-generated happy playlist",
    "tracks": [
        {
            "track_id": "spotify:track:4iV5W9uYEdYUVa79Axb7Rh",
            "added_by": ObjectId("..."),
            "added_at": ISODate("2024-01-01T00:00:00Z"),
            "mood_context": "happy"
        }
    ],
    "collaborators": [ObjectId("...")],
    "mood_tags": ["happy", "energetic"],
    "is_public": false,
    "spotify_playlist_id": "37i9dQZF1DX0XUsuxWHRQd",
    "created_at": ISODate("2024-01-01T00:00:00Z"),
    "updated_at": ISODate("2024-01-01T00:00:00Z")
}
```

#### Mood History
```javascript
{
    "_id": ObjectId("..."),
    "user_id": ObjectId("..."),
    "emotion_scores": {
        "happy": 0.82,
        "neutral": 0.15,
        "sad": 0.03
    },
    "primary_mood": "happy",
    "confidence": 0.82,
    "source": "camera", // "camera", "text", "manual"
    "context": {
        "text_input": "Having a great day!",
        "session_id": "session_123"
    },
    "timestamp": ISODate("2024-01-01T12:00:00Z")
}
```

#### Generated Music
```javascript
{
    "_id": ObjectId("..."),
    "job_id": "gen_uuid_123",
    "user_id": ObjectId("..."),
    "parameters": {
        "mood": "happy",
        "tempo": 120,
        "length_seconds": 30,
        "instrument": "piano"
    },
    "status": "completed", // "queued", "processing", "completed", "failed"
    "result": {
        "audio_url": "https://storage/gen_uuid_123.mp3",
        "midi_url": "https://storage/gen_uuid_123.mid",
        "metadata": {
            "key": "C major",
            "time_signature": "4/4"
        }
    },
    "created_at": ISODate("2024-01-01T00:00:00Z"),
    "completed_at": ISODate("2024-01-01T00:01:30Z")
}
```

### Redis Schema

```
# User sessions
session:{user_id} -> JSON session data

# Mood timeseries
mood:{user_id} -> Sorted set (score=timestamp, value=mood_data)

# Socket.IO room management
socketio:user:{user_id} -> Set of socket_ids

# Generation job queue
queue:generation -> List of job_ids

# Cache
cache:recommendations:{mood}:{user_id} -> JSON recommendations (TTL: 1h)
cache:spotify:track:{track_id} -> JSON track info (TTL: 24h)
```

---

## Environment Configuration

### `.env` File Structure

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-super-secret-key-here
DEBUG=True

# Database URLs
MONGO_URI=mongodb://localhost:27017/museaika
REDIS_URL=redis://localhost:6379/0

# Spotify API
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:3000/auth/callback

# Object Storage (MinIO/S3)
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET_NAME=museaika-storage
S3_REGION=us-east-1

# Hugging Face (for models)
HF_TOKEN=your_hugging_face_token

# Security
JWT_SECRET_KEY=your-jwt-secret-key
ENCRYPT_KEY=your-encryption-key-32-chars

# Performance
WORKERS=4
REDIS_POOL_SIZE=10
MONGO_POOL_SIZE=10

# Features
ENABLE_MUSIC_GENERATION=True
ENABLE_REAL_TIME=True
DEBUG_EMOTION_DETECTION=False
```

### Required External Services

1. **Spotify Developer Account**
   - Create app at https://developer.spotify.com/
   - Get Client ID and Secret
   - Set redirect URI to your frontend callback

2. **Hugging Face Account** (optional, for custom models)
   - Sign up at https://huggingface.co/
   - Create access token for model downloads

3. **MongoDB** (local or cloud)
   - Local: `brew install mongodb` or Docker
   - Cloud: MongoDB Atlas

4. **Redis** (local or cloud)
   - Local: `brew install redis` or Docker
   - Cloud: Redis Cloud, AWS ElastiCache

---

## Development Setup

### Prerequisites

- Python 3.9+ 
- MongoDB 4.4+
- Redis 6.0+
- FFmpeg (for audio processing)
- Git

### Step-by-Step Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/museaika.git
   cd museaika/backend
   ```

2. **Python Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

4. **Start Dependencies**
   ```bash
   # Using Docker
   docker-compose up -d mongo redis minio

   # Or install locally
   brew services start mongodb-community
   brew services start redis
   ```

5. **Initialize Database**
   ```bash
   python scripts/init_db.py
   ```

6. **Run Tests**
   ```bash
   python -m pytest tests/ -v
   ```

7. **Start Development Server**
   ```bash
   flask run --host=0.0.0.0 --port=8000 --debug
   ```

### Development Commands

```bash
# Run with auto-reload
flask run --debug

# Run background worker
python -m workers.generator_worker

# Database migration/reset
python scripts/reset_db.py
python scripts/init_db.py

# Run specific tests
python -m pytest tests/test_emotion.py -v

# Code formatting
black .
isort .

# Security check
bandit -r .
```

---

## Production Deployment

### Using Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run application
CMD ["gunicorn", "-k", "eventlet", "-w", "4", "--bind", "0.0.0.0:8000", "wsgi:app"]
```

### Using Docker Compose

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# Scale workers
docker-compose -f docker-compose.prod.yml up -d --scale worker=3
```

### Environment Variables for Production

```bash
FLASK_ENV=production
DEBUG=False
WORKERS=4
MONGO_URI=mongodb://mongo:27017/museaika
REDIS_URL=redis://redis:6379/0
S3_ENDPOINT=https://your-s3-endpoint.com
```

---

## Testing

### Running Tests

```bash
# All tests
python -m pytest

# With coverage
python -m pytest --cov=modules --cov=routes

# Specific test file
python -m pytest tests/test_emotion.py -v

# Integration tests only
python -m pytest tests/integration/ -v
```

### Test Categories

1. **Unit Tests** (`tests/unit/`)
   - Individual module testing
   - Mock external dependencies
   - Fast execution

2. **Integration Tests** (`tests/integration/`)
   - API endpoint testing
   - Database operations
   - Service interactions

3. **E2E Tests** (`tests/e2e/`)
   - Full workflow testing
   - WebSocket functionality
   - File upload/download

### Test Configuration

```python
# tests/conftest.py
import pytest
from app import create_app
from db.mongo import get_db

@pytest.fixture
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    return app.test_client()
```

---

## Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   ```bash
   # Check MongoDB status
   brew services list | grep mongodb
   
   # Restart MongoDB
   brew services restart mongodb-community
   ```

2. **Redis Connection Failed**
   ```bash
   # Check Redis status
   redis-cli ping
   
   # Should return "PONG"
   ```

3. **Spotify API 401 Unauthorized**
   - Check client ID and secret in `.env`
   - Verify redirect URI matches Spotify app settings
   - Ensure tokens haven't expired

4. **Emotion Detection Not Working**
   ```bash
   # Check OpenCV installation
   python -c "import cv2; print(cv2.__version__)"
   
   # Reinstall if needed
   pip uninstall opencv-python
   pip install opencv-python-headless
   ```

5. **Music Generation Fails**
   ```bash
   # Check TensorFlow installation
   python -c "import tensorflow as tf; print(tf.__version__)"
   
   # Check Magenta
   python -c "import magenta; print('OK')"
   ```

6. **WebSocket Not Connecting**
   - Ensure `eventlet` is installed: `pip install eventlet`
   - Use eventlet worker: `gunicorn -k eventlet`
   - Check CORS settings for WebSocket

### Debug Mode

Enable detailed logging:

```python
# In config.py
import logging
logging.basicConfig(level=logging.DEBUG)

# In app.py
app.logger.setLevel(logging.DEBUG)
```

### Performance Monitoring

```bash
# Monitor Redis
redis-cli monitor

# Monitor MongoDB
db.runCommand({currentOp: 1})

# Check memory usage
python -m memory_profiler app.py
```

---

## API Response Examples

### Emotion Detection Response
```json
{
    "success": true,
    "data": {
        "primary_mood": "happy",
        "confidence": 0.87,
        "emotions": {
            "happy": 0.87,
            "neutral": 0.10,
            "sad": 0.02,
            "angry": 0.01
        },
        "recommendations": [
            {
                "playlist_id": "37i9dQZF1DX0XUsuxWHRQd",
                "name": "Happy Hits",
                "reason": "matches_happy_mood"
            }
        ]
    },
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### Music Generation Response
```json
{
    "success": true,
    "data": {
        "job_id": "gen_uuid_123",
        "status": "queued",
        "estimated_time": 45,
        "parameters": {
            "mood": "happy",
            "tempo": 120,
            "length": 30
        }
    }
}
```

---

For additional help, check the [project documentation](../docs/) or open an issue on GitHub.