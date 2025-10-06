from flask import Blueprint, request, jsonify
from src.services.audius_service import AudiusService
from src.services.recommender import BasicRecommender
from src.models.mood_entry import MoodEntry
from src.utils.helpers import require_auth

music_bp = Blueprint('music', __name__, url_prefix='/api/v1/music')
audius_service = None
recommender = None

def init_music_services(audius: AudiusService, rec: BasicRecommender):
    global audius_service, recommender
    audius_service = audius
    recommender = rec

@music_bp.route('/search', methods=['GET'])
@require_auth
def search_tracks():
    try:
        query = request.args.get('query')
        genre = request.args.get('genre')
        limit = request.args.get('limit', 20, type=int)
        tracks = audius_service.search_tracks(query=query, genre=genre, limit=limit)
        return jsonify({'tracks': tracks}), 200
    except Exception as e:
        print(f"Error searching tracks: {e}")
        return jsonify({'error': 'Failed to search tracks'}), 500

@music_bp.route('/trending', methods=['GET'])
@require_auth
def get_trending():
    try:
        genre = request.args.get('genre')
        limit = request.args.get('limit', 20, type=int)
        tracks = audius_service.get_trending_tracks(genre=genre, limit=limit)
        return jsonify({'tracks': tracks}), 200
    except Exception as e:
        print(f"Error getting trending: {e}")
        return jsonify({'error': 'Failed to get trending tracks'}), 500

@music_bp.route('/track/<track_id>', methods=['GET'])
@require_auth
def get_track(track_id):
    try:
        track = audius_service.get_track(track_id)
        if not track:
            return jsonify({'error': 'Track not found'}), 404
        return jsonify({'track': track}), 200
    except Exception as e:
        print(f"Error getting track: {e}")
        return jsonify({'error': 'Failed to get track'}), 500

@music_bp.route('/recommend', methods=['GET'])
@require_auth
def get_recommendations():
    try:
        mood = MoodEntry.get_latest(request.user_id)
        if not mood:
            valence = 0.5
            arousal = 0.5
        else:
            valence = mood['valence']
            arousal = mood['arousal']
        limit = request.args.get('limit', 20, type=int)
        recommendations = recommender.get_recommendations_by_mood(
            valence=valence, arousal=arousal, limit=limit
        )
        return jsonify({'recommendations': recommendations, 'based_on_mood': mood}), 200
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return jsonify({'error': 'Failed to get recommendations'}), 500

@music_bp.route('/recommend/custom', methods=['POST'])
@require_auth
def get_custom_recommendations():
    try:
        data = request.get_json()
        valence = data.get('valence', 0.5)
        arousal = data.get('arousal', 0.5)
        limit = data.get('limit', 20)
        recommendations = recommender.get_recommendations_by_mood(
            valence=valence, arousal=arousal, limit=limit
        )
        return jsonify({'recommendations': recommendations}), 200
    except Exception as e:
        print(f"Error getting custom recommendations: {e}")
        return jsonify({'error': 'Failed to get recommendations'}), 500
