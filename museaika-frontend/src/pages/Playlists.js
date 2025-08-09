import React, { useState, useEffect } from 'react';
import { Plus, Music, Play } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import musicService from '../services/musicService';

const Playlists = () => {
  const { user } = useAuth();
  const [playlists, setPlaylists] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newPlaylistTitle, setNewPlaylistTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (user) {
      loadPlaylists();
    }
  }, [user]);

  const loadPlaylists = async () => {
    setLoading(true);
    try {
      const result = await musicService.getPlaylists();
      setPlaylists(result.playlists || []);
    } catch (error) {
      setError('Failed to load playlists');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const createPlaylist = async () => {
    if (!newPlaylistTitle.trim()) return;

    setLoading(true);
    try {
      await musicService.createPlaylist(newPlaylistTitle);
      setNewPlaylistTitle('');
      setShowCreateForm(false);
      loadPlaylists();
    } catch (error) {
      setError('Failed to create playlist');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <div className="card" style={{ textAlign: 'center' }}>
        <h2>Login Required</h2>
        <p>Please login with Spotify to view your playlists.</p>
      </div>
    );
  }

  return (
    <div>
      <div className="card">
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: '2rem'
        }}>
          <h2>Your Playlists</h2>
          <button
            onClick={() => setShowCreateForm(true)}
            className="btn"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}
          >
            <Plus size={20} />
            Create Playlist
          </button>
        </div>

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {showCreateForm && (
          <div style={{
            background: 'rgba(102, 126, 234, 0.1)',
            padding: '1.5rem',
            borderRadius: '8px',
            marginBottom: '2rem'
          }}>
            <h3 style={{ marginBottom: '1rem' }}>Create New Playlist</h3>
            <input
              type="text"
              value={newPlaylistTitle}
              onChange={(e) => setNewPlaylistTitle(e.target.value)}
              placeholder="Playlist title..."
              style={{
                width: '100%',
                padding: '0.75rem',
                border: '1px solid #ddd',
                borderRadius: '8px',
                marginBottom: '1rem',
                fontSize: '16px'
              }}
            />
            <div style={{ display: 'flex', gap: '1rem' }}>
              <button
                onClick={createPlaylist}
                disabled={!newPlaylistTitle.trim() || loading}
                className="btn"
              >
                {loading ? 'Creating...' : 'Create'}
              </button>
              <button
                onClick={() => {
                  setShowCreateForm(false);
                  setNewPlaylistTitle('');
                }}
                className="btn btn-secondary"
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        {loading && !showCreateForm ? (
          <div className="loading">
            <p>Loading playlists...</p>
          </div>
        ) : (
          <div>
            {playlists.length === 0 ? (
              <div style={{ 
                textAlign: 'center', 
                padding: '3rem',
                color: '#666'
              }}>
                <Music size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
                <p>No playlists yet. Create your first playlist!</p>
              </div>
            ) : (
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
                gap: '1.5rem'
              }}>
                {playlists.map((playlist, index) => (
                  <div
                    key={index}
                    style={{
                      background: 'rgba(255, 255, 255, 0.5)',
                      padding: '1.5rem',
                      borderRadius: '12px',
                      border: '1px solid rgba(255, 255, 255, 0.3)',
                      transition: 'transform 0.2s ease',
                      cursor: 'pointer'
                    }}
                    onMouseEnter={(e) => {
                      e.target.style.transform = 'translateY(-2px)';
                    }}
                    onMouseLeave={(e) => {
                      e.target.style.transform = 'translateY(0)';
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1rem' }}>
                      <Music size={24} style={{ marginRight: '0.5rem', color: '#667eea' }} />
                      <h3 style={{ margin: 0 }}>{playlist.title}</h3>
                    </div>
                    <p style={{ color: '#666', marginBottom: '1rem' }}>
                      {playlist.tracks?.length || 0} tracks
                    </p>
                    <button
                      className="btn"
                      style={{
                        width: '100%',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '0.5rem'
                      }}
                    >
                      <Play size={16} />
                      Play
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Playlists;
