from pymongo import MongoClient
from pymongo.database import Database

_client = None
_db = None

def init_db(mongodb_uri: str) -> Database:
    global _client, _db
    _client = MongoClient(mongodb_uri)
    _db = _client.get_database()
    _db.users.create_index('email', unique=True)
    _db.mood_entries.create_index([('user_id', 1), ('timestamp', -1)])
    return _db

def get_db() -> Database:
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db first.")
    return _db
