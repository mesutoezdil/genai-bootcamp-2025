export const config = {
  api: {
    baseUrl: process.env.REACT_APP_API_URL || 'http://localhost:8080/api',
    timeout: 10000,
  },
  app: {
    name: 'Chinese Learning App',
    version: '0.1.0',
    theme: {
      primary: '#1976d2',
      secondary: '#dc004e',
      background: '#f5f5f5',
    },
  },
  features: {
    speechRecognition: true,
    characterPractice: true,
    grammarExercises: true,
    darkMode: true,
  },
};
