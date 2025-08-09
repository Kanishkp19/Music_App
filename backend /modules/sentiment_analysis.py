from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        self.classifier = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
    
    def analyze_text(self, text: str) -> Dict:
        result = self.classifier(text)[0]
        
        # Map sentiment to mood
        mood_mapping = {
            'POSITIVE': 'happy',
            'NEGATIVE': 'sad',
            'NEUTRAL': 'neutral'
        }
        
        return {
            'sentiment': result['label'].lower(),
            'confidence': result['score'],
            'mood_mapping': mood_mapping.get(result['label'], 'neutral')
        }