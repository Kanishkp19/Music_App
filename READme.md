# MuseAIka 🎵🎭

**AI-Powered Emotion-Based Music Discovery & Generation Platform**

MuseAIka is a multi-page web application that analyzes user emotions through facial expressions, text, or manual input to recommend and generate personalized music experiences in real-time.

---

## 🌟 Features

### Core Features
- **Real-time Mood Detection**: Webcam-based emotion analysis using computer vision
- **Emotion Analysis**: Analyze mood from uploaded images or text input
- **Smart Music Recommendations**: Hybrid recommender system based on mood (valence/arousal)
- **AI Music Generation**: Generate original tracks using Magenta/TensorFlow based on your mood
- **Collaborative Playlists**: Real-time playlist editing with friends via WebSocket
- **Multi-source Music Integration**: Primary Audius API with Last.fm metadata enrichment

### Privacy-First Design
- Client-side face preprocessing
- Immediate frame deletion after analysis
- Explicit user consent for webcam access
- No persistent storage of facial images

---

## 🏗️ Architecture

### Tech Stack

**Frontend**
- React 18 with React Router (multi-page SPA)
- Material-UI (MUI) for components
- Chart.js for mood visualization
- Socket.IO client for real-time features
- Axios for HTTP requests

**Backend**
- Flask (Python 3.10+)
- Flask-SocketIO for WebSocket support
- MongoDB for data persistence
- Redis for caching and pub/sub
- Celery for async task processing
- Mistral AI for LLM-based features

**AI/ML**
- OpenCV for face detection
- Hugging Face Transformers (emotion classification)
- Magenta/TensorFlow for music generation
- Mistral LLM for conversational features

**Music APIs**
- **Primary**: Audius (open, free streaming API)
- **Metadata**: Last.fm (track similarity, artist info)
- **Fallback**: YouTube IFrame Player API

---

## 📁 Project Structure

```
museaika/
├── backend/                 # Flask application
│   ├── src/
│   │   ├── app.py          # Main Flask app + SocketIO
│   │   ├── config.py       # Configuration
│   │   ├── blueprints/     # Route blueprints
│   │   ├── services/       # External API clients
│   │   ├── ml/             # ML model wrappers
│   │   ├── models/         # MongoDB models
│   │   ├── utils/          # Helper functions
│   │   └── tasks/          # Celery tasks
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/               # React application
│   ├── src/
│   │   ├── App.jsx        # Router setup
│   │   ├── routes/        # Page components
│   │   ├── components/    # Reusable components
│   │   ├── services/      # API & Socket clients
│   │   ├── store/         # State management
│   │   ├── hooks/         # Custom React hooks
│   │   └── utils/         # Helper functions
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml      # Local development setup
└── k8s/                    # Kubernetes configs
```

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend dev)
- Python 3.10+ (for local backend dev)
- API Keys:
  - Audius API key (free at docs.audius.org)
  - Last.fm API key
  - Mistral API key
  - (Optional) YouTube Data API key

### Quick Start with Docker

1. **Clone the repository**
```bash
git clone <repository-url>
cd museaika
```

2. **Set up environment variables**
```bash
# Backend .env
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- MongoDB: localhost:27017
- Redis: localhost:6379

### Local Development Setup

**Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/app.py
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

---

## 🔑 Environment Variables

### Backend (.env)
```env
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret

# Database
MONGODB_URI=mongodb://localhost:27017/museaika
REDIS_URL=redis://localhost:6379/0

# APIs
AUDIUS_API_KEY=your-audius-key
LASTFM_API_KEY=your-lastfm-key
MISTRAL_API_KEY=your-mistral-key
YOUTUBE_API_KEY=your-youtube-key (optional)

# Storage
S3_BUCKET=museaika-storage
S3_REGION=us-east-1
AWS_ACCESS_KEY=your-aws-key
AWS_SECRET_KEY=your-aws-secret

