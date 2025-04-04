export const config = {
  apiUrl: process.env.VITE_API_URL || 'http://localhost:5000/api',
  appName: 'Chinese Language Portal',
  version: '1.0.0',
  features: {
    speechRecognition: true,
    characterPractice: true,
    grammarExercises: true
  }
}
