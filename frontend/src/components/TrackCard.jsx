import { Card, CardContent, CardMedia, Typography, Box, IconButton, Chip } from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import FavoriteIcon from '@mui/icons-material/Favorite';

export const TrackCard = ({ track, onPlay }) => {
  const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardMedia
        component="img"
        height="200"
        image={track.artwork_url || 'https://via.placeholder.com/300x300?text=No+Artwork'}
        alt={track.title}
        sx={{ objectFit: 'cover' }}
      />
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography variant="h6" noWrap title={track.title}>
          {track.title}
        </Typography>
        <Typography variant="body2" color="text.secondary" noWrap>
          {track.artist}
        </Typography>

        <Box mt={2} display="flex" gap={1} flexWrap="wrap">
          {track.genre && (
            <Chip label={track.genre} size="small" color="secondary" variant="outlined" />
          )}
          {track.mood && (
            <Chip label={track.mood} size="small" color="primary" variant="outlined" />
          )}
        </Box>

        <Box mt={2} display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="caption" color="text.secondary">
            {formatDuration(track.duration)}
          </Typography>
          <Box display="flex" gap={1}>
            <IconButton size="small" color="primary" onClick={() => onPlay(track)}>
              <PlayArrowIcon />
            </IconButton>
            <IconButton size="small" color="error">
              <FavoriteIcon fontSize="small" />
            </IconButton>
          </Box>
        </Box>

        <Box mt={1} display="flex" gap={2}>
          <Typography variant="caption" color="text.secondary">
            ▶ {track.play_count?.toLocaleString() || 0}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            ❤ {track.favorite_count?.toLocaleString() || 0}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};
