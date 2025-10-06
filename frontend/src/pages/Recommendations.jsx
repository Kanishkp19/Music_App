import { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Grid,
  CircularProgress,
  Alert,
  Button,
} from '@mui/material';
import { musicAPI } from '@/services/api';
import { TrackCard } from '@/components/TrackCard';
import { MusicPlayer } from '@/components/MusicPlayer';
import RefreshIcon from '@mui/icons-material/Refresh';

export const Recommendations = () => {
  const [tracks, setTracks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentTrack, setCurrentTrack] = useState(null);
  const [basedOnMood, setBasedOnMood] = useState(null);

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await musicAPI.getRecommendations(20);
      setTracks(response.data.recommendations);
      setBasedOnMood(response.data.based_on_mood);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load recommendations');
    } finally {
      setLoading(false);
    }
  };

  const handlePlay = (track) => {
    setCurrentTrack(track);
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="50vh">
          <CircularProgress size={60} />
        </Box>
      </Container>
    );
  }

  return (
    <>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 12 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Box>
            <Typography variant="h3" fontWeight={700} gutterBottom>
              Recommendations For You
            </Typography>
            {basedOnMood && (
              <Typography variant="body1" color="text.secondary">
                Based on your <strong>{basedOnMood.emotion}</strong> mood
              </Typography>
            )}
          </Box>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={fetchRecommendations}
          >
            Refresh
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {tracks.length === 0 ? (
          <Alert severity="info">
            No recommendations found. Try checking your mood first!
          </Alert>
        ) : (
          <Grid container spacing={3}>
            {tracks.map((track) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={track.id}>
                <TrackCard track={track} onPlay={handlePlay} />
              </Grid>
            ))}
          </Grid>
        )}
      </Container>

      <MusicPlayer
        currentTrack={currentTrack}
        playlist={tracks}
        onTrackChange={setCurrentTrack}
      />
    </>
  );
};
