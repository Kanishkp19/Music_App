import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { User, Settings, History, TrendingUp } from 'lucide-react';
import moodService from '../services/moodService';

const Profile = () => {
  const { user } = useAuth();
  const [moodHistory, setMoodHistory] = useState([]);
  const [preferences, setPreferences] = useState({
    theme: 'light',
    notifications: true,
    autoplay: false
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      loadMoodHistory();
    }
  }, [user]);

  const loadMoodHistory = async () => {
    setLoading(true);
    try {
      const result = await moodService.getMoodHistory();
      setMoodHistory(result.history || []);
    } catch (error) {
      console.error('Failed to load mood history:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <div className="card" style={{ textAlign: 'center' }}>
        <h2>Login Required</h2>
        <p>Please login with Spotify to view your profile.</p>
      </div>
    );
  }

  return (
    <div>
      {/* User Info Card */}
      <div className="card">
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '2rem' }}>
          <div style={{
            width: '80px',
            height: '80px',
            borderRadius: '50%',
            background: 'linear-gradient(45deg, #667eea, #764ba2)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginRight: '1.5rem'
          }}>
            <User size={40} color="white" />
          </div>
          <div>
            <h2 style={{ margin: 0, marginBottom: '0.5rem' }}>
              {user?.display_name || 'MuseAIka User'}
            </h2>
            <p style={{ color: '#666', margin: 0 }}>
              {user?.email || 'user@example.com'}
            </p>
          </div>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '1rem'
        }}>
          <div style={{
            background: 'rgba(102, 126, 234, 0.1)',
            padding: '1rem',
            borderRadius: '8px',
            textAlign: 'center'
          }}>
            <TrendingUp size={24} style={{ color: '#667eea', marginBottom: '0.5rem' }} />
            <h3 style={{ margin: 0, marginBottom: '0.25rem' }}>12</h3>
            <p style={{ margin: 0, color: '#666', fontSize: '0.9rem' }}>
              Mood Detections
            </p>
          </div>
          
          <div style={{
            background: 'rgba(39, 174, 96, 0.1)',
            padding: '1rem',
            borderRadius: '8px',
            textAlign: 'center'
          }}>
            <History size={24} style={{ color: '#27ae60', marginBottom: '0.5rem' }} />
            <h3 style={{ margin: 0, marginBottom: '0.25rem' }}>5</h3>
            <p style={{ margin: 0, color: '#666', fontSize: '0.9rem' }}>
              Playlists Created
            </p>
          </div>
        </div>
      </div>

      {/* Mood History */}
      <div className="card">
        <h3 style={{ marginBottom: '1.5rem' }}>Recent Mood History</h3>
        {loading ? (
          <div className="loading">
            <p>Loading mood history...</p>
          </div>
        ) : moodHistory.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
            <History size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
            <p>No mood history yet. Start by detecting your emotions!</p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {/* Placeholder mood history items */}
            {[
              { mood: 'Happy', confidence: 85, date: '2 hours ago' },
              { mood: 'Calm', confidence: 78, date: '1 day ago' },
              { mood: 'Energetic', confidence: 92, date: '3 days ago' }
            ].map((item, index) => (
              <div
                key={index}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '1rem',
                  background: 'rgba(255, 255, 255, 0.5)',
                  borderRadius: '8px',
                  border: '1px solid rgba(255, 255, 255, 0.3)'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                  <div style={{
                    fontSize: '1.5rem',
                    padding: '0.5rem',
                    background: 'rgba(102, 126, 234, 0.2)',
                    borderRadius: '50%'
                  }}>
                    😊
                  </div>
                  <div>
                    <p style={{ margin: 0, fontWeight: '600' }}>{item.mood}</p>
                    <p style={{ margin: 0, color: '#666', fontSize: '0.9rem' }}>
                      {item.confidence}% confidence
                    </p>
                  </div>
                </div>
                <span style={{ color: '#888', fontSize: '0.9rem' }}>
                  {item.date}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Settings */}
      <div className="card">
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1.5rem' }}>
          <Settings size={24} style={{ marginRight: '0.5rem', color: '#667eea' }} />
          <h3 style={{ margin: 0 }}>Preferences</h3>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            padding: '1rem',
            background: 'rgba(255, 255, 255, 0.5)',
            borderRadius: '8px'
          }}>
            <div>
              <p style={{ margin: 0, fontWeight: '600' }}>Theme</p>
              <p style={{ margin: 0, color: '#666', fontSize: '0.9rem' }}>
                Choose your preferred theme
              </p>
            </div>
            <select
              value={preferences.theme}
              onChange={(e) => setPreferences({...preferences, theme: e.target.value})}
              style={{
                padding: '0.5rem',
                borderRadius: '4px',
                border: '1px solid #ddd'
              }}
            >
              <option value="light">Light</option>
              <option value="dark">Dark</option>
              <option value="auto">Auto</option>
            </select>
          </div>

          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            padding: '1rem',
            background: 'rgba(255, 255, 255, 0.5)',
            borderRadius: '8px'
          }}>
            <div>
              <p style={{ margin: 0, fontWeight: '600' }}>Notifications</p>
              <p style={{ margin: 0, color: '#666', fontSize: '0.9rem' }}>
                Receive mood and playlist updates
              </p>
            </div>
            <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={preferences.notifications}
                onChange={(e) => setPreferences({...preferences, notifications: e.target.checked})}
                style={{ marginRight: '0.5rem' }}
              />
              <span>Enable</span>
            </label>
          </div>

          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            padding: '1rem',
            background: 'rgba(255, 255, 255, 0.5)',
            borderRadius: '8px'
          }}>
            <div>
              <p style={{ margin: 0, fontWeight: '600' }}>Auto-play</p>
              <p style={{ margin: 0, color: '#666', fontSize: '0.9rem' }}>
                Automatically play recommended music
              </p>
            </div>
            <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={preferences.autoplay}
                onChange={(e) => setPreferences({...preferences, autoplay: e.target.checked})}
                style={{ marginRight: '0.5rem' }}
              />
              <span>Enable</span>
            </label>
          </div>
        </div>

        <button 
          className="btn" 
          style={{ marginTop: '1rem', width: '100%' }}
          onClick={() => alert('Settings saved!')}
        >
          Save Preferences
        </button>
      </div>
    </div>
  );
};

export default Profile;
