from typing import List, Dict, Optional
from src.services.audius_service import AudiusService


class EnhancedRecommender:
    """Enhanced music recommender with focus on Bollywood and Pop music"""
    
    def __init__(self, audius_service: AudiusService):
        self.audius = audius_service
        
        # Major international pop artists
        self.pop_artists = [
            'Ed Sheeran', 'Coldplay', 'Taylor Swift', 'The Weeknd',
            'Ariana Grande', 'Bruno Mars', 'Dua Lipa', 'Harry Styles',
            'Adele', 'Sam Smith', 'Billie Eilish', 'Post Malone',
            'Shawn Mendes', 'Justin Bieber', 'Maroon 5'
        ]
        
        # Major Bollywood artists and music directors
        self.bollywood_artists = [
            'Arijit Singh', 'Shreya Ghoshal', 'Atif Aslam', 'Neha Kakkar',
            'Sonu Nigam', 'A.R. Rahman', 'Pritam', 'Vishal-Shekhar',
            'Sunidhi Chauhan', 'KK', 'Mohit Chauhan', 'Armaan Malik',
            'Badshah', 'Guru Randhawa', 'Yo Yo Honey Singh', 'Divine',
            'Jubin Nautiyal', 'Darshan Raval', 'B Praak', 'Sachin-Jigar'
        ]
        
        # Classic hit artists (70s-90s)
        self.classic_artists = [
            'Michael Jackson', 'Queen', 'The Beatles', 'ABBA',
            'Kishore Kumar', 'Lata Mangeshkar', 'Mohammed Rafi',
            'R.D. Burman', 'Asha Bhosle', 'Whitney Houston'
        ]
    
    def get_recommendations_by_mood(self, valence: float, arousal: float, 
                                     limit: int = 20, include_classics: bool = True) -> List[Dict]:
        """
        Get recommendations based on mood with focus on Bollywood and Pop
        
        Args:
            valence: Mood positivity (0-1, low=sad, high=happy)
            arousal: Energy level (0-1, low=calm, high=energetic)
            limit: Number of tracks to return
            include_classics: Whether to include classic hits
        """
        all_tracks = []
        
        # Get mood-based parameters
        genre, mood_tag, era = self._mood_to_music_params(valence, arousal, include_classics)
        
        # Search with genre and mood
        tracks = self.audius.search_tracks(genre=genre, mood=mood_tag, limit=limit//2)
        all_tracks.extend(tracks)
        
        # Get artist-specific recommendations based on mood
        artist_tracks = self._get_artist_recommendations(valence, arousal, include_classics, limit//2)
        all_tracks.extend(artist_tracks)
        
        # If not enough tracks, get trending
        if len(all_tracks) < limit:
            trending = self.audius.get_trending_tracks(genre=genre, limit=limit)
            all_tracks.extend(trending)
        
        # Remove duplicates and limit
        unique_tracks = self._remove_duplicates(all_tracks)[:limit]
        
        return self._format_recommendations(unique_tracks)
    
    def get_trending_recommendations(self, limit: int = 20, 
                                     include_bollywood: bool = True,
                                     include_pop: bool = True) -> List[Dict]:
        """Get trending tracks from Bollywood and Pop genres"""
        all_tracks = []
        
        if include_bollywood:
            # Search for Bollywood/Indian Pop
            bollywood_tracks = self.audius.search_tracks(query='Bollywood Hindi Indian', limit=limit//2)
            all_tracks.extend(bollywood_tracks)
        
        if include_pop:
            # Get Pop trending tracks
            pop_tracks = self.audius.get_trending_tracks(genre='Pop', limit=limit//2)
            all_tracks.extend(pop_tracks)
        
        unique_tracks = self._remove_duplicates(all_tracks)[:limit]
        return self._format_recommendations(unique_tracks)
    
    def get_artist_hits(self, artist_type: str = 'all', limit: int = 20) -> List[Dict]:
        """
        Get hits from specific artist categories
        
        Args:
            artist_type: 'pop', 'bollywood', 'classic', or 'all'
        """
        all_tracks = []
        artists_to_search = []
        
        if artist_type == 'pop' or artist_type == 'all':
            artists_to_search.extend(self.pop_artists[:5])
        
        if artist_type == 'bollywood' or artist_type == 'all':
            artists_to_search.extend(self.bollywood_artists[:5])
        
        if artist_type == 'classic':
            artists_to_search.extend(self.classic_artists[:5])
        
        # Search for each artist
        tracks_per_artist = max(2, limit // len(artists_to_search)) if artists_to_search else limit
        for artist in artists_to_search:
            tracks = self.audius.search_by_artist(artist, limit=tracks_per_artist)
            all_tracks.extend(tracks)
        
        # Sort by popularity and limit
        sorted_tracks = sorted(all_tracks, 
                             key=lambda x: x.get('play_count', 0) + x.get('favorite_count', 0),
                             reverse=True)
        
        unique_tracks = self._remove_duplicates(sorted_tracks)[:limit]
        return self._format_recommendations(unique_tracks)
    
    def _get_artist_recommendations(self, valence: float, arousal: float, 
                                   include_classics: bool, limit: int) -> List[Dict]:
        """Get tracks from artists based on mood"""
        tracks = []
        
        # Select artists based on mood
        if arousal > 0.6 and valence > 0.6:
            # Energetic & Happy - upbeat pop/Bollywood
            artists = self.pop_artists[:3] + self.bollywood_artists[:2]
        elif arousal > 0.6 and valence < 0.4:
            # Energetic & Sad - intense emotional songs
            artists = self.bollywood_artists[:3] + ['Coldplay', 'Adele']
        elif arousal < 0.4 and valence > 0.6:
            # Calm & Happy - soothing pop
            artists = ['Ed Sheeran', 'Arijit Singh', 'Atif Aslam']
        elif arousal < 0.4 and valence < 0.4:
            # Calm & Sad - melancholic ballads
            artists = ['Arijit Singh', 'Ed Sheeran', 'Adele', 'Atif Aslam']
        else:
            # Neutral - mix of popular artists
            artists = self.pop_artists[:2] + self.bollywood_artists[:2]
        
        # Add classics if requested
        if include_classics:
            artists.extend(self.classic_artists[:2])
        
        # Search for tracks from selected artists
        for artist in artists[:5]:
            artist_tracks = self.audius.search_by_artist(artist, limit=2)
            tracks.extend(artist_tracks)
        
        return tracks
    
    def _mood_to_music_params(self, valence: float, arousal: float, 
                              include_classics: bool) -> tuple:
        """Map mood to music parameters with Bollywood/Pop focus"""
        
        if arousal > 0.6 and valence > 0.6:
            return 'Pop', 'energetic', 'modern'
        elif arousal > 0.6 and valence < 0.4:
            return 'Pop', 'intense', 'modern'
        elif arousal < 0.4 and valence > 0.6:
            return 'Pop', 'peaceful', 'classic' if include_classics else 'modern'
        elif arousal < 0.4 and valence < 0.4:
            return 'Pop', 'melancholic', 'classic' if include_classics else 'modern'
        else:
            return 'Pop', 'uplifting', 'modern'
    
    def _remove_duplicates(self, tracks: List[Dict]) -> List[Dict]:
        """Remove duplicate tracks based on track ID"""
        seen_ids = set()
        unique_tracks = []
        
        for track in tracks:
            track_id = track.get('id')
            if track_id and track_id not in seen_ids:
                seen_ids.add(track_id)
                unique_tracks.append(track)
        
        return unique_tracks
    
    def _format_recommendations(self, tracks: List[Dict]) -> List[Dict]:
        """Format track data for consistent output"""
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
                'favorite_count': track.get('favorite_count', 0),
                'release_date': track.get('release_date'),
                'popularity_score': track.get('play_count', 0) + track.get('favorite_count', 0)
            })
        
        # Sort by popularity
        formatted.sort(key=lambda x: x['popularity_score'], reverse=True)
        return formatted
    
    def _get_artwork_url(self, track: Dict) -> Optional[str]:
        """Extract artwork URL from track data"""
        artwork = track.get('artwork', {})
        if artwork:
            return artwork.get('1000x1000') or artwork.get('480x480') or artwork.get('150x150')
        return None


class BasicRecommender:
    """Basic recommender - maintains backward compatibility while using EnhancedRecommender"""
    
    def __init__(self, audius_service: AudiusService):
        self.audius = audius_service
        # Use EnhancedRecommender internally
        self.enhanced = EnhancedRecommender(audius_service)
    
    def get_recommendations_by_mood(self, valence: float, arousal: float, 
                                     limit: int = 20) -> List[Dict]:
        """Backward compatible method - now uses enhanced recommender"""
        return self.enhanced.get_recommendations_by_mood(valence, arousal, limit, include_classics=True)
    
    def _mood_to_music_params(self, valence: float, arousal: float) -> tuple:
        """Legacy method - kept for compatibility"""
        genre, mood_tag, era = self.enhanced._mood_to_music_params(valence, arousal, include_classics=False)
        return genre, mood_tag
    
    def _format_recommendations(self, tracks: List[Dict]) -> List[Dict]:
        """Legacy method - kept for compatibility"""
        return self.enhanced._format_recommendations(tracks)
    
    def _get_artwork_url(self, track: Dict) -> Optional[str]:
        """Legacy method - kept for compatibility"""
        return self.enhanced._get_artwork_url(track)