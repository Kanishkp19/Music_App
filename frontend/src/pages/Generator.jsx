import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Button,
  Slider,
  FormControl,
  FormLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  Grid,
  IconButton,
  Divider,
} from '@mui/material';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import DownloadIcon from '@mui/icons-material/Download';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import RefreshIcon from '@mui/icons-material/Refresh';
import { emotionAPI, generatorAPI } from '@/services/api';

export const Generator = () => {
  const [currentMood, setCurrentMood] = useState(null);
  const [useCurrentMood, setUseCurrentMood] = useState(true);
  const [valence, setValence] = useState(0.5);
  const [arousal, setArousal] = useState(0.5);
  const [duration, setDuration] = useState(30);
  const [tempo, setTempo] = useState(120);
  const [style, setStyle] = useState('auto');
  const [generating, setGenerating] = useState(false);
  const [jobId, setJobId] = useState(null);
  const [jobStatus, setJobStatus] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  useEffect(() => {
    fetchCurrentMood();
    fetchHistory();
  }, []);

  useEffect(() => {
    let interval;
    if (jobId && jobStatus !== 'completed' && jobStatus !== 'failed') {
      interval = setInterval(() => {
        checkJobStatus();
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [jobId, jobStatus]);

  const fetchCurrentMood = async () => {
    try {
      const response = await emotionAPI.getCurrent();
      setCurrentMood(response.data);
      if (response.data) {
        setValence(response.data.valence);
        setArousal(response.data.arousal);
      }
    } catch (err) {
      console.log('No current mood found');
    }
  };

  const fetchHistory = async () => {
    setLoadingHistory(true);
    try {
      const response = await generatorAPI.getGenerationHistory(10);
      setHistory(response.data.history);
    } catch (err) {
      console.error('Failed to load history');
    } finally {
      setLoadingHistory(false);
    }
  };

  const checkJobStatus = async () => {
    try {
      const response = await generatorAPI.getGenerationStatus(jobId);
      setJobStatus(response.data.status);
      
      if (response.data.status === 'completed' || response.data.status === 'failed') {
        setGenerating(false);
        if (response.data.status === 'completed') {
          fetchHistory();
        }
      }
    } catch (err) {
      console.error('Failed to check job status');
    }
  };

  const handleGenerate = async () => {
    setError(null);
    setGenerating(true);
    setJobId(null);
    setJobStatus(null);

    try {
      const params = {
        use_current_mood: useCurrentMood,
        duration: duration,
        tempo: tempo,
        style: style,
      };

      if (!useCurrentMood) {
        params.valence = valence;
        params.arousal = arousal;
      }

      const response = await generatorAPI.startGeneration(params);
      setJobId(response.data.job_id);
      setJobStatus(response.data.status);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to start generation');
      setGenerating(false);
    }
  };

  const handleDownload = async (downloadJobId) => {
    try {
      const response = await generatorAPI.downloadGeneration(downloadJobId);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `generated_music_${downloadJobId}.wav`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Failed to download file');
    }
  };

  const getMoodDescription = (v, a) => {
    if (a > 0.6 && v > 0.6) return 'Happy & Energetic';
    if (a > 0.6 && v < 0.4) return 'Angry & Intense';
    if (a < 0.4 && v > 0.6) return 'Calm & Peaceful';
    if (a < 0.4 && v < 0.4) return 'Sad & Melancholic';
    return 'Neutral & Balanced';
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'success';
      case 'failed': return 'error';
      case 'processing': return 'warning';
      default: return 'info';
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box mb={4}>
        <Typography variant="h3" fontWeight={700} gutterBottom>
          AI Music Generator
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Generate original music based on your mood using AI
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Generation Controls */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Generation Settings
            </Typography>

            {/* Mood Source */}
            <FormControl component="fieldset" sx={{ mb: 3 }}>
              <FormLabel component="legend">Mood Source</FormLabel>
              <RadioGroup
                value={useCurrentMood ? 'current' : 'custom'}
                onChange={(e) => setUseCurrentMood(e.target.value === 'current')}
              >
                <FormControlLabel
                  value="current"
                  control={<Radio />}
                  label={
                    currentMood
                      ? `Use Current Mood (${currentMood.emotion})`
                      : 'Use Current Mood (No mood detected)'
                  }
                  disabled={!currentMood}
                />
                <FormControlLabel
                  value="custom"
                  control={<Radio />}
                  label="Custom Mood"
                />
              </RadioGroup>
            </FormControl>

            {/* Custom Mood Controls */}
            {!useCurrentMood && (
              <Box mb={3}>
                <Typography variant="subtitle2" gutterBottom>
                  Mood: {getMoodDescription(valence, arousal)}
                </Typography>
                
                <Box mb={2}>
                  <Typography variant="body2" gutterBottom>
                    Valence (Negative ← → Positive): {valence.toFixed(2)}
                  </Typography>
                  <Slider
                    value={valence}
                    onChange={(_, value) => setValence(value)}
                    min={0}
                    max={1}
                    step={0.01}
                    marks={[
                      { value: 0, label: 'Negative' },
                      { value: 0.5, label: 'Neutral' },
                      { value: 1, label: 'Positive' },
                    ]}
                  />
                </Box>

                <Box mb={2}>
                  <Typography variant="body2" gutterBottom>
                    Arousal (Calm ← → Energetic): {arousal.toFixed(2)}
                  </Typography>
                  <Slider
                    value={arousal}
                    onChange={(_, value) => setArousal(value)}
                    min={0}
                    max={1}
                    step={0.01}
                    marks={[
                      { value: 0, label: 'Calm' },
                      { value: 0.5, label: 'Moderate' },
                      { value: 1, label: 'Energetic' },
                    ]}
                  />
                </Box>
              </Box>
            )}

            <Divider sx={{ my: 3 }} />

            {/* Musical Parameters */}
            <Box mb={2}>
              <Typography variant="body2" gutterBottom>
                Duration: {duration} seconds
              </Typography>
              <Slider
                value={duration}
                onChange={(_, value) => setDuration(value)}
                min={15}
                max={120}
                step={5}
                marks={[
                  { value: 15, label: '15s' },
                  { value: 60, label: '1m' },
                  { value: 120, label: '2m' },
                ]}
              />
            </Box>

            <Box mb={2}>
              <Typography variant="body2" gutterBottom>
                Tempo: {tempo} BPM
              </Typography>
              <Slider
                value={tempo}
                onChange={(_, value) => setTempo(value)}
                min={60}
                max={180}
                step={5}
                marks={[
                  { value: 60, label: 'Slow' },
                  { value: 120, label: 'Medium' },
                  { value: 180, label: 'Fast' },
                ]}
              />
            </Box>

            <FormControl component="fieldset" sx={{ mb: 3 }}>
              <FormLabel component="legend">Style</FormLabel>
              <RadioGroup
                value={style}
                onChange={(e) => setStyle(e.target.value)}
                row
              >
                <FormControlLabel value="auto" control={<Radio />} label="Auto" />
                <FormControlLabel value="ambient" control={<Radio />} label="Ambient" />
                <FormControlLabel value="melodic" control={<Radio />} label="Melodic" />
                <FormControlLabel value="rhythmic" control={<Radio />} label="Rhythmic" />
              </RadioGroup>
            </FormControl>

            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            <Button
              variant="contained"
              size="large"
              fullWidth
              startIcon={generating ? <CircularProgress size={20} /> : <MusicNoteIcon />}
              onClick={handleGenerate}
              disabled={generating || (useCurrentMood && !currentMood)}
            >
              {generating ? 'Generating...' : 'Generate Music'}
            </Button>

            {/* Generation Progress */}
            {generating && jobStatus && (
              <Box mt={3}>
                <Card>
                  <CardContent>
                    <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                      <Typography variant="subtitle1">Generation Status</Typography>
                      <Chip
                        label={jobStatus}
                        color={getStatusColor(jobStatus)}
                        size="small"
                      />
                    </Box>
                    {jobStatus === 'processing' && <LinearProgress />}
                    {jobStatus === 'completed' && (
                      <Button
                        variant="outlined"
                        startIcon={<DownloadIcon />}
                        onClick={() => handleDownload(jobId)}
                        fullWidth
                      >
                        Download Generated Music
                      </Button>
                    )}
                  </CardContent>
                </Card>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Generation History */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
              <Typography variant="h6">Recent Generations</Typography>
              <IconButton size="small" onClick={fetchHistory}>
                <RefreshIcon />
              </IconButton>
            </Box>

            {loadingHistory ? (
              <Box display="flex" justifyContent="center" p={3}>
                <CircularProgress />
              </Box>
            ) : history.length === 0 ? (
              <Typography variant="body2" color="text.secondary" align="center">
                No generations yet
              </Typography>
            ) : (
              <Box>
                {history.map((item) => (
                  <Card key={item.job_id} sx={{ mb: 2 }}>
                    <CardContent>
                      <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                        <Chip
                          label={item.status}
                          color={getStatusColor(item.status)}
                          size="small"
                        />
                        <Typography variant="caption" color="text.secondary">
                          {new Date(item.created_at).toLocaleDateString()}
                        </Typography>
                      </Box>
                      <Typography variant="body2" gutterBottom>
                        {item.parameters.duration}s • {item.parameters.tempo || 'Auto'} BPM
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {item.parameters.style}
                      </Typography>
                      {item.status === 'completed' && (
                        <Button
                          size="small"
                          startIcon={<DownloadIcon />}
                          onClick={() => handleDownload(item.job_id)}
                          fullWidth
                          sx={{ mt: 1 }}
                        >
                          Download
                        </Button>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};
