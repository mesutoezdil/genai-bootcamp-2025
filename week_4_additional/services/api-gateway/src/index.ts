import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import { json } from 'body-parser';
import { config } from '../config';
import { authRouter } from './routes/auth';
import { learningRouter } from './routes/learning';
import { analyticsRouter } from './routes/analytics';
import { logger } from './utils/logger';
import { metrics } from './metrics';

const app = express();

// Security middleware
app.use(helmet());
app.use(compression());
app.use(cors());
app.use(json());

// Metrics middleware
app.use(metrics);

// Routes
app.use('/api/auth', authRouter);
app.use('/api/learning', learningRouter);
app.use('/api/analytics', analyticsRouter);

// Error handling middleware
app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
  logger.error(err.message, { stack: err.stack });
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
const PORT = config.api.port;
app.listen(PORT, () => {
  logger.info(`API Gateway running on port ${PORT}`);
});
