import requests
from typing import List, Dict

class AudiusService:
    def __init__(self, host: str, api_key: str = None):
        self.host = host
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers['X-API-Key'] = api_key
    
    def search_tracks(self, query: str = None, genre: str = None, 
                      mood: str = None, limit: int = 20) -> List[Dict]:
        """Search for tracks with optional filters"""
        try:
            params = {'limit': limit}
            if query:
                params['query'] = query
            if genre:
                params['genre'] = genre
            if mood:
                params['mood'] = mood
            
            response = self.session.get(
                f'{self.host}/v1/tracks/search',
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except Exception as e:
            print(f"Audius API error in search_tracks: {e}")
            return []
    
    def get_trending_tracks(self, genre: str = None, limit: int = 20) -> List[Dict]:
        """Get trending tracks, optionally filtered by genre"""
        try:
            params = {'limit': limit}
            if genre:
                params['genre'] = genre
            
            response = self.session.get(
                f'{self.host}/v1/tracks/trending',
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except Exception as e:
            print(f"Audius API error in get_trending_tracks: {e}")
            return []
    
    def get_track(self, track_id: str) -> Dict:
        """Get details for a specific track by ID"""
        try:
            response = self.session.get(
                f'{self.host}/v1/tracks/{track_id}',
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get('data', {})
        except Exception as e:
            print(f"Audius API error in get_track: {e}")
            return {}
    
    def search_by_artist(self, artist_name: str, limit: int = 20) -> List[Dict]:
        """Search tracks by artist name"""
        try:
            response = self.session.get(
                f'{self.host}/v1/tracks/search',
                params={'query': artist_name, 'limit': limit},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except Exception as e:
            print(f"Audius API error in search_by_artist: {e}")
            return []