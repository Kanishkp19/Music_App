import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from src.config import Config

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id: str) -> str:
    payload = {'user_id': user_id, 'exp': datetime.utcnow() + Config.JWT_EXPIRATION}
    return jwt.encode(payload, Config.JWT_SECRET, algorithm='HS256')

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise ValueError('Token expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        try:
            payload = decode_token(token)
            request.user_id = payload['user_id']
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        return f(*args, **kwargs)
    return decorated

def map_emotion_to_mood(emotion: str) -> dict:
    mapping = {
        'happy': {'valence': 0.8, 'arousal': 0.7},
        'joy': {'valence': 0.9, 'arousal': 0.8},
        'excited': {'valence': 0.7, 'arousal': 0.9},
        'sad': {'valence': 0.2, 'arousal': 0.3},
        'angry': {'valence': 0.1, 'arousal': 0.8},
        'fear': {'valence': 0.2, 'arousal': 0.7},
        'disgust': {'valence': 0.1, 'arousal': 0.5},
        'surprise': {'valence': 0.5, 'arousal': 0.8},
        'neutral': {'valence': 0.5, 'arousal': 0.5},
        'calm': {'valence': 0.6, 'arousal': 0.2}
    }
    return mapping.get(emotion.lower(), {'valence': 0.5, 'arousal': 0.5})
