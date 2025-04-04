import express from 'express';
import cors from 'cors';
import { config } from '../config';
import { OpenAIClient } from './services/openai';
import { WordService } from './services/word';
import { logger } from './utils/logger';
import { metrics } from './metrics';
import { learningRouter } from './routes/learning';

const app = express();

// Initialize services
const openai = new OpenAIClient(config.openai);
const wordService = new WordService(openai);

// Middleware
app.use(cors());
app.use(express.json());
app.use(metrics);

// Routes
app.use('/api/learning', learningRouter(wordService));

// Error handling
app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
  logger.error(err.message, { stack: err.stack });
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
const PORT = config.learningService.port;
app.listen(PORT, () => {
  logger.info(`Learning service running on port ${PORT}`);
});
