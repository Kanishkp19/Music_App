import { useState } from 'react';
import { Box, TextField, Button, Card, CardContent, Typography, CircularProgress, Alert } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { emotionAPI } from '@/services/api';

export const TextMoodAnalyzer = ({ onAnalysisComplete }) => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!text.trim()) return;

    setError(null);
    setLoading(true);

    try {
      const response = await emotionAPI.analyzeText(text);
      onAnalysisComplete(response.data);
      setText('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze text');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Describe How You're Feeling
        </Typography>

        <TextField
          fullWidth
          multiline
          rows={4}
          placeholder="Tell us how you feel... (e.g., 'I'm feeling really happy today!')"
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={loading}
          sx={{ mb: 2 }}
        />

        <Button
          variant="contained"
          fullWidth
          onClick={handleAnalyze}
          disabled={loading || !text.trim()}
          startIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
        >
          {loading ? 'Analyzing...' : 'Analyze Mood'}
        </Button>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </CardContent>
    </Card>
  );
};
