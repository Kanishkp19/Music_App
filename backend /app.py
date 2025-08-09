"""Flask application factory for MuseAIka backend"""
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Initialize SocketIO
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.music_routes import music_bp
    from routes.mood_routes import mood_bp
    from routes.user_routes import user_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(music_bp, url_prefix='/api/v1')
    app.register_blueprint(mood_bp, url_prefix='/api/v1')
    app.register_blueprint(user_bp, url_prefix='/api/v1')
    
    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()
    socketio.run(app, debug=True, host='0.0.0.0', port=8000)
