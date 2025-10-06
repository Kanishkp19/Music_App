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
            print(f"Audius API error: {e}")
            return []
    
    def get_trending_tracks(self, genre: str = None, limit: int = 20) -> List[Dict]:
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
            print(f"Audius API error: {e}")
            return []
    
    def get_track(self, track_id: str) -> Dict:
        try:
            response = self.session.get(
                f'{self.host}/v1/tracks/{track_id}',
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get('data', {})
        except Exception as e:
            print(f"Audius API error: {e}")
            return {}
