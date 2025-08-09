"""Mood detection route handlers"""
from flask import Blueprint, request, jsonify
from modules.emotion_detection import EmotionDetector
from modules.sentiment_analysis import SentimentAnalyzer

mood_bp = Blueprint('mood', __name__)

@mood_bp.route('/detect/emotion', methods=['POST'])
def detect_emotion():
    """Detect emotion from uploaded image"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image = request.files['image']
    detector = EmotionDetector()
    
    # TODO: Process image and detect emotions
    result = detector.detect_from_image(image.read())
    return jsonify({'success': True, 'data': result})

@mood_bp.route('/detect/sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyze sentiment from text"""
    data = request.get_json()
    text = data.get('text', '')
    
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_text(text)
    
    return jsonify({'success': True, 'data': result})

@mood_bp.route('/detect/history')
def get_mood_history():
    """Get user's mood history"""
    # TODO: Get mood history from database
    return jsonify({'history': []})
