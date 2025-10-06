import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#FF6B9D',
      light: '#FFA3C1',
      dark: '#CC4E7D',
    },
    secondary: {
      main: '#00D9FF',
      light: '#5FE3FF',
      dark: '#00B0CC',
    },
    background: {
      default: '#0A0E27',
      paper: '#151B3D',
    },
    text: {
      primary: '#FFFFFF',
      secondary: '#B8C5D6',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 700,
    },
    h2: {
      fontWeight: 600,
    },
    h3: {
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: 'linear-gradient(135deg, #151B3D 0%, #1A2250 100%)',
        },
      },
    },
  },
});
