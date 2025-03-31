# OPEA LLM Mega-Service

This repository hosts an **advanced Ollama-based LLM** service, containerized with **Docker** and orchestrated using **Docker Compose**. It pairs a robust **FastAPI** application with the **Ollama** server to deliver enhanced text generation, improved model management, and better overall reliability.

---

## Table of Contents

1. [Overview](#1-overview)  
2. [Key Improvements](#2-key-improvements)  
3. [Prerequisites](#3-prerequisites)  
4. [Environment Variables](#4-environment-variables)  
5. [Getting Started](#5-getting-started)  
   1. [Clone & Build](#51-clone--build)  
   2. [Verify Service](#52-verify-service)  
6. [API Endpoints](#6-api-endpoints)  
   1. [Root Endpoint (`GET /`)](#61-root-endpoint-get-)  
   2. [Generate Text (`POST /v1/generate`)](#62-generate-text-post-v1generate)  
   3. [Pull Model (`POST /v1/pull`)](#63-pull-model-post-v1pull)  
   4. [List Models (`GET /v1/models`)](#64-list-models-get-v1models)

---

## 1. Overview

The **OPEA LLM Mega-Service** is designed to streamline large language model (LLM) interactions using **Ollama**. It provides:

- **Text Generation**: Make requests to generate text based on a prompt.  
- **Model Pulling & Management**: Dynamically download and cache new models.  
- **Model Listing**: Retrieve a list of currently installed models.

This approach maintains the **core functionality** from the original project while adding modular enhancements to improve scalability, reliability, and developer experience.

---

## 2. Key Improvements

1. **Advanced Logging & Error Handling**  
   - Detailed logs (e.g., request/response cycles, exceptions) help diagnose issues quickly in both development and production.
   - Dedicated exception handlers in FastAPI produce clear JSON error responses.

2. **Request Validation with Pydantic**  
   - Incoming API requests (e.g., text generation prompts) are validated against **Pydantic models**, guaranteeing consistent data formats.
   - Automatically generates user-friendly Swagger documentation for each endpoint.

3. **Additional Endpoints**  
   - **`/v1/models`** lists all currently installed models, providing better insight and control over the system’s available LLMs.

4. **Modular & Future-Proof Architecture**  
   - **Docker & Docker Compose** handle service orchestration, environment variables, and networking.
   - Clear separation of concerns: 
     - **Ollama** container for LLM functionalities  
     - **my-app** container for FastAPI-based API logic  

---

## 3. Prerequisites

- **Docker**: Recommended Engine version **>= 20.10**.  
- **Docker Compose**: Using the **compose v2** syntax.  
- **Python 3.10+**: Needed if you plan to run or extend the FastAPI application outside of Docker.

---

## 4. Environment Variables

Configure these variables either in your shell or within a **`.env`** file for Docker Compose to pick up:

- **`LLM_MODEL_ID`**: The **default** Ollama model ID (e.g., `"llama3.2:1b"`).  
  - Defaults to `"llama3.2:1b"` if not provided.  
- **`LLM_ENDPOINT_PORT`**: Host port mapped to Ollama’s internal port **11434**.  
  - Defaults to **`8008`**.  
- **`no_proxy`, `http_proxy`, `https_proxy`**: Set these if your environment requires proxy configuration.  
- **`OLLAMA_SERVER_HOST`, `OLLAMA_SERVER_PORT`**: Automatically set by Docker Compose for internal container networking. Usually shouldn’t be changed manually.

---

## 5. Getting Started

### 5.1 Clone & Build

1. **Clone this repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Launch Docker Compose**:
   ```bash
   docker compose up --build
   ```
   This will:
   - **Build** the `my-app` container for FastAPI.  
   - **Pull** and run the `ollama-server` container for LLM operations.

### 5.2 Verify Service

- Once the containers are up, open your browser at [http://localhost:8000](http://localhost:8000). You should see a simple JSON welcome message:
  ```json
  {"message": "Welcome to the advanced OPEA LLM mega-service!"}
  ```
- Check the **Swagger UI** at [http://localhost:8000/docs](http://localhost:8000/docs) to explore endpoints and experiment with requests.

---

## 6. API Endpoints

All routes are served by the **FastAPI** application running at **port 8000** (unless overridden).

### 6.1 Root Endpoint (`GET /`)

- **Description**:  
  Simple health check or “welcome” endpoint. Indicates that the FastAPI service is running.

- **Response Example**:
  ```json
  {
    "message": "Welcome to the advanced OPEA LLM mega-service!"
  }
  ```

---

### 6.2 Generate Text (`POST /v1/generate`)

- **Purpose**:  
  Send a prompt to the Ollama server for text completion or generation.

- **Request Body Example**:
  ```json
  {
    "model": "llama3.2:1b",
    "prompt": "Why is the sky blue?"
  }
  ```
  - If `model` is omitted, **`LLM_MODEL_ID`** is used by default.

- **Response**:
  ```json
  {
    "model": "llama3.2:1b",
    "response": "The sky appears blue due to Rayleigh scattering..."
  }
  ```

- **Use Cases**:
  - Chatbot-like conversations.  
  - Generating short text completions or answers.

---

### 6.3 Pull Model (`POST /v1/pull`)

- **Purpose**:  
  Download a specific model into the Ollama server’s cache.

- **Request Body Example**:
  ```json
  {
    "model": "llama3.2:1b"
  }
  ```
  - Again, if `model` is missing, the default from `LLM_MODEL_ID` is used.

- **Response**:
  ```json
  {
    "status": "Model llama3.2:1b pulled successfully."
  }
  ```

- **When to Use**:
  - Adding a **new** model to the system so it can be used in subsequent generation requests.

---

### 6.4 List Models (`GET /v1/models`)

- **Purpose**:  
  Retrieves a **list** of all models currently available in the Ollama server’s cache.

- **Response Example**:
  ```json
  {
    "models": [
      {
        "name": "llama3.2:1b",
        "lastModified": "2025-03-12T09:22:11Z"
      },
      {
        "name": "alpaca:7b",
        "lastModified": "2025-03-14T10:05:47Z"
      }
    ]
  }
  ```

- **Use Cases**:
  - Verifying which models are installed before deciding which to use for text generation.  
  - Debugging or monitoring the system.

