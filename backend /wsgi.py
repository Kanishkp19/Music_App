"""WSGI entry point for production deployment"""
from app import create_app

app, socketio = create_app('production')

if __name__ == "__main__":
    socketio.run(app)
