import { AppBar, Toolbar, Typography, Button, Box, IconButton } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import LogoutIcon from '@mui/icons-material/Logout';

export const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout, isAuthenticated } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { label: 'Home', path: '/' },
    { label: 'Mood Check', path: '/mood-check' },
    { label: 'Recommendations', path: '/recommendations' },
    { label: 'Generator', path: '/generator' },
    { label: 'History', path: '/history' },
  ];

  return (
    <AppBar position="static" sx={{ background: 'linear-gradient(90deg, #FF6B9D 0%, #00D9FF 100%)' }}>
      <Toolbar>
        <MusicNoteIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 0, fontWeight: 700 }}>
          MuseAIka
        </Typography>

        <Box sx={{ flexGrow: 1, display: 'flex', ml: 4 }}>
          {isAuthenticated && navItems.map((item) => (
            <Button
              key={item.path}
              color="inherit"
              onClick={() => navigate(item.path)}
              sx={{
                mx: 1,
                fontWeight: location.pathname === item.path ? 700 : 400,
                borderBottom: location.pathname === item.path ? '2px solid white' : 'none',
              }}
            >
              {item.label}
            </Button>
          ))}
        </Box>

        {isAuthenticated && (
          <Box display="flex" alignItems="center" gap={2}>
            <Typography variant="body2">{user?.name}</Typography>
            <IconButton color="inherit" onClick={handleLogout} title="Logout">
              <LogoutIcon />
            </IconButton>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
};
