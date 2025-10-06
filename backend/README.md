# MuseAIka Backend

AI-powered emotion detection and music recommendation API

## Features
- User authentication (JWT)
- Emotion detection from images (facial recognition)
- Text-based emotion analysis
- Music recommendations based on mood
- Integration with Audius music platform
- MongoDB for data persistence

## Setup

### Prerequisites
- Python 3.8+
- MongoDB
- pip

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user (requires auth)

### Emotion Detection
- `POST /api/v1/emotion/analyze/image` - Analyze emotion from image
- `POST /api/v1/emotion/analyze/text` - Analyze emotion from text
- `POST /api/v1/emotion/manual` - Manual mood entry
- `GET /api/v1/emotion/history` - Get mood history
- `GET /api/v1/emotion/current` - Get current mood

### Music
- `GET /api/v1/music/search` - Search tracks
- `GET /api/v1/music/trending` - Get trending tracks
- `GET /api/v1/music/track/:id` - Get track details
- `GET /api/v1/music/recommend` - Get mood-based recommendations
- `POST /api/v1/music/recommend/custom` - Custom mood recommendations

## Project Structure
```
backend/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── app.py
│   ├── models/
│   │   ├── user.py
│   │   └── mood_entry.py
│   ├── services/
│   │   ├── emotion_service.py
│   │   ├── audius_service.py
│   │   └── recommender.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── emotion.py
│   │   └── music.py
│   └── utils/
│       ├── db.py
│       └── helpers.py
├── run.py
├── requirements.txt
└── .env
```

## Development
Run in debug mode:
```bash
FLASK_ENV=development python run.py
```
