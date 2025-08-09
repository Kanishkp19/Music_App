"""Database initialization script"""
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
