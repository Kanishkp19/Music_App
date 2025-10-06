from typing import List, Dict
from src.services.audius_service import AudiusService

class BasicRecommender:
    def __init__(self, audius_service: AudiusService):
        self.audius = audius_service
    
    def get_recommendations_by_mood(self, valence: float, arousal: float, 
                                     limit: int = 20) -> List[Dict]:
        genre, mood_tag = self._mood_to_music_params(valence, arousal)
        tracks = self.audius.search_tracks(genre=genre, mood=mood_tag, limit=limit)
        if not tracks:
            tracks = self.audius.get_trending_tracks(genre=genre, limit=limit)
        if not tracks:
            tracks = self.audius.get_trending_tracks(limit=limit)
        return self._format_recommendations(tracks)
    
    def _mood_to_music_params(self, valence: float, arousal: float) -> tuple:
        if arousal > 0.6 and valence > 0.6:
            return 'Electronic', 'energetic'
        elif arousal > 0.6 and valence < 0.4:
            return 'Rock', 'aggressive'
        elif arousal < 0.4 and valence > 0.6:
            return 'Ambient', 'peaceful'
        elif arousal < 0.4 and valence < 0.4:
            return 'Blues', 'melancholic'
        else:
            return 'Pop', 'uplifting'
    
    def _format_recommendations(self, tracks: List[Dict]) -> List[Dict]:
        formatted = []
        for track in tracks:
            formatted.append({
                'id': track.get('id'),
                'title': track.get('title'),
                'artist': track.get('user', {}).get('name', 'Unknown'),
                'duration': track.get('duration', 0),
                'genre': track.get('genre'),
                'mood': track.get('mood'),
                'artwork_url': self._get_artwork_url(track),
                'stream_url': f"{self.audius.host}/v1/tracks/{track.get('id')}/stream",
                'play_count': track.get('play_count', 0),
                'favorite_count': track.get('favorite_count', 0)
            })
        return formatted
    
    def _get_artwork_url(self, track: Dict) -> str:
        artwork = track.get('artwork', {})
        if artwork and artwork.get('1000x1000'):
            return artwork['1000x1000']
        return None
