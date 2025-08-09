import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { Music, Heart, Headphones, Sparkles } from 'lucide-react';
import api from '../services/api';

const Home = () => {
  const { user } = useAuth();
  const [healthStatus, setHealthStatus] = useState(null);

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const response = await api.get('/health');
      setHealthStatus(response.data);
    } catch (error) {
      setHealthStatus({ status: 'error', message: 'Backend not connected' });
    }
  };

  return (
    <div>
      <div className="card" style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1 style={{ 
          fontSize: '3rem', 
          marginBottom: '1rem',
          background: 'linear-gradient(45deg, #667eea, #764ba2)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text'
        }}>
          Welcome to MuseAIka
        </h1>
        <p style={{ fontSize: '1.2rem', color: '#666', marginBottom: '2rem' }}>
          Emotion-driven music recommendations powered by AI
        </p>
        
        {healthStatus && (
          <div style={{
            padding: '1rem',
            borderRadius: '8px',
            marginBottom: '2rem',
            background: healthStatus.status === 'healthy' 
              ? 'rgba(39, 174, 96, 0.1)' 
              : 'rgba(231, 76, 60, 0.1)',
            border: `1px solid ${healthStatus.status === 'healthy' ? '#27ae60' : '#e74c3c'}`
          }}>
            Backend Status: {healthStatus.status === 'healthy' ? '✅ Connected' : '❌ Disconnected'}
          </div>
        )}

        {!user && (
          <p style={{ color: '#888' }}>
            Please login with Spotify to access all features
          </p>
        )}
      </div>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
        gap: '2rem' 
      }}>
        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1rem' }}>
            <Heart size={24} style={{ marginRight: '0.5rem', color: '#e74c3c' }} />
            <h3>Emotion Detection</h3>
          </div>
          <p>Upload a photo or describe your feelings to detect your current mood</p>
        </div>

        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1rem' }}>
            <Headphones size={24} style={{ marginRight: '0.5rem', color: '#3498db' }} />
            <h3>Smart Recommendations</h3>
          </div>
          <p>Get personalized music recommendations based on your detected emotions</p>
        </div>

        <div className="card">
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1rem' }}>
            <Sparkles size={24} style={{ marginRight: '0.5rem', color: '#f39c12' }} />
            <h3>AI Music Generation</h3>
          </div>
          <p>Generate unique music compositions tailored to your mood</p>
        </div>
      </div>
    </div>
  );
};

export default Home;
