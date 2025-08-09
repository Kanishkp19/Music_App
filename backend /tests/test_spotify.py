"""Tests for Spotify service"""
import pytest
from modules.spotify_service import SpotifyService

def test_spotify_service_init():
    """Test SpotifyService initialization"""
    service = SpotifyService("client_id", "client_secret", "redirect_uri")
    assert service.client_id == "client_id"
    assert service.client_secret == "client_secret"

def test_get_recommendations():
    """Test getting recommendations"""
    service = SpotifyService("test", "test", "test")
    recommendations = service.get_recommendations("happy")
    assert isinstance(recommendations, list)
