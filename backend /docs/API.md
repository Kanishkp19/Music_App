# MuseAIka Backend API Documentation

## Authentication Endpoints

### POST /api/v1/auth/spotify/login
Initiates Spotify OAuth flow
- **Response**: `{"auth_url": "https://accounts.spotify.com/authorize..."}`

### GET /api/v1/auth/spotify/callback
Handles Spotify OAuth callback
- **Parameters**: `code`, `state`
- **Response**: `{"success": true, "user": {...}}`

### GET /api/v1/auth/me
Get current authenticated user
- **Response**: `{"user": {...}}`

### POST /api/v1/auth/logout
Logout current user
- **Response**: `{"success": true}`

## Mood Detection Endpoints

### POST /api/v1/detect/emotion
Detect emotions from uploaded image
- **Content-Type**: `multipart/form-data`
- **Body**: `image` (file)
- **Response**: 
```json
{
  "success": true,
  "data": {
    "primary_mood": "happy",
    "confidence": 0.85,
    "emotions": {"happy": 0.85, "neutral": 0.15}
  }
}
```

### POST /api/v1/detect/sentiment
Analyze sentiment from text
- **Content-Type**: `application/json`
- **Body**: `{"text": "I feel great today!"}`
- **Response**:
```json
{
  "success": true,
  "data": {
    "sentiment": "positive",
    "confidence": 0.8,
    "mood_mapping": "happy"
  }
}
```

### GET /api/v1/detect/history
Get user's mood detection history
- **Response**: `{"history": [...]}`

## Music Endpoints

### GET /api/v1/recommendations
Get mood-based music recommendations
- **Parameters**: `mood` (string), `limit` (int, default: 20)
- **Response**: `{"recommendations": [...]}`

### GET /api/v1/playlists
Get user's playlists
- **Response**: `{"playlists": [...]}`

### POST /api/v1/playlists
Create new playlist
- **Body**: `{"title": "My Playlist", "tracks": [...]}`
- **Response**: `{"success": true, "playlist_id": "..."}`

### POST /api/v1/generate
Start music generation
- **Body**: `{"mood": "happy", "tempo": 120, "length": 30}`
- **Response**: `{"job_id": "...", "status": "queued"}`

### GET /api/v1/generate/{job_id}
Get music generation status
- **Response**: `{"status": "completed", "download_url": "..."}`

## User Endpoints

### GET /api/v1/profile
Get user profile
- **Response**: `{"profile": {...}}`

### GET /api/v1/preferences
Get user preferences
- **Response**: `{"preferences": {...}}`

### PUT /api/v1/preferences
Update user preferences
- **Body**: `{"theme": "dark", "notifications": true}`
- **Response**: `{"success": true}`

### GET /api/v1/health
Health check endpoint
- **Response**: `{"status": "healthy", "service": "museaika-backend"}`

## WebSocket Events

### Namespace: `/realtime`

#### Client → Server Events
- `subscribe_mood`: Subscribe to mood updates for a user
- `playlist_edit`: Edit playlist collaboratively

#### Server → Client Events  
- `mood_update`: Real-time mood detection updates
- `playlist_update`: Real-time playlist changes
- `subscribed`: Confirmation of subscription

## Error Responses

All endpoints return errors in the format:
```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {...}
}
```

Common HTTP status codes:
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error
