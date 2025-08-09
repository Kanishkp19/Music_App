"""MongoDB connection and utilities"""
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
