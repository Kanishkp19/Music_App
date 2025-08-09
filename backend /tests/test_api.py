"""API endpoint tests"""
import pytest
import json

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_emotion_detection_no_image(client):
    """Test emotion detection without image"""
    response = client.post('/api/v1/detect/emotion')
    assert response.status_code == 400

def test_sentiment_analysis(client):
    """Test sentiment analysis endpoint"""
    response = client.post('/api/v1/detect/sentiment',
                          json={'text': 'I feel happy today'})
    assert response.status_code == 200
