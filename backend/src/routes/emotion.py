from flask import Blueprint, request, jsonify
from src.models.mood_entry import MoodEntry
from src.services.emotion_service import EmotionService
from src.utils.helpers import require_auth, map_emotion_to_mood
from src.config import Config

emotion_bp = Blueprint('emotion', __name__, url_prefix='/api/v1/emotion')
emotion_service = None

def init_emotion_service(service: EmotionService):
    global emotion_service
    emotion_service = service

@emotion_bp.route('/analyze/image', methods=['POST'])
@require_auth
def analyze_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        image_bytes = image_file.read()
        result = emotion_service.detect_emotion_from_image(image_bytes)
        mood_entry = MoodEntry.create(
            user_id=request.user_id,
            emotion=result['emotion'],
            valence=result['valence'],
            arousal=result['arousal'],
            source='image',
            confidence=result['confidence']
        )
        return jsonify({'analysis': result, 'mood_entry': mood_entry}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return jsonify({'error': 'Failed to analyze image'}), 500

@emotion_bp.route('/analyze/text', methods=['POST'])
@require_auth
def analyze_text():
    try:
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        result = emotion_service.analyze_text_emotion(text)
        mood_entry = MoodEntry.create(
            user_id=request.user_id,
            emotion=result['emotion'],
            valence=result['valence'],
            arousal=result['arousal'],
            source='text',
            confidence=result['confidence']
        )
        return jsonify({'analysis': result, 'mood_entry': mood_entry}), 200
    except Exception as e:
        print(f"Error analyzing text: {e}")
        return jsonify({'error': 'Failed to analyze text'}), 500

@emotion_bp.route('/manual', methods=['POST'])
@require_auth
def manual_entry():
    try:
        data = request.get_json()
        emotion = data.get('emotion')
        if not emotion:
            return jsonify({'error': 'No emotion provided'}), 400
        mood_coords = map_emotion_to_mood(emotion)
        mood_entry = MoodEntry.create(
            user_id=request.user_id,
            emotion=emotion,
            valence=mood_coords['valence'],
            arousal=mood_coords['arousal'],
            source='manual',
            confidence=1.0
        )
        return jsonify({'mood_entry': mood_entry}), 201
    except Exception as e:
        print(f"Error creating manual entry: {e}")
        return jsonify({'error': 'Failed to save mood'}), 500

@emotion_bp.route('/history', methods=['GET'])
@require_auth
def get_history():
    try:
        limit = request.args.get('limit', 50, type=int)
        history = MoodEntry.get_user_history(request.user_id, limit)
        return jsonify({'history': history}), 200
    except Exception as e:
        print(f"Error fetching history: {e}")
        return jsonify({'error': 'Failed to fetch history'}), 500

@emotion_bp.route('/current', methods=['GET'])
@require_auth
def get_current():
    try:
        mood = MoodEntry.get_latest(request.user_id)
        if not mood:
            return jsonify({'mood': None}), 200
        return jsonify({'mood': mood}), 200
    except Exception as e:
        print(f"Error fetching current mood: {e}")
        return jsonify({'error': 'Failed to fetch mood'}), 500
