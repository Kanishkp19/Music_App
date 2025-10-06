import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Button,
  Grid,
  Card,
  CardContent,
  CircularProgress,
} from '@mui/material';
import { emotionAPI } from '@/services/api';
import { EMOTIONS } from '@/utils/constants';
import MoodIcon from '@mui/icons-material/Mood';
import LibraryMusicIcon from '@mui/icons-material/LibraryMusic';
import HistoryIcon from '@mui/icons-material/History';

export const Home = () => {
  const [currentMood, setCurrentMood] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchCurrentMood();
  }, []);

  const fetchCurrentMood = async () => {
    try {
      const response = await emotionAPI.getCurrent();
      setCurrentMood(response.data.mood);
    } catch (error) {
      console.error('Failed to fetch mood:', error);
    } finally {
      setLoading(false);
    }
  };

  const getMoodEmoji = (emotion) => {
    const emotionData = EMOTIONS.find((e) => e.value === emotion);
    return emotionData?.emoji || '😐';
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 10 }}>
      <Box textAlign="center" mb={6}>
        <Typography variant="h2" fontWeight={700} gutterBottom>
          Welcome to MuseAIka 🎵
        </Typography>
        <Typography variant="h5" color="text.secondary">
          AI-Powered Emotion-Based Music Discovery
        </Typography>
      </Box>

      {loading ? (
        <Box display="flex" justifyContent="center" my={4}>
          <CircularProgress />
        </Box>
      ) : currentMood ? (
        <Card sx={{ mb: 4, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
          <CardContent sx={{ textAlign: 'center', py: 4 }}>
            <Typography variant="h4" gutterBottom>
              Your Current Mood
            </Typography>
            <Typography variant="h1" sx={{ fontSize: '4rem' }}>
              {getMoodEmoji(currentMood.emotion)}
            </Typography>
            <Typography variant="h5" sx={{ textTransform: 'capitalize', mt: 2 }}>
              {currentMood.emotion}
            </Typography>
            <Typography variant="body2" sx={{ mt: 1, opacity: 0.9 }}>
              Detected {new Date(currentMood.timestamp).toLocaleDateString()} via{' '}
              {currentMood.source}
            </Typography>
          </CardContent>
        </Card>
      ) : (
        <Card sx={{ mb: 4 }}>
          <CardContent sx={{ textAlign: 'center', py: 4 }}>
            <Typography variant="h5" gutterBottom>
              No mood detected yet
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              Let's discover your current emotion!
            </Typography>
            <Button
              variant="contained"
              size="large"
              onClick={() => navigate('/mood-check')}
            >
              Check My Mood
            </Button>
          </CardContent>
        </Card>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%', cursor: 'pointer' }} onClick={() => navigate('/mood-check')}>
            <CardContent sx={{ textAlign: 'center', py: 4 }}>
              <MoodIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h5" gutterBottom>
                Check Mood
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Upload a photo, describe your feelings, or manually select your mood
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card
            sx={{ height: '100%', cursor: 'pointer' }}
            onClick={() => navigate('/recommendations')}
          >
            <CardContent sx={{ textAlign: 'center', py: 4 }}>
              <LibraryMusicIcon sx={{ fontSize: 60, color: 'secondary.main', mb: 2 }} />
              <Typography variant="h5" gutterBottom>
                Get Recommendations
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Discover music that matches your current emotional state
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%', cursor: 'pointer' }} onClick={() => navigate('/history')}>
            <CardContent sx={{ textAlign: 'center', py: 4 }}>
              <HistoryIcon sx={{ fontSize: 60, color: 'success.main', mb: 2 }} />
              <Typography variant="h5" gutterBottom>
                View History
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Track your emotional journey over time
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box mt={6} textAlign="center">
        <Typography variant="h4" gutterBottom>
          How It Works
        </Typography>
        <Grid container spacing={3} mt={2}>
          <Grid item xs={12} md={3}>
            <Typography variant="h6" gutterBottom>
              1. Detect Emotion
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Use AI to analyze your face, text, or manually select your mood
            </Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="h6" gutterBottom>
              2. Map to Music
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Our AI maps your emotion to music characteristics
            </Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="h6" gutterBottom>
              3. Discover Tracks
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Get personalized recommendations from Audius
            </Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="h6" gutterBottom>
              4. Enjoy Music
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Listen and vibe with music that matches your mood
            </Typography>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};
