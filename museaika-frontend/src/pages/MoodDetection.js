import React, { useState } from 'react';
import { Camera, FileText, Upload } from 'lucide-react';
import moodService from '../services/moodService';
import musicService from '../services/musicService';

const MoodDetection = () => {
  const [activeTab, setActiveTab] = useState('image');
  const [imageFile, setImageFile] = useState(null);
  const [textInput, setTextInput] = useState('');
  const [moodResult, setMoodResult] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    setImageFile(file);
  };

  const detectEmotionFromImage = async () => {
    if (!imageFile) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const result = await moodService.detectEmotionFromImage(imageFile);
      setMoodResult(result.data);
      
      // Get music recommendations based on detected mood
      const musicResult = await musicService.getRecommendations(result.data.primary_mood);
      setRecommendations(musicResult.recommendations);
    } catch (error) {
      setError('Failed to detect emotion. Please try again.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const analyzeSentiment = async () => {
    if (!textInput.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const result = await moodService.analyzeSentiment(textInput);
      setMoodResult(result.data);
      
      // Get music recommendations based on detected mood
      const musicResult = await musicService.getRecommendations(result.data.mood_mapping);
      setRecommendations(musicResult.recommendations);
    } catch (error) {
      setError('Failed to analyze sentiment. Please try again.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="card">
        <h2 style={{ marginBottom: '2rem', textAlign: 'center' }}>Mood Detection</h2>
        
        {/* Tab Navigation */}
        <div style={{ 
          display: 'flex', 
          marginBottom: '2rem',
          borderBottom: '1px solid #eee'
        }}>
          <button
            onClick={() => setActiveTab('image')}
            style={{
              flex: 1,
              padding: '1rem',
              border: 'none',
              background: activeTab === 'image' ? '#667eea' : 'transparent',
              color: activeTab === 'image' ? 'white' : '#666',
              cursor: 'pointer',
              borderRadius: '8px 8px 0 0',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem'
            }}
          >
            <Camera size={20} />
            Image Detection
          </button>
          <button
            onClick={() => setActiveTab('text')}
            style={{
              flex: 1,
              padding: '1rem',
              border: 'none',
              background: activeTab === 'text' ? '#667eea' : 'transparent',
              color: activeTab === 'text' ? 'white' : '#666',
              cursor: 'pointer',
              borderRadius: '8px 8px 0 0',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '0.5rem'
            }}
          >
            <FileText size={20} />
            Text Analysis
          </button>
        </div>

        {/* Image Detection Tab */}
        {activeTab === 'image' && (
          <div>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ 
                display: 'block', 
                marginBottom: '0.5rem',
                fontWeight: '600'
              }}>
                Upload an image to detect your emotion:
              </label>
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                style={{
                  width: '100%',
                  padding: '0.5rem',
                  border: '1px solid #ddd',
                  borderRadius: '8px'
                }}
              />
            </div>
            
            {imageFile && (
              <div style={{ 
                marginBottom: '1rem', 
                textAlign: 'center' 
              }}>
                <img
                  src={URL.createObjectURL(imageFile)}
                  alt="Preview"
                  style={{
                    maxWidth: '300px',
                    maxHeight: '300px',
                    borderRadius: '8px',
                    objectFit: 'cover'
                  }}
                />
              </div>
            )}
            
            <button
              onClick={detectEmotionFromImage}
              disabled={!imageFile || loading}
              className="btn"
              style={{
                width: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem'
              }}
            >
              <Upload size={20} />
              {loading ? 'Analyzing...' : 'Detect Emotion'}
            </button>
          </div>
        )}

        {/* Text Analysis Tab */}
        {activeTab === 'text' && (
          <div>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ 
                display: 'block', 
                marginBottom: '0.5rem',
                fontWeight: '600'
              }}>
                Describe how you're feeling:
              </label>
              <textarea
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                placeholder="I'm feeling..."
                rows="4"
                style={{
                  width: '100%',
                  padding: '1rem',
                  border: '1px solid #ddd',
                  borderRadius: '8px',
                  fontSize: '16px',
                  resize: 'vertical'
                }}
              />
            </div>
            
            <button
              onClick={analyzeSentiment}
              disabled={!textInput.trim() || loading}
              className="btn"
              style={{ width: '100%' }}
            >
              {loading ? 'Analyzing...' : 'Analyze Sentiment'}
            </button>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {/* Results Display */}
        {moodResult && (
          <div style={{
            marginTop: '2rem',
            padding: '1.5rem',
            background: 'rgba(102, 126, 234, 0.1)',
            borderRadius: '8px',
            border: '1px solid rgba(102, 126, 234, 0.3)'
          }}>
            <h3 style={{ marginBottom: '1rem' }}>Detected Mood</h3>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div style={{
                fontSize: '2rem',
                padding: '1rem',
                background: 'rgba(102, 126, 234, 0.2)',
                borderRadius: '50%'
              }}>
                😊
              </div>
              <div>
                <p style={{ fontSize: '1.2rem', fontWeight: '600', textTransform: 'capitalize' }}>
                  {moodResult.primary_mood || moodResult.mood_mapping}
                </p>
                <p style={{ color: '#666' }}>
                  Confidence: {Math.round((moodResult.confidence || 0.8) * 100)}%
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Music Recommendations */}
      {recommendations && (
        <div className="card">
          <h3 style={{ marginBottom: '1rem' }}>Recommended Music</h3>
          <p style={{ color: '#666', marginBottom: '1rem' }}>
            Based on your detected mood, here are some music suggestions:
          </p>
          <div style={{ color: '#888' }}>
            <p>🎵 Music recommendations will appear here once integrated with Spotify API</p>
            <p>Detected mood: {moodResult?.primary_mood || moodResult?.mood_mapping}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default MoodDetection;
