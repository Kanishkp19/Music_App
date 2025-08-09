"""Redis connection and utilities"""
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
