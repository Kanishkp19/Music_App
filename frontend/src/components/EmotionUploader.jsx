import { useState } from 'react';
import { Box, Button, Typography, Card, CardContent, CircularProgress, Alert } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { emotionAPI } from '@/services/api';

export const EmotionUploader = ({ onAnalysisComplete }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setPreview(URL.createObjectURL(file));
    setError(null);
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('image', file);

      const response = await emotionAPI.analyzeImage(formData);
      onAnalysisComplete(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze image');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Upload Photo for Emotion Detection
        </Typography>

        <Box textAlign="center" py={4}>
          <input
            accept="image/*"
            style={{ display: 'none' }}
            id="image-upload"
            type="file"
            onChange={handleFileChange}
            disabled={loading}
          />
          <label htmlFor="image-upload">
            <Button
              variant="contained"
              component="span"
              startIcon={<CloudUploadIcon />}
              disabled={loading}
              size="large"
            >
              Choose Image
            </Button>
          </label>

          {preview && (
            <Box mt={3}>
              <img
                src={preview}
                alt="Preview"
                style={{ maxWidth: '100%', maxHeight: '300px', borderRadius: '8px' }}
              />
            </Box>
          )}

          {loading && (
            <Box mt={3}>
              <CircularProgress />
              <Typography variant="body2" mt={2}>
                Analyzing your emotion...
              </Typography>
            </Box>
          )}

          {error && (
            <Alert severity="error" sx={{ mt: 3 }}>
              {error}
            </Alert>
          )}
        </Box>
      </CardContent>
    </Card>
  );
};
