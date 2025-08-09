# MuseAIka Backend Deployment Guide

## Development Setup

1. **Clone and Setup**
```bash
git clone <repository-url>
cd museaika-backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Start Services**
```bash
docker-compose up -d  # Start MongoDB, Redis, MinIO
python scripts/init_db.py  # Initialize database
```

5. **Run Development Server**
```bash
python app.py
# or
flask run --host=0.0.0.0 --port=8000 --debug
```

## Production Deployment

### Option 1: Docker Compose
```bash
# Build and run with production settings
docker-compose -f docker-compose.prod.yml up --build -d
```

### Option 2: Manual Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=production
export MONGO_URI=your_production_mongo_uri
export REDIS_URL=your_production_redis_url

# Run with Gunicorn
gunicorn --worker-class eventlet -w 4 --bind 0.0.0.0:8000 wsgi:app
```

### Option 3: Kubernetes
```bash
# Apply Kubernetes manifests (create these based on your needs)
kubectl apply -f k8s/
```

## Environment Variables

Required for production:
```bash
FLASK_ENV=production
SECRET_KEY=your-super-secret-key
MONGO_URI=mongodb://user:pass@host:port/database
REDIS_URL=redis://user:pass@host:port/db
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

## Health Checks

- **Endpoint**: `GET /api/v1/health`
- **Expected Response**: `{"status": "healthy", "service": "museaika-backend"}`

## Monitoring

1. **Application Logs**
```bash
# View logs
docker-compose logs -f app
```

2. **Database Monitoring**
```bash
# MongoDB stats
docker exec -it mongo_container mongo --eval "db.stats()"
```

3. **Redis Monitoring**
```bash
# Redis info
docker exec -it redis_container redis-cli info
```

## Scaling

### Horizontal Scaling
- Run multiple app instances behind a load balancer
- Ensure session data is stored in Redis, not memory
- Use external services for MongoDB and Redis

### Vertical Scaling
- Increase CPU/Memory allocation
- Optimize database indexes
- Implement caching strategies

## Security Checklist

- [ ] Change default secrets and keys
- [ ] Enable HTTPS in production
- [ ] Implement rate limiting
- [ ] Validate all inputs
- [ ] Use secure headers
- [ ] Regular security audits with `bandit`

## Backup Strategy

1. **Database Backups**
```bash
# MongoDB backup
docker exec mongo_container mongodump --out /backup
```

2. **Redis Persistence**
```bash
# Ensure Redis persistence is enabled
CONFIG SET save "900 1 300 10 60 10000"
```

## Troubleshooting

### Common Issues

1. **Import Errors**
- Ensure virtual environment is activated
- Check Python path and module installations

2. **Database Connection Issues**
- Verify MongoDB is running and accessible
- Check connection string format

3. **WebSocket Issues**
- Ensure eventlet is installed
- Check CORS configuration

4. **Permission Errors**
- Check file permissions for uploads directory
- Ensure proper user permissions in Docker
