"""Authentication utility functions"""
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
