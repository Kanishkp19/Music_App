export const EMOTIONS = [
  { value: 'happy', label: 'Happy', color: '#FFD700', emoji: '😊' },
  { value: 'sad', label: 'Sad', color: '#4682B4', emoji: '😢' },
  { value: 'angry', label: 'Angry', color: '#DC143C', emoji: '😠' },
  { value: 'calm', label: 'Calm', color: '#98FB98', emoji: '😌' },
  { value: 'excited', label: 'Excited', color: '#FF69B4', emoji: '🤩' },
  { value: 'anxious', label: 'Anxious', color: '#DDA0DD', emoji: '😰' },
  { value: 'neutral', label: 'Neutral', color: '#D3D3D3', emoji: '😐' },
];

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
