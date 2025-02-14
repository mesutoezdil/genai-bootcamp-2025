# OPEA LLM Service

This repository hosts a sample setup for running an Ollama-based LLM service (via Docker) alongside a Python FastAPI application.

## 1. Prerequisites

- **Docker** (preferably Docker Engine >= 20.10)
- **Docker Compose** (compose v2 syntax)
- **Python 3.10+** (optional, if running outside Docker)

## 2. Environment Variables

These environment variables can be set in your shell or in a `.env` file:

- `LLM_MODEL_ID`: Ollama model identifier (e.g., `llama3.2:1b`). Defaults to `"llama3.2:1b"`.
- `LLM_ENDPOINT_PORT`: Port on the host mapped to Ollama’s internal port 11434. Defaults to `8008`.
- `no_proxy`, `http_proxy`, `https_proxy`: Proxy settings, if needed.

## 3. How to Run

1. **Clone this repository** (or copy these files into your project).
2. **Build and start** via Docker Compose:
   ```sh
   docker compose up --build
