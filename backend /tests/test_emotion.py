"""Tests for emotion detection module"""
import pytest
from modules.emotion_detection import EmotionDetector

def test_emotion_detector_init():
    """Test EmotionDetector initialization"""
    detector = EmotionDetector()
    assert len(detector.emotions) == 7
    assert 'happy' in detector.emotions

def test_detect_from_image():
    """Test emotion detection from image"""
    detector = EmotionDetector()
    result = detector.detect_from_image(b"fake_image_data")
    
    assert 'primary_mood' in result
    assert 'confidence' in result
    assert 'emotions' in result
