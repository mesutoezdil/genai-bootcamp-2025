# OPEA LLM Mega-Service

This repository hosts an advanced implementation of an Ollama-based LLM service, containerized with Docker and orchestrated using Docker Compose. It pairs a robust FastAPI application with the Ollama server to provide enhanced text generation, model management, and improved overall reliability.

## Overview

In this version, the core functionality of the original project is preserved, but significant improvements have been made:

- **Advanced Logging & Error Handling:** Detailed logs and dedicated exception handlers help diagnose issues quickly, both during development and in production.
- **Request Validation with Pydantic:** Incoming API requests are validated against Pydantic models, ensuring consistent data formats and automatic, user-friendly documentation through Swagger.
- **Additional Endpoints:** Beyond basic text generation and model pulling, a new endpoint (`/v1/models`) has been added to list available models, enhancing control over the deployed models.
- **Modular & Future-Proof Architecture:** With a dedicated Dockerfile, clear environment variable configuration, and containerized services, this setup is highly maintainable and easily extendable.

## Prerequisites

- **Docker** (preferably Docker Engine >= 20.10)
- **Docker Compose** (compose v2 syntax)
- **Python 3.10+** (optional, if running outside Docker)

## Environment Variables

Configure these variables in your shell or in a `.env` file:

- `LLM_MODEL_ID`: The default Ollama model identifier (e.g., `llama3.2:1b`). Default is `"llama3.2:1b"`.
- `LLM_ENDPOINT_PORT`: The host port mapped to Ollama’s internal port 11434. Default is `8008`.
- `no_proxy`, `http_proxy`, `https_proxy`: Set these if proxy configurations are needed.
- `OLLAMA_SERVER_HOST` and `OLLAMA_SERVER_PORT` are set automatically by Docker Compose for internal networking.

## Getting Started

1. **Clone this repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Build and start the services using Docker Compose:**
   ```bash
   docker compose up --build
   ```
   This command will:
   - Launch the `ollama-server` container using the official Ollama image.
   - Build and run the `my-app` container containing the advanced FastAPI application.

3. **Verify the Service:**
   - Open your browser and visit [http://localhost:8000](http://localhost:8000). You should see a welcome message:
     ```json
     {"message": "Welcome to the advanced OPEA LLM mega-service!"}
     ```
   - Access the Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs) to explore the API endpoints.

## API Endpoints

### 1. Root Endpoint
- **GET /**  
  Returns a simple welcome message, useful for health checks.

### 2. Generate Text
- **POST /v1/generate**  
  Sends a prompt to the Ollama server for text generation.
  
  **Request Body Example:**
  ```json
  {
    "model": "llama3.2:1b",
    "prompt": "Why is the sky blue?"
  }
  ```
  If the `model` field is omitted, the default model is used.

### 3. Pull Model
- **POST /v1/pull**  
  Downloads a new model into the Ollama server’s cache.
  
  **Request Body Example:**
  ```json
  {
    "model": "llama3.2:1b"
  }
  ```
  Again, if `model` is omitted, the default is applied.

### 4. List Models
- **GET /v1/models**  
  Retrieves a list of models currently available on the Ollama server. This endpoint is useful for verifying which models are loaded and ready for use.
