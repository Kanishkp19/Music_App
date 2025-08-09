"""Input validation utilities"""
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
