export const config = {
  api: {
    baseUrl: 'http://localhost:3000',
    timeout: 10000
  },
  app: {
    name: 'Chinese Learning App',
    version: '1.0.0',
    theme: {
      primary: '#1976d2',
      secondary: '#dc004e',
      background: '#f5f5f5'
    }
  },
  openai: {
    model: 'gpt-4',
    temperature: 0.7
  }
};
