from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from src.config import Config
from src.utils.db import init_db
from src.services.emotion_service import EmotionService
from src.services.audius_service import AudiusService
from src.services.recommender import BasicRecommender, EnhancedRecommender
from src.services.music_generator import MusicGenerator
from src.routes.auth import auth_bp
from src.routes.emotion import emotion_bp, init_emotion_service
from src.routes.music import music_bp, init_music_services
from src.routes.generator import generator_bp, init_generator_service
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app, origins=config_class.CORS_ORIGINS, supports_credentials=True)

    # Initialize MongoDB
    init_db(app.config['MONGODB_URI'])

    # Initialize services
    emotion_service = EmotionService(app.config['EMOTION_MODEL'])
    audius_service = AudiusService(app.config['AUDIUS_HOST'], app.config['AUDIUS_API_KEY'])
    
    # Initialize both recommenders
    # BasicRecommender now uses EnhancedRecommender internally for backward compatibility
    recommender = BasicRecommender(audius_service)
    enhanced_recommender = EnhancedRecommender(audius_service)
    
    music_generator = MusicGenerator(os.path.join(app.root_path, '..', app.config['GENERATION_OUTPUT_DIR']))

    # Initialize routes/services
    init_emotion_service(emotion_service)
    # Pass both recommenders to music routes
    init_music_services(audius_service, recommender, enhanced_recommender)
    init_generator_service(music_generator)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(emotion_bp)
    app.register_blueprint(music_bp)
    app.register_blueprint(generator_bp)

    # Root route
    @app.route('/')
    def home():
        return jsonify({
            'message': 'Welcome to MuseAIka Backend!',
            'version': '2.0.0',
            'features': [
                'Emotion-based music recommendations',
                'Bollywood & International Pop focus',
                'Trending songs from top artists',
                'Classic hits collection',
                'AI music generation'
            ]
        }), 200

    # Health check
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy', 
            'service': 'MuseAIka Backend', 
            'version': '2.0.0',
            'recommender': 'Enhanced with Bollywood & Pop focus'
        }), 200

    # Favicon route
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico', 
            mimetype='image/vnd.microsoft.icon'
        )

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)