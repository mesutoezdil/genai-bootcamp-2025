Below is a short guide on how to run a **Go-based backend** and a **React-based frontend** application on Docker, based on your existing **technical specification** documents (backend and frontend). In this guide, you will find:

1. **Dockerfile** examples (for both backend and frontend)  
2. A **docker-compose.yml** example (for orchestrating both)  
3. **Environment variable** and general usage tips  

---

## 1. Project Structure

You can use a directory structure similar to the following:

```text
my_chinese_learning_app/
├── backend_go/
│   ├── cmd/
│   │   └── server/
│   ├── internal/
│   ├── db/
│   ├── go.mod
│   ├── magefile.go
│   ├── Dockerfile
│   └── ...
├── frontend_react/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── Dockerfile
│   └── ...
├── docker-compose.yml
└── .env
```

> **Note**: Directory names and files may vary depending on your existing project.

---

## 2. Backend Dockerfile (Go)

Below is a very simple **multi-stage build** example. Here we use Go 1.20 and opt for a minimal Alpine image in the final stage.

**`backend_go/Dockerfile`**:

```dockerfile
# Stage 1: Builder
FROM golang:1.20-alpine AS builder

WORKDIR /app

# Copy go.mod and go.sum, then download modules
COPY go.mod go.sum ./
RUN go mod download

COPY . .

# Example: If you use Mage, migrations, or seeds, you can embed them here
# RUN mage build
RUN go build -o server ./cmd/server

# Stage 2: Final (runtime)
FROM alpine:3.17

# Optional: Add CA certificates if needed
RUN apk --no-cache add ca-certificates

WORKDIR /app

COPY --from=builder /app/server .
COPY db/ ./db  # For example, if migrations exist

# If the SQLite file is created for the first time, you can use a volume or local bind mount
# RUN ./server init_db etc.

EXPOSE 8080

# Environment variables, optionally you can COPY a .env file here
ENV BACKEND_PORT=8080

CMD ["./server"]
```

### Explanation
- In the **builder** stage, we run `go build` to produce an executable.  
- In the **final** stage, we copy that executable into a minimal Alpine image and expose port **8080**.  

---

## 3. Frontend Dockerfile (React)

We will build the React app using **Node**, then serve the build output with something like **Nginx**.

**`frontend_react/Dockerfile`**:

```dockerfile
# Stage 1: Builder
FROM node:16-alpine AS builder

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . .

# Production build
RUN yarn build

# Stage 2: Nginx
FROM nginx:stable-alpine

# Copy build output to /usr/share/nginx/html for serving
COPY --from=builder /app/build /usr/share/nginx/html

# Default Nginx config
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Explanation
- In the **builder** stage, we run `yarn build` for React.  
- In the **final** stage, we copy the build folder to the `nginx` image.  
- If you want SPA (Single Page Application) routing, add a relevant `nginx.conf`.  

---

## 4. Docker Compose Example

Below is a simple **docker-compose** example to bring up both **backend** and **frontend** services together.

**`docker-compose.yml`** (recommended at project root):

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend_go
      dockerfile: Dockerfile
    container_name: my_chinese_backend
    # Environment variables:
    environment:
      - BACKEND_PORT=8080
      # Example: DATABASE_URL=sqlite3://db/words.db
    ports:
      - '8080:8080'
    volumes:
      # If you want to persist the SQLite file, use a bind mount or named volume
      - ./backend_go/db:/app/db
    # depends_on:
    #   - db  # e.g., if you had a separate database service

  frontend:
    build:
      context: ./frontend_react
      dockerfile: Dockerfile
    container_name: my_chinese_frontend
    # If you want, define environment variable FRONTEND_PORT
    ports:
      - '3000:80'
    depends_on:
      - backend
```

### How to Run

From the project root (where `docker-compose.yml` is located):

1. `docker-compose build`  
2. `docker-compose up`  

This will run:  
- **Backend** on port 8080 (`localhost:8080`).  
- **Frontend** on port 3000 (`localhost:3000`).  

(For instance, the frontend can call the backend at `http://localhost:8080/api/...`.)

---

## 5. Environment Variables (.env)

You can use a **`.env`** file along with Docker Compose. For example:

**`.env`**:

```env
BACKEND_PORT=8080
FRONTEND_PORT=3000
DATABASE_URL=sqlite3://app/db/words.db
```

Then reference it in `docker-compose.yml` like `${ENV_VARIABLE}`. For instance:

```yaml
services:
  backend:
    environment:
      - BACKEND_PORT=${BACKEND_PORT}
      - DATABASE_URL=${DATABASE_URL}
    ports:
      - '${BACKEND_PORT}:${BACKEND_PORT}'
```

---

## 6. Additional Tips

1. **CI/CD**  
   - Use GitHub Actions or GitLab CI, etc. to:  
     1. Run tests upon code push.  
     2. Build Docker images.  
     3. Push them to a registry (e.g., Docker Hub).  

2. **Production Environment**  
   - You might switch from `docker-compose` to an orchestration solution (Kubernetes, ECS, etc.) later.  
   - Don’t forget Nginx, reverse proxy, and HTTPS (Let’s Encrypt, etc.) in a real production scenario.

3. **Logging & Monitoring**  
   - Printing logs to stdout/stderr is often enough to start.  
   - For advanced insights, consider Prometheus/Grafana or an ELK Stack.

4. **Versioning**  
   - Tag images: e.g., `my_chinese_backend:v1.0.0`.  
   - Relying solely on `latest` is usually not recommended for production.  