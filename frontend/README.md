# MuseAIka Frontend

AI-Powered Emotion-Based Music Discovery Platform

## Setup Instructions

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables:
   - Copy `.env` and update if needed
   - Default API URL: `http://localhost:5000`

3. Start development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

## Features

- Emotion detection via facial recognition, text analysis, or manual selection
- AI-powered music recommendations based on detected emotions
- Music player with playlist functionality
- Mood history tracking
- Modern dark theme UI with Material-UI

## Tech Stack

- React 18
- Vite
- Material-UI (MUI)
- React Router
- Axios
- Emotion/Styled

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   ├── pages/          # Page components
│   ├── services/       # API services
│   ├── context/        # React context providers
│   ├── styles/         # Theme and styling
│   ├── utils/          # Utility functions and constants
│   ├── App.jsx         # Main app component
│   └── main.jsx        # Entry point
├── index.html
├── vite.config.js
└── package.json
```

## Available Routes

- `/` - Home page
- `/login` - User login
- `/register` - User registration
- `/mood-check` - Emotion detection
- `/recommendations` - Music recommendations
- `/history` - Mood history

