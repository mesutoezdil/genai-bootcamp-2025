# Chinese Learning Platform

[![Docker](https://img.shields.io/docker/build/yourusername/chinese-learning-platform)](https://hub.docker.com/r/yourusername/chinese-learning-platform)
[![CI Status](https://github.com/yourusername/chinese-learning-platform/workflows/CI/badge.svg)](https://github.com/yourusername/chinese-learning-platform/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A professional Chinese language learning platform that leverages OpenAI Enterprise API for advanced language processing and interactive learning experiences. The platform is built using a modern microservices architecture with comprehensive observability and monitoring capabilities.

## 🚀 Features

- 🌐 Real-time Chinese text analysis using OpenAI Enterprise
- 📚 Interactive learning sessions with personalized content
- 📊 Comprehensive analytics and progress tracking
- 📱 Responsive web interface with Material-UI
- 🔐 Enterprise-grade security and authentication
- 📈 Real-time monitoring with Prometheus and Grafana
- 🔄 Containerized deployment with Docker
- 🔄 CI/CD integration with GitHub Actions

## 🏗️ Architecture

The platform is built using a microservices architecture with the following components:

### 1. API Gateway
- Built with Node.js/Express
- JWT-based authentication
- Rate limiting and request validation
- Service routing and load balancing
- OpenAPI/Swagger documentation

### 2. Learning Service
- OpenAI Enterprise integration
- Text analysis and processing
- Example sentence generation
- Word meaning and usage analysis
- Audio processing capabilities

### 3. Analytics Service
- User progress tracking
- Learning analytics
- Performance metrics
- Usage statistics
- Custom reporting

### 4. Frontend Service
- React with TypeScript
- Material-UI components
- Responsive design
- Real-time updates
- Progressive Web App (PWA) support

### 5. Monitoring Stack
- Prometheus for metrics collection
- Grafana for visualization
- Alertmanager for notifications
- ELK Stack for logging
- Zipkin for distributed tracing

## 🛠️ Technical Stack

### Frontend
- React 18
- TypeScript
- Material-UI
- Redux Toolkit
- React Router
- i18next for internationalization

### Backend
- Node.js
- Express.js
- OpenAI Enterprise API
- PostgreSQL
- Redis

### Infrastructure
- Docker
- Docker Compose
- Kubernetes (optional)
- Prometheus
- Grafana
- ELK Stack

## 📋 Prerequisites

- Node.js (v18 or higher)
- Docker and Docker Compose
- OpenAI Enterprise API credentials
- PostgreSQL 15+
- Redis 7+

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chinese-learning-platform.git
```

2. Copy the environment file:
```bash
cp .env.example .env
```

3. Update the `.env` file with your credentials:
```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_ORGANIZATION_ID=your_organization_id

# Database Configuration
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=chinese_learning

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Frontend Configuration
FRONTEND_URL=http://localhost:80

# API Configuration
API_PORT=3000
```

4. Build and run the containers:
```bash
docker-compose up -d
```

5. Access the application:
- Frontend: http://localhost:80
- API Gateway: http://localhost:3000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001

## 📊 Monitoring Setup

The platform includes comprehensive monitoring capabilities:

1. **Prometheus Metrics**:
   - Request metrics (latency, success rate)
   - System health metrics
   - Database performance
   - Redis metrics

2. **Grafana Dashboards**:
   - System Overview
   - API Performance
   - Database Metrics
   - User Analytics
   - Learning Progress

3. **Alerting Configuration**:
   - High CPU usage alerts
   - Memory usage warnings
   - Request latency alerts
   - Error rate notifications

## 🛡️ Security Features

- JWT-based authentication
- Rate limiting
- Input validation
- Secure API key management
- HTTPS enforcement
- CORS configuration
- Security headers
- Regular security audits

## 📝 Documentation

- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)
- [Monitoring Guide](docs/monitoring.md)
- [Security Guide](docs/security.md)
- [Troubleshooting Guide](docs/troubleshooting.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- OpenAI for their enterprise API
- Material-UI team for their excellent UI components
- The Docker community for containerization
- Prometheus and Grafana teams for monitoring solutions
