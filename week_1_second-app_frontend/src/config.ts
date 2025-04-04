export const config = {
  apiUrl: process.env.VITE_API_URL || 'http://localhost:3000/api',
  appName: process.env.VITE_APP_NAME || 'Chinese Learning App',
  appVersion: process.env.VITE_APP_VERSION || '1.0.0',
  appDescription: process.env.VITE_APP_DESCRIPTION || 'An app for learning Chinese'
}
