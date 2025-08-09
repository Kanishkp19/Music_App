#!/usr/bin/env python3
"""
MuseAIka Backend Project Structure Setup Script
Creates all necessary directories and base files for the Flask-based music recommendation API
"""

import os
import sys
from pathlib import Path

def create_directory(path):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)
    print(f"✅ Created directory: {path}")

def create_file(path, content=""):
    """Create file with content if it doesn't exist"""
    file_path = Path(path)
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"📄 Created file: {path}")
    else:
        print(f"⚠️  File exists: {path}")

def setup_backend_structure():
    """Create complete backend project structure"""
    
    print("🎵 Setting up MuseAIka Backend Structure...\n")
    
    # Root files
    create_file("app.py", '''"""Flask application factory for MuseAIka backend"""
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Initialize SocketIO
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.music_routes import music_bp
    from routes.mood_routes import mood_bp
    from routes.user_routes import user_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(music_bp, url_prefix='/api/v1')
    app.register_blueprint(mood_bp, url_prefix='/api/v1')
    app.register_blueprint(user_bp, url_prefix='/api/v1')
    
    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()
    socketio.run(app, debug=True, host='0.0.0.0', port=8000)
''')

    create_file("wsgi.py", '''"""WSGI entry point for production deployment"""
from app import create_app

app, socketio = create_app('production')

if __name__ == "__main__":
    socketio.run(app)
''')

    create_file("config.py", '''"""Configuration management for MuseAIka backend"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/museaika')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Spotify API
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
    
    # Features
    ENABLE_MUSIC_GENERATION = os.getenv('ENABLE_MUSIC_GENERATION', 'True').lower() == 'true'
    ENABLE_REAL_TIME = os.getenv('ENABLE_REAL_TIME', 'True').lower() == 'true'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
''')

    create_file("requirements.txt", '''Flask==2.3.3
Flask-CORS==4.0.0
Flask-SocketIO==5.3.6
python-dotenv==1.0.0
pymongo==4.5.0
redis==5.0.1
requests==2.31.0
tensorflow==2.13.0
opencv-python-headless==4.8.1.78
transformers==4.35.0
torch==2.1.0
spotipy==2.22.1
numpy==1.24.3
Pillow==10.0.1
gunicorn==21.2.0
eventlet==0.33.3
pytest==7.4.3
pytest-cov==4.1.0
black==23.9.1
isort==5.12.0
bandit==1.7.5
''')

    create_file(".env.example", '''# Flask Configuration
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

# Hugging Face
HF_TOKEN=your_hugging_face_token

# Security
JWT_SECRET_KEY=your-jwt-secret-key
ENCRYPT_KEY=your-encryption-key-32-chars

# Features
ENABLE_MUSIC_GENERATION=True
ENABLE_REAL_TIME=True
''')

    # Scripts directory
    create_file("scripts/__init__.py")
    create_file("scripts/init_db.py", '''"""Database initialization script"""
from db.mongo import get_db
from pymongo import MongoClient
import os

def init_database():
    """Initialize MongoDB collections and indexes"""
    db = get_db()
    
    # Create indexes
    db.users.create_index("spotify_id", unique=True)
    db.playlists.create_index("owner_id")
    db.mood_history.create_index([("user_id", 1), ("timestamp", -1)])
    db.generated_music.create_index("job_id", unique=True)
    
    print("✅ Database initialized successfully")

if __name__ == "__main__":
    init_database()
''')

    create_file("scripts/setup.py", '''"""Automated setup script for development environment"""
import subprocess
import sys
import os

def run_command(command):
    """Run shell command and handle errors"""
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🚀 Setting up MuseAIka development environment...")
    
    # Install dependencies
    if run_command("pip install -r requirements.txt"):
        print("✅ Dependencies installed")
    else:
        print("❌ Failed to install dependencies")
        return
    
    # Copy environment file
    if not os.path.exists('.env') and os.path.exists('.env.example'):
        run_command("cp .env.example .env")
        print("✅ Environment file created")
    
    print("🎉 Setup complete! Edit .env with your configuration.")

if __name__ == "__main__":
    main()
''')

    # Modules directory
    create_file("modules/__init__.py")
    create_file("modules/emotion_detection.py", '''"""Computer vision emotion detection module"""
import cv2
import numpy as np
from typing import Dict, Tuple

class EmotionDetector:
    def __init__(self):
        self.emotions = ['happy', 'sad', 'angry', 'neutral', 'surprise', 'fear', 'disgust']
    
    def detect_from_image(self, image_data: bytes) -> Dict:
        """Detect emotions from image data"""
        # TODO: Implement emotion detection logic
        return {
            'primary_mood': 'happy',
            'confidence': 0.85,
            'emotions': {'happy': 0.85, 'neutral': 0.15}
        }
    
    def preprocess_image(self, image_data: bytes) -> np.ndarray:
        """Preprocess image for emotion detection"""
        # TODO: Implement image preprocessing
        pass
''')

    create_file("modules/sentiment_analysis.py", '''"""Text sentiment analysis module"""
from transformers import pipeline
from typing import Dict

class SentimentAnalyzer:
    def __init__(self):
        # TODO: Initialize sentiment analysis model
        self.classifier = None
    
    def analyze_text(self, text: str) -> Dict:
        """Analyze sentiment from text"""
        # TODO: Implement sentiment analysis
        return {
            'sentiment': 'positive',
            'confidence': 0.8,
            'mood_mapping': 'happy'
        }
''')

    create_file("modules/music_generator.py", '''"""Magenta-based music generation module"""
import tensorflow as tf
from typing import Dict, Optional

class MusicGenerator:
    def __init__(self):
        # TODO: Initialize Magenta models
        pass
    
    def generate_music(self, mood: str, tempo: int = 120, length: int = 30) -> str:
        """Generate music based on mood parameters"""
        # TODO: Implement music generation
        return "job_id_placeholder"
    
    def get_generation_status(self, job_id: str) -> Dict:
        """Get status of music generation job"""
        # TODO: Implement status checking
        return {'status': 'completed', 'download_url': f'/download/{job_id}'}
''')

    create_file("modules/spotify_service.py", '''"""Spotify Web API integration service"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import List, Dict

class SpotifyService:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
    
    def get_recommendations(self, mood: str, limit: int = 20) -> List[Dict]:
        """Get mood-based recommendations from Spotify"""
        # TODO: Implement Spotify recommendations
        return []
    
    def create_playlist(self, user_id: str, name: str, tracks: List[str]) -> str:
        """Create playlist on Spotify"""
        # TODO: Implement playlist creation
        return "playlist_id_placeholder"
''')

    create_file("modules/playlist_manager.py", '''"""Playlist CRUD operations module"""
from db.mongo import get_db
from typing import List, Dict, Optional
from bson import ObjectId

class PlaylistManager:
    def __init__(self):
        self.db = get_db()
    
    def create_playlist(self, owner_id: str, title: str, tracks: List = None) -> Dict:
        """Create new playlist"""
        playlist = {
            'owner_id': ObjectId(owner_id),
            'title': title,
            'tracks': tracks or [],
            'created_at': None,  # TODO: Add timestamp
            'updated_at': None
        }
        result = self.db.playlists.insert_one(playlist)
        return {'id': str(result.inserted_id)}
    
    def get_user_playlists(self, user_id: str) -> List[Dict]:
        """Get all playlists for a user"""
        # TODO: Implement playlist retrieval
        return []
''')

    # Routes directory
    create_file("routes/__init__.py")
    create_file("routes/auth_routes.py", '''"""Authentication route handlers"""
from flask import Blueprint, request, jsonify, session
from modules.spotify_service import SpotifyService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/spotify/login')
def spotify_login():
    """Redirect to Spotify OAuth"""
    # TODO: Implement Spotify OAuth login
    return jsonify({'auth_url': 'https://accounts.spotify.com/authorize'})

@auth_bp.route('/spotify/callback')
def spotify_callback():
    """Handle Spotify OAuth callback"""
    # TODO: Handle OAuth callback
    return jsonify({'success': True})

@auth_bp.route('/me')
def get_current_user():
    """Get current user information"""
    # TODO: Get user from session
    return jsonify({'user': None})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'success': True})
''')

    create_file("routes/music_routes.py", '''"""Music-related route handlers"""
from flask import Blueprint, request, jsonify
from modules.spotify_service import SpotifyService
from modules.music_generator import MusicGenerator

music_bp = Blueprint('music', __name__)

@music_bp.route('/recommendations')
def get_recommendations():
    """Get mood-based music recommendations"""
    mood = request.args.get('mood', 'happy')
    limit = int(request.args.get('limit', 20))
    
    # TODO: Get recommendations based on mood
    return jsonify({'recommendations': []})

@music_bp.route('/playlists', methods=['GET', 'POST'])
def handle_playlists():
    """Handle playlist operations"""
    if request.method == 'GET':
        # TODO: Get user playlists
        return jsonify({'playlists': []})
    else:
        # TODO: Create new playlist
        return jsonify({'success': True})

@music_bp.route('/generate', methods=['POST'])
def generate_music():
    """Start music generation"""
    data = request.get_json()
    mood = data.get('mood', 'happy')
    
    # TODO: Start generation job
    return jsonify({'job_id': 'placeholder', 'status': 'queued'})

@music_bp.route('/generate/<job_id>')
def get_generation_status(job_id):
    """Get generation status"""
    # TODO: Check generation status
    return jsonify({'status': 'completed'})
''')

    create_file("routes/mood_routes.py", '''"""Mood detection route handlers"""
from flask import Blueprint, request, jsonify
from modules.emotion_detection import EmotionDetector
from modules.sentiment_analysis import SentimentAnalyzer

mood_bp = Blueprint('mood', __name__)

@mood_bp.route('/detect/emotion', methods=['POST'])
def detect_emotion():
    """Detect emotion from uploaded image"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image = request.files['image']
    detector = EmotionDetector()
    
    # TODO: Process image and detect emotions
    result = detector.detect_from_image(image.read())
    return jsonify({'success': True, 'data': result})

@mood_bp.route('/detect/sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyze sentiment from text"""
    data = request.get_json()
    text = data.get('text', '')
    
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_text(text)
    
    return jsonify({'success': True, 'data': result})

@mood_bp.route('/detect/history')
def get_mood_history():
    """Get user's mood history"""
    # TODO: Get mood history from database
    return jsonify({'history': []})
''')

    create_file("routes/user_routes.py", '''"""User management route handlers"""
from flask import Blueprint, request, jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
def get_profile():
    """Get user profile"""
    # TODO: Get user profile
    return jsonify({'profile': {}})

@user_bp.route('/preferences', methods=['GET', 'PUT'])
def handle_preferences():
    """Handle user preferences"""
    if request.method == 'GET':
        # TODO: Get preferences
        return jsonify({'preferences': {}})
    else:
        # TODO: Update preferences
        return jsonify({'success': True})

@user_bp.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'museaika-backend'})
''')

    # WebSocket directory
    create_file("websocket/__init__.py")
    create_file("websocket/mood_socket.py", '''"""Real-time mood updates via WebSocket"""
from flask_socketio import SocketIO, emit, join_room, leave_room

class MoodSocketManager:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup WebSocket event handlers"""
        
        @self.socketio.on('subscribe_mood', namespace='/realtime')
        def handle_subscribe_mood(data):
            user_id = data.get('user_id')
            join_room(f"user_{user_id}", namespace='/realtime')
            emit('subscribed', {'user_id': user_id})
        
        @self.socketio.on('playlist_edit', namespace='/realtime')
        def handle_playlist_edit(data):
            # TODO: Handle collaborative playlist editing
            emit('playlist_update', data, broadcast=True)
    
    def broadcast_mood_update(self, user_id: str, mood_data: dict):
        """Broadcast mood update to subscribed clients"""
        self.socketio.emit('mood_update', mood_data, 
                          room=f"user_{user_id}", namespace='/realtime')
''')

    # Database directory
    create_file("db/__init__.py")
    create_file("db/mongo.py", '''"""MongoDB connection and utilities"""
from pymongo import MongoClient
from config import Config
import os

_db = None

def get_db():
    """Get MongoDB database connection"""
    global _db
    if _db is None:
        client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
        _db = client.museaika
    return _db

def close_db():
    """Close database connection"""
    global _db
    if _db is not None:
        _db.client.close()
        _db = None
''')

    create_file("db/redis_client.py", '''"""Redis connection and utilities"""
import redis
import json
from typing import Any, Optional
import os

class RedisClient:
    def __init__(self):
        self.client = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/0'))
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set key-value with optional TTL"""
        serialized = json.dumps(value) if not isinstance(value, str) else value
        self.client.set(key, serialized, ex=ttl)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value by key"""
        value = self.client.get(key)
        if value:
            try:
                return json.loads(value.decode('utf-8'))
            except json.JSONDecodeError:
                return value.decode('utf-8')
        return None
    
    def delete(self, key: str):
        """Delete key"""
        self.client.delete(key)

# Global Redis client instance
redis_client = RedisClient()
''')

    # Utils directory
    create_file("utils/__init__.py")
    create_file("utils/audio_utils.py", '''"""Audio processing utilities"""
import numpy as np
from typing import Tuple

def convert_audio_format(input_data: bytes, target_format: str = 'mp3') -> bytes:
    """Convert audio to target format"""
    # TODO: Implement audio conversion
    return input_data

def extract_audio_features(audio_data: bytes) -> dict:
    """Extract features from audio for analysis"""
    # TODO: Implement feature extraction
    return {'tempo': 120, 'key': 'C', 'energy': 0.8}

def generate_waveform(duration: int, frequency: int = 440) -> np.ndarray:
    """Generate simple waveform for testing"""
    sample_rate = 44100
    t = np.linspace(0, duration, sample_rate * duration)
    return np.sin(2 * np.pi * frequency * t)
''')

    create_file("utils/auth_utils.py", '''"""Authentication utility functions"""
import jwt
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Optional

def generate_jwt_token(user_data: Dict, secret_key: str, expires_hours: int = 24) -> str:
    """Generate JWT token for user"""
    payload = {
        'user_id': user_data['id'],
        'exp': datetime.utcnow() + timedelta(hours=expires_hours),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def verify_jwt_token(token: str, secret_key: str) -> Optional[Dict]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()
''')

    create_file("utils/validators.py", '''"""Input validation utilities"""
import re
from typing import Dict, List, Any

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_mood_data(data: Dict) -> Dict[str, List[str]]:
    """Validate mood detection data"""
    errors = {}
    
    if 'mood' not in data:
        errors['mood'] = ['Mood field is required']
    elif data['mood'] not in ['happy', 'sad', 'angry', 'neutral', 'surprise', 'fear']:
        errors['mood'] = ['Invalid mood value']
    
    if 'confidence' in data and not (0 <= data['confidence'] <= 1):
        errors['confidence'] = ['Confidence must be between 0 and 1']
    
    return errors

def validate_playlist_data(data: Dict) -> Dict[str, List[str]]:
    """Validate playlist creation data"""
    errors = {}
    
    if 'title' not in data or not data['title'].strip():
        errors['title'] = ['Title is required']
    
    if 'tracks' in data and not isinstance(data['tracks'], list):
        errors['tracks'] = ['Tracks must be a list']
    
    return errors
''')

    # Workers directory
    create_file("workers/__init__.py")
    create_file("workers/generator_worker.py", '''"""Background worker for music generation"""
import time
import threading
from db.redis_client import redis_client
from modules.music_generator import MusicGenerator
from typing import Dict

class GeneratorWorker:
    def __init__(self):
        self.generator = MusicGenerator()
        self.running = False
    
    def start(self):
        """Start the background worker"""
        self.running = True
        thread = threading.Thread(target=self._work_loop)
        thread.daemon = True
        thread.start()
    
    def stop(self):
        """Stop the background worker"""
        self.running = False
    
    def _work_loop(self):
        """Main work loop"""
        while self.running:
            # Check for pending jobs
            job_data = redis_client.client.lpop('queue:generation')
            if job_data:
                self._process_job(job_data)
            else:
                time.sleep(1)  # Wait before checking again
    
    def _process_job(self, job_data: str):
        """Process a single generation job"""
        try:
            import json
            job = json.loads(job_data)
            job_id = job['job_id']
            
            # Update status to processing
            redis_client.set(f"job:{job_id}", {'status': 'processing'})
            
            # Generate music (placeholder)
            result = self.generator.generate_music(
                job['mood'], job.get('tempo', 120), job.get('length', 30)
            )
            
            # Update status to completed
            redis_client.set(f"job:{job_id}", {
                'status': 'completed',
                'result': result
            })
            
        except Exception as e:
            print(f"Job failed: {e}")
            redis_client.set(f"job:{job_id}", {'status': 'failed', 'error': str(e)})

if __name__ == '__main__':
    worker = GeneratorWorker()
    worker.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        worker.stop()
''')

    # Tests directory
    create_file("tests/__init__.py")
    create_file("tests/conftest.py", '''"""Pytest configuration and fixtures"""
import pytest
from app import create_app
from db.mongo import get_db

@pytest.fixture
def app():
    """Create test Flask app"""
    app, socketio = create_app('testing')
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def db():
    """Create test database connection"""
    return get_db()
''')

    create_file("tests/test_emotion.py", '''"""Tests for emotion detection module"""
import pytest
from modules.emotion_detection import EmotionDetector

def test_emotion_detector_init():
    """Test EmotionDetector initialization"""
    detector = EmotionDetector()
    assert len(detector.emotions) == 7
    assert 'happy' in detector.emotions

def test_detect_from_image():
    """Test emotion detection from image"""
    detector = EmotionDetector()
    result = detector.detect_from_image(b"fake_image_data")
    
    assert 'primary_mood' in result
    assert 'confidence' in result
    assert 'emotions' in result
''')

    create_file("tests/test_spotify.py", '''"""Tests for Spotify service"""
import pytest
from modules.spotify_service import SpotifyService

def test_spotify_service_init():
    """Test SpotifyService initialization"""
    service = SpotifyService("client_id", "client_secret", "redirect_uri")
    assert service.client_id == "client_id"
    assert service.client_secret == "client_secret"

def test_get_recommendations():
    """Test getting recommendations"""
    service = SpotifyService("test", "test", "test")
    recommendations = service.get_recommendations("happy")
    assert isinstance(recommendations, list)
''')

    create_file("tests/test_api.py", '''"""API endpoint tests"""
import pytest
import json

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_emotion_detection_no_image(client):
    """Test emotion detection without image"""
    response = client.post('/api/v1/detect/emotion')
    assert response.status_code == 400

def test_sentiment_analysis(client):
    """Test sentiment analysis endpoint"""
    response = client.post('/api/v1/detect/sentiment',
                          json={'text': 'I feel happy today'})
    assert response.status_code == 200
''')

    # Additional files
    create_file("docker-compose.yml", '''version: '3.8'

services:
  mongo:
    image: mongo:5.0
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    environment:
      MONGO_INITDB_DATABASE: museaika

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data --console-address ":9001"

volumes:
  mongo_data:
  redis_data:
  minio_data:
''')

    create_file(".gitignore", '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.venv
venv/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Generated files
generated_music/
uploads/
cache/

# Testing
.coverage
htmlcov/
.pytest_cache/
''')

    create_file("README.md", '''# MuseAIka Backend

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
''')

    # Missing closing functions and execution
    print("\n✅ Creating additional configuration files...")
    
    create_file("Dockerfile", '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    libsndfile1 \\
    ffmpeg \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs generated_music uploads cache

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:8000", "wsgi:app"]
''')

    create_file("Makefile", '''# MuseAIka Backend Makefile

.PHONY: help install setup start stop test clean docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  setup       Setup development environment"
	@echo "  start       Start development server"
	@echo "  stop        Stop all services"
	@echo "  test        Run tests"
	@echo "  clean       Clean generated files"
	@echo "  docker-build Build Docker image"
	@echo "  docker-run  Run with Docker"

install:
	pip install -r requirements.txt

setup:
	python scripts/setup.py

start:
	docker-compose up -d
	python app.py

stop:
	docker-compose down

test:
	python -m pytest tests/ -v --cov=.

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/

docker-build:
	docker build -t museaika-backend .

docker-run:
	docker-compose up --build

lint:
	black . --check
	isort . --check-only

format:
	black .
	isort .

security:
	bandit -r . -f json -o security-report.json
''')

    create_file("pytest.ini", '''[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=.
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80

markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
''')

    create_file("docs/API.md", '''# MuseAIka Backend API Documentation

## Authentication Endpoints

### POST /api/v1/auth/spotify/login
Initiates Spotify OAuth flow
- **Response**: `{"auth_url": "https://accounts.spotify.com/authorize..."}`

### GET /api/v1/auth/spotify/callback
Handles Spotify OAuth callback
- **Parameters**: `code`, `state`
- **Response**: `{"success": true, "user": {...}}`

### GET /api/v1/auth/me
Get current authenticated user
- **Response**: `{"user": {...}}`

### POST /api/v1/auth/logout
Logout current user
- **Response**: `{"success": true}`

## Mood Detection Endpoints

### POST /api/v1/detect/emotion
Detect emotions from uploaded image
- **Content-Type**: `multipart/form-data`
- **Body**: `image` (file)
- **Response**: 
```json
{
  "success": true,
  "data": {
    "primary_mood": "happy",
    "confidence": 0.85,
    "emotions": {"happy": 0.85, "neutral": 0.15}
  }
}
```

### POST /api/v1/detect/sentiment
Analyze sentiment from text
- **Content-Type**: `application/json`
- **Body**: `{"text": "I feel great today!"}`
- **Response**:
```json
{
  "success": true,
  "data": {
    "sentiment": "positive",
    "confidence": 0.8,
    "mood_mapping": "happy"
  }
}
```

### GET /api/v1/detect/history
Get user's mood detection history
- **Response**: `{"history": [...]}`

## Music Endpoints

### GET /api/v1/recommendations
Get mood-based music recommendations
- **Parameters**: `mood` (string), `limit` (int, default: 20)
- **Response**: `{"recommendations": [...]}`

### GET /api/v1/playlists
Get user's playlists
- **Response**: `{"playlists": [...]}`

### POST /api/v1/playlists
Create new playlist
- **Body**: `{"title": "My Playlist", "tracks": [...]}`
- **Response**: `{"success": true, "playlist_id": "..."}`

### POST /api/v1/generate
Start music generation
- **Body**: `{"mood": "happy", "tempo": 120, "length": 30}`
- **Response**: `{"job_id": "...", "status": "queued"}`

### GET /api/v1/generate/{job_id}
Get music generation status
- **Response**: `{"status": "completed", "download_url": "..."}`

## User Endpoints

### GET /api/v1/profile
Get user profile
- **Response**: `{"profile": {...}}`

### GET /api/v1/preferences
Get user preferences
- **Response**: `{"preferences": {...}}`

### PUT /api/v1/preferences
Update user preferences
- **Body**: `{"theme": "dark", "notifications": true}`
- **Response**: `{"success": true}`

### GET /api/v1/health
Health check endpoint
- **Response**: `{"status": "healthy", "service": "museaika-backend"}`

## WebSocket Events

### Namespace: `/realtime`

#### Client → Server Events
- `subscribe_mood`: Subscribe to mood updates for a user
- `playlist_edit`: Edit playlist collaboratively

#### Server → Client Events  
- `mood_update`: Real-time mood detection updates
- `playlist_update`: Real-time playlist changes
- `subscribed`: Confirmation of subscription

## Error Responses

All endpoints return errors in the format:
```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {...}
}
```

Common HTTP status codes:
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error
''')

    create_file("docs/DEPLOYMENT.md", '''# MuseAIka Backend Deployment Guide

## Development Setup

1. **Clone and Setup**
```bash
git clone <repository-url>
cd museaika-backend
python -m venv .venv
source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Start Services**
```bash
docker-compose up -d  # Start MongoDB, Redis, MinIO
python scripts/init_db.py  # Initialize database
```

5. **Run Development Server**
```bash
python app.py
# or
flask run --host=0.0.0.0 --port=8000 --debug
```

## Production Deployment

### Option 1: Docker Compose
```bash
# Build and run with production settings
docker-compose -f docker-compose.prod.yml up --build -d
```

### Option 2: Manual Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=production
export MONGO_URI=your_production_mongo_uri
export REDIS_URL=your_production_redis_url

# Run with Gunicorn
gunicorn --worker-class eventlet -w 4 --bind 0.0.0.0:8000 wsgi:app
```

### Option 3: Kubernetes
```bash
# Apply Kubernetes manifests (create these based on your needs)
kubectl apply -f k8s/
```

## Environment Variables

Required for production:
```bash
FLASK_ENV=production
SECRET_KEY=your-super-secret-key
MONGO_URI=mongodb://user:pass@host:port/database
REDIS_URL=redis://user:pass@host:port/db
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

## Health Checks

- **Endpoint**: `GET /api/v1/health`
- **Expected Response**: `{"status": "healthy", "service": "museaika-backend"}`

## Monitoring

1. **Application Logs**
```bash
# View logs
docker-compose logs -f app
```

2. **Database Monitoring**
```bash
# MongoDB stats
docker exec -it mongo_container mongo --eval "db.stats()"
```

3. **Redis Monitoring**
```bash
# Redis info
docker exec -it redis_container redis-cli info
```

## Scaling

### Horizontal Scaling
- Run multiple app instances behind a load balancer
- Ensure session data is stored in Redis, not memory
- Use external services for MongoDB and Redis

### Vertical Scaling
- Increase CPU/Memory allocation
- Optimize database indexes
- Implement caching strategies

## Security Checklist

- [ ] Change default secrets and keys
- [ ] Enable HTTPS in production
- [ ] Implement rate limiting
- [ ] Validate all inputs
- [ ] Use secure headers
- [ ] Regular security audits with `bandit`

## Backup Strategy

1. **Database Backups**
```bash
# MongoDB backup
docker exec mongo_container mongodump --out /backup
```

2. **Redis Persistence**
```bash
# Ensure Redis persistence is enabled
CONFIG SET save "900 1 300 10 60 10000"
```

## Troubleshooting

### Common Issues

1. **Import Errors**
- Ensure virtual environment is activated
- Check Python path and module installations

2. **Database Connection Issues**
- Verify MongoDB is running and accessible
- Check connection string format

3. **WebSocket Issues**
- Ensure eventlet is installed
- Check CORS configuration

4. **Permission Errors**
- Check file permissions for uploads directory
- Ensure proper user permissions in Docker
''')

    print("\n🎵 MuseAIka Backend structure created successfully!")
    print("\n📋 Next Steps:")
    print("1. cd into your project directory")
    print("2. Create virtual environment: python -m venv .venv")
    print("3. Activate environment: source .venv/bin/activate (Linux/Mac) or .venv\\Scripts\\activate (Windows)")
    print("4. Run setup: python scripts/setup.py")
    print("5. Edit .env file with your configuration")
    print("6. Start services: docker-compose up -d")
    print("7. Initialize database: python scripts/init_db.py")
    print("8. Run server: python app.py")
    print("\n🚀 Your MuseAIka backend is ready for development!")


def main():
    """Main execution function"""
    try:
        setup_backend_structure()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()