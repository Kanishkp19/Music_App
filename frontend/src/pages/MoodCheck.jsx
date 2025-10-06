import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Tabs,
  Tab,
  Card,
  CardContent,
  Button,
  Alert,
} from '@mui/material';
import { EmotionUploader } from '@/components/EmotionUploader';
import { TextMoodAnalyzer } from '@/components/TextMoodAnalyzer';
import { MoodSelector } from '@/components/MoodSelector';
import { emotionAPI } from '@/services/api';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

export const MoodCheck = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [selectedEmotion, setSelectedEmotion] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleManualSubmit = async () => {
    if (!selectedEmotion) return;

    setLoading(true);
    try {
      const response = await emotionAPI.manualEntry(selectedEmotion);
      setAnalysisResult({
        analysis: {
          emotion: selectedEmotion,
          confidence: 1.0,
        },
        mood_entry: response.data.mood_entry,
      });
    } catch (error) {
      console.error('Failed to submit mood:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGetRecommendations = () => {
    navigate('/recommendations');
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 10 }}>
      <Typography variant="h3" fontWeight={700} gutterBottom textAlign="center">
        How are you feeling?
      </Typography>
      <Typography variant="body1" color="text.secondary" textAlign="center" paragraph>
        Choose a method to detect your current emotion
      </Typography>

      {analysisResult && (
        <Alert
          icon={<CheckCircleIcon />}
          severity="success"
          sx={{ mb: 3 }}
          action={
            <Button color="inherit" size="small" onClick={handleGetRecommendations}>
              Get Recommendations
            </Button>
          }
        >
          Emotion detected: <strong>{analysisResult.analysis.emotion}</strong> (
          {(analysisResult.analysis.confidence * 100).toFixed(0)}% confidence)
        </Alert>
      )}

      <Card>
        <Tabs
          value={activeTab}
          onChange={(_, newValue) => setActiveTab(newValue)}
          variant="fullWidth"
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab label="Upload Photo" />
          <Tab label="Describe Feelings" />
          <Tab label="Manual Selection" />
        </Tabs>

        <CardContent sx={{ p: 3 }}>
          {activeTab === 0 && <EmotionUploader onAnalysisComplete={setAnalysisResult} />}

          {activeTab === 1 && <TextMoodAnalyzer onAnalysisComplete={setAnalysisResult} />}

          {activeTab === 2 && (
            <Box>
              <MoodSelector
                selectedEmotion={selectedEmotion}
                onSelect={setSelectedEmotion}
              />
              <Box mt={3} textAlign="center">
                <Button
                  variant="contained"
                  size="large"
                  onClick={handleManualSubmit}
                  disabled={!selectedEmotion || loading}
                >
                  {loading ? 'Saving...' : 'Submit Mood'}
                </Button>
              </Box>
            </Box>
          )}
        </CardContent>
      </Card>
    </Container>
  );
};
