import { Grid, Card, CardContent, Typography, Box } from '@mui/material';
import { EMOTIONS } from '@/utils/constants';

export const MoodSelector = ({ onSelect, selectedEmotion }) => {
  return (
    <Grid container spacing={2}>
      {EMOTIONS.map((emotion) => (
        <Grid item xs={6} sm={4} md={3} key={emotion.value}>
          <Card
            sx={{
              cursor: 'pointer',
              transition: 'all 0.3s',
              border: selectedEmotion === emotion.value ? '3px solid' : '1px solid transparent',
              borderColor: selectedEmotion === emotion.value ? emotion.color : 'transparent',
              '&:hover': {
                transform: 'scale(1.05)',
                boxShadow: 6,
              },
            }}
            onClick={() => onSelect(emotion.value)}
          >
            <CardContent sx={{ textAlign: 'center' }}>
              <Box fontSize="3rem" mb={1}>
                {emotion.emoji}
              </Box>
              <Typography variant="h6" sx={{ color: emotion.color }}>
                {emotion.label}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};
