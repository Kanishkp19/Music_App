import { useState, useRef, useEffect } from 'react';
import { Box, Card, Typography, IconButton, Slider, LinearProgress } from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import PauseIcon from '@mui/icons-material/Pause';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import SkipPreviousIcon from '@mui/icons-material/SkipPrevious';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';

export const MusicPlayer = ({ currentTrack, playlist, onTrackChange }) => {
  const [playing, setPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(0.7);
  const audioRef = useRef(new Audio());

  useEffect(() => {
    const audio = audioRef.current;

    if (currentTrack) {
      audio.src = currentTrack.stream_url;
      audio.load();
      if (playing) {
        audio.play();
      }
    }

    audio.ontimeupdate = () => setCurrentTime(audio.currentTime);
    audio.onloadedmetadata = () => setDuration(audio.duration);
    audio.onended = handleNext;

    return () => {
      audio.pause();
      audio.src = '';
    };
  }, [currentTrack]);

  useEffect(() => {
    audioRef.current.volume = volume;
  }, [volume]);

  const togglePlay = () => {
    if (playing) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setPlaying(!playing);
  };

  const handleSeek = (_, value) => {
    audioRef.current.currentTime = value;
    setCurrentTime(value);
  };

  const handleNext = () => {
    if (!playlist || playlist.length === 0) return;
    const currentIndex = playlist.findIndex((t) => t.id === currentTrack?.id);
    const nextIndex = (currentIndex + 1) % playlist.length;
    onTrackChange(playlist[nextIndex]);
  };

  const handlePrevious = () => {
    if (!playlist || playlist.length === 0) return;
    const currentIndex = playlist.findIndex((t) => t.id === currentTrack?.id);
    const prevIndex = currentIndex === 0 ? playlist.length - 1 : currentIndex - 1;
    onTrackChange(playlist[prevIndex]);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!currentTrack) {
    return (
      <Card sx={{ position: 'fixed', bottom: 0, left: 0, right: 0, p: 2 }}>
        <Typography variant="body2" color="text.secondary" align="center">
          No track selected
        </Typography>
      </Card>
    );
  }

  return (
    <Card sx={{ position: 'fixed', bottom: 0, left: 0, right: 0, zIndex: 1000 }}>
      <LinearProgress
        variant="determinate"
        value={(currentTime / duration) * 100 || 0}
        sx={{ height: 2 }}
      />
      <Box p={2} display="flex" alignItems="center" gap={2}>
        <Box
          component="img"
          src={currentTrack.artwork_url || 'https://via.placeholder.com/60'}
          alt={currentTrack.title}
          sx={{ width: 60, height: 60, borderRadius: 1 }}
        />

        <Box flexGrow={1}>
          <Typography variant="subtitle1" noWrap>
            {currentTrack.title}
          </Typography>
          <Typography variant="body2" color="text.secondary" noWrap>
            {currentTrack.artist}
          </Typography>
        </Box>

        <Box display="flex" alignItems="center" gap={1}>
          <IconButton onClick={handlePrevious} disabled={!playlist || playlist.length <= 1}>
            <SkipPreviousIcon />
          </IconButton>
          <IconButton onClick={togglePlay} color="primary" size="large">
            {playing ? <PauseIcon /> : <PlayArrowIcon />}
          </IconButton>
          <IconButton onClick={handleNext} disabled={!playlist || playlist.length <= 1}>
            <SkipNextIcon />
          </IconButton>
        </Box>

        <Box display="flex" alignItems="center" gap={2} minWidth={300}>
          <Typography variant="caption">{formatTime(currentTime)}</Typography>
          <Slider
            value={currentTime}
            max={duration || 100}
            onChange={handleSeek}
            sx={{ flexGrow: 1 }}
          />
          <Typography variant="caption">{formatTime(duration)}</Typography>
        </Box>

        <Box display="flex" alignItems="center" gap={1} minWidth={150}>
          <VolumeUpIcon />
          <Slider
            value={volume}
            min={0}
            max={1}
            step={0.01}
            onChange={(_, value) => setVolume(value)}
          />
        </Box>
      </Box>
    </Card>
  );
};
