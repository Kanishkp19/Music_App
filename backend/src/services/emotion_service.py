import cv2
import numpy as np
from PIL import Image
from transformers import pipeline
from src.utils.helpers import map_emotion_to_mood

class EmotionService:
    def __init__(self, model_name: str):
        self.classifier = pipeline("image-classification", model=model_name)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    def detect_emotion_from_image(self, image_bytes: bytes) -> dict:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Invalid image")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) == 0:
            raise ValueError("No face detected in image")
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        face_img = img[y:y+h, x:x+w]
        face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(face_rgb)
        results = self.classifier(pil_img)
        top_emotion = results[0]
        emotion = top_emotion['label'].lower()
        confidence = top_emotion['score']
        mood_coords = map_emotion_to_mood(emotion)
        return {
            'emotion': emotion,
            'confidence': confidence,
            'valence': mood_coords['valence'],
            'arousal': mood_coords['arousal'],
            'all_emotions': results
        }
    
    def analyze_text_emotion(self, text: str) -> dict:
        text_lower = text.lower()
        emotion_keywords = {
            'happy': ['happy', 'joy', 'excited', 'great', 'wonderful', 'love'],
            'sad': ['sad', 'unhappy', 'down', 'depressed', 'miserable'],
            'angry': ['angry', 'mad', 'furious', 'annoyed', 'frustrated'],
            'calm': ['calm', 'peaceful', 'relaxed', 'serene'],
            'anxious': ['anxious', 'worried', 'nervous', 'stressed']
        }
        detected_emotion = 'neutral'
        max_matches = 0
        for emotion, keywords in emotion_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            if matches > max_matches:
                max_matches = matches
                detected_emotion = emotion
        mood_coords = map_emotion_to_mood(detected_emotion)
        confidence = min(0.5 + (max_matches * 0.1), 0.95)
        return {
            'emotion': detected_emotion,
            'confidence': confidence,
            'valence': mood_coords['valence'],
            'arousal': mood_coords['arousal']
        }
