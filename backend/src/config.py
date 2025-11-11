import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/museaika')
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key-change-in-production')
    JWT_EXPIRATION = timedelta(days=7)
    AUDIUS_API_KEY = os.getenv('AUDIUS_API_KEY', '')
    AUDIUS_HOST = 'https://discoveryprovider.audius.co'
    EMOTION_MODEL = 'trpakov/vit-face-expression'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
    
    # Music Generation Settings
    GENERATION_OUTPUT_DIR = os.getenv('GENERATION_OUTPUT_DIR', 'generated_music')
    MAX_GENERATION_DURATION = int(os.getenv('MAX_GENERATION_DURATION', 120))  # seconds
    MIN_GENERATION_DURATION = int(os.getenv('MIN_GENERATION_DURATION', 15))  # seconds
    SUPPORTED_AUDIO_FORMATS = ['wav', 'mp3']
    DEFAULT_AUDIO_FORMAT = 'wav'
    GENERATION_CLEANUP_HOURS = int(os.getenv('GENERATION_CLEANUP_HOURS', 24))  # hours