# ML Models
EMOTION_MODEL=facebook/detr-resnet-50-fer2013
HF_TOKEN=your-huggingface-token (if using private models)

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:5000
VITE_WS_URL=ws://localhost:5000
```

---

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login (returns JWT)
- `POST /api/v1/auth/logout` - Logout
- `GET /api/v1/auth/me` - Get current user

### Emotion Analysis
- `POST /api/v1/emotion/analyze` - Analyze emotion from image/text
- `POST /api/v1/emotion/manual` - Submit manual mood entry
- `GET /api/v1/emotion/history` - Get user's mood history

### Music
- `GET /api/v1/music/search` - Search tracks (proxies to Audius)
- `GET /api/v1/music/track/:id` - Get track details
- `GET /api/v1/music/stream/:id` - Get streaming URL

### Recommendations
- `GET /api/v1/recommender/by-mood` - Get tracks by mood parameters
- `POST /api/v1/recommender/feedback` - Submit user feedback
- `GET /api/v1/recommender/similar/:trackId` - Get similar tracks

### Music Generation
- `POST /api/v1/generate` - Start generation job
- `GET /api/v1/generate/:jobId` - Get generation status
- `GET /api/v1/generate/:jobId/download` - Download generated track

### Playlists
- `GET /api/v1/playlists` - List user playlists
- `POST /api/v1/playlists` - Create playlist
- `GET /api/v1/playlists/:id` - Get playlist details
- `PUT /api/v1/playlists/:id` - Update playlist
- `DELETE /api/v1/playlists/:id` - Delete playlist
- `POST /api/v1/playlists/:id/tracks` - Add track to playlist
- `DELETE /api/v1/playlists/:id/tracks/:trackId` - Remove track

### WebSocket Events
- **Namespace**: `/mood`
  - `connect` - Client connects
  - `frame` (client→server) - Send video frame
  - `mood_update` (server→client) - Receive mood analysis
  - `disconnect` - Client disconnects

- **Namespace**: `/collab`
  - `join_playlist` - Join playlist room
  - `playlist_update` - Broadcast playlist changes
  - `leave_playlist` - Leave playlist room

---

## 🎨 Frontend Pages

1. **Home** (`/`) - Landing page with quick mood snapshot
2. **Mood Check** (`/mood-check`) - Upload image or text for analysis
3. **Live Mood** (`/live-mood`) - Real-time webcam emotion tracking
4. **Recommender** (`/recommender`) - Browse mood-based recommendations
5. **Generator** (`/generator`) - Generate custom AI music
6. **Library** (`/library`) - User's saved tracks and playlists
7. **Playlists** (`/playlists/:id`) - Collaborative playlist editor
8. **Profile** (`/profile`) - User settings and privacy controls

---

## 🧠 ML Models & Data Flow

### Emotion Detection Pipeline
1. Frontend captures webcam frame (160x120 JPEG, ~1 FPS)
2. Client sends compressed frame via WebSocket
3. Backend runs OpenCV face detection
4. Hugging Face model classifies emotion
5. Maps emotion to valence/arousal coordinates
6. Returns: `{emotion: "happy", valence: 0.8, arousal: 0.6}`

### Music Recommendation Pipeline
1. Receive mood vector (valence, arousal)
2. Map to music features (tempo, energy, danceability)
3. Query Audius API with filters
4. Enrich with Last.fm similarity data
5. Hybrid ranking (content + collaborative filtering)
6. Return top 20 tracks

### Music Generation Pipeline
1. User inputs mood + preferences (tempo, length, style)
2. Generate MIDI using Magenta MelodyRNN
3. Convert MIDI→WAV using FluidSynth
4. Normalize audio and upload to S3
5. Store metadata in MongoDB
6. Return download URL to client

---

## 🔒 Security & Privacy

### Data Protection
- JWT authentication with httpOnly cookies
- Password hashing with bcrypt
- Rate limiting on all endpoints
- CORS configuration for allowed origins
- Input validation and sanitization

### Privacy Measures
- Explicit consent before webcam access
- No persistent storage of facial images
- Frames deleted immediately after analysis
- Option to use text-based mood input instead
- User data deletion on request (GDPR compliant)

### Secrets Management
- Environment variables for sensitive data
- Kubernetes Secrets in production
- API keys never exposed to client

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test                    # Unit tests
npm run test:e2e           # Cypress E2E tests
```

---

## 📊 Monitoring & Logging

- **Application Logs**: Structured JSON logging via Python logging
- **Error Tracking**: Sentry integration
- **Metrics**: Prometheus + Grafana dashboards
- **Uptime**: Health check endpoint at `/api/health`

---

## 🚢 Deployment

### Production with Kubernetes

```bash
# Build and push images
docker build -t museaika-backend:latest ./backend
docker build -t museaika-frontend:latest ./frontend
docker push <your-registry>/museaika-backend:latest
docker push <your-registry>/museaika-frontend:latest

# Deploy to K8s
kubectl apply -f k8s/
```

### Environment-Specific Configs
- Development: `docker-compose.yml`
- Staging: `k8s/staging/`
- Production: `k8s/production/`

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Backend: Black formatter, flake8 linting
- Frontend: ESLint + Prettier

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- **Audius** for open music streaming API
- **Last.fm** for music metadata
- **Magenta** for music generation models
- **Hugging Face** for emotion recognition models
- **Mistral AI** for LLM capabilities

---

## 📧 Support

- Documentation: [Wiki](wiki-url)
- Issues: [GitHub Issues](issues-url)
- Email: support@museaika.com

---

## 🗺️ Roadmap

### MVP (Current)
- ✅ Basic emotion analysis
- ✅ Audius integration
- ✅ Simple recommendations
- ✅ Real-time mood tracking

### v1.0 (Next 2 months)
- [ ] Collaborative playlists
- [ ] Advanced hybrid recommender
- [ ] Lyrics integration (Musixmatch)
- [ ] Mobile responsive design
- [ ] User onboarding flow

### v1.5 (Future)
- [ ] Social features (share moods/playlists)
- [ ] Advanced music generation (style transfer)
- [ ] Voice-based mood input
- [ ] Spotify/Apple Music integration
- [ ] Mobile apps (React Native)

---

**Built with ❤️ and AI**