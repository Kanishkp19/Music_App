"""Real-time mood updates via WebSocket"""
from flask_socketio import SocketIO, emit, join_room, leave_room

class MoodSocketManager:
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup WebSocket event handlers"""
        
        @self.socketio.on('subscribe_mood', namespace='/realtime')
        def handle_subscribe_mood(data):
            user_id = data.get('user_id')
            join_room(f"user_{user_id}", namespace='/realtime')
            emit('subscribed', {'user_id': user_id})
        
        @self.socketio.on('playlist_edit', namespace='/realtime')
        def handle_playlist_edit(data):
            # TODO: Handle collaborative playlist editing
            emit('playlist_update', data, broadcast=True)
    
    def broadcast_mood_update(self, user_id: str, mood_data: dict):
        """Broadcast mood update to subscribed clients"""
        self.socketio.emit('mood_update', mood_data, 
                          room=f"user_{user_id}", namespace='/realtime')
