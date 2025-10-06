import { useEffect, useState } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Grid,
  CircularProgress,
  Alert,
  Chip,
} from '@mui/material';
import { emotionAPI } from '@/services/api';
import { EMOTIONS } from '@/utils/constants';

export const History = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await emotionAPI.getHistory(50);
      setHistory(response.data.history);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load history');
    } finally {
      setLoading(false);
    }
  };

  const getEmotionData = (emotion) => {
    return EMOTIONS.find((e) => e.value === emotion) || EMOTIONS[6];
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
    <Container maxWidth="lg" sx={{ mt: 4, mb: 10 }}>
      <Typography variant="h3" fontWeight={700} gutterBottom>
        Your Mood History
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Track your emotional journey over time
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {history.length === 0 ? (
        <Alert severity="info">
          No mood history yet. Start by checking your mood!
        </Alert>
      ) : (
        <Grid container spacing={2}>
          {history.map((entry) => {
            const emotionData = getEmotionData(entry.emotion);
            return (
              <Grid item xs={12} key={entry.id}>
                <Card>
                  <CardContent>
                    <Box display="flex" alignItems="center" gap={2}>
                      <Box fontSize="2.5rem">{emotionData.emoji}</Box>
                      
                      <Box flexGrow={1}>
                        <Typography variant="h6" sx={{ textTransform: 'capitalize' }}>
                          {entry.emotion}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {new Date(entry.timestamp).toLocaleString()}
                        </Typography>
                      </Box>

                      <Box display="flex" gap={1}>
                        <Chip
                          label={`Source: ${entry.source}`}
                          size="small"
                          variant="outlined"
                        />
                        <Chip
                          label={`${(entry.confidence * 100).toFixed(0)}% confidence`}
                          size="small"
                          color="primary"
                          variant="outlined"
                        />
                      </Box>

                      <Box textAlign="right" minWidth={120}>
                        <Typography variant="caption" color="text.secondary">
                          Valence: {entry.valence.toFixed(2)}
                        </Typography>
                        <br />
                        <Typography variant="caption" color="text.secondary">
                          Arousal: {entry.arousal.toFixed(2)}
                        </Typography>
                      </Box>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            );
          })}
        </Grid>
      )}
    </Container>
  );
};
