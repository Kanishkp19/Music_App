import cv2
import numpy as np
from tensorflow.keras.models import load_model

class EmotionDetector:
    def __init__(self):
        # Load your trained emotion detection model
        self.model = load_model('path/to/emotion_model.h5')
        self.emotions = ['happy', 'sad', 'angry', 'neutral', 'surprise', 'fear', 'disgust']
    
    def detect_from_image(self, image_data: bytes) -> Dict:
        # Preprocess image
        image = self.preprocess_image(image_data)
        
        # Run inference
        predictions = self.model.predict(image)
        emotion_idx = np.argmax(predictions)
        confidence = float(predictions[0][emotion_idx])
        
        return {
            'primary_mood': self.emotions[emotion_idx],
            'confidence': confidence,
            'emotions': {
                emotion: float(pred) 
                for emotion, pred in zip(self.emotions, predictions[0])
            }
        }