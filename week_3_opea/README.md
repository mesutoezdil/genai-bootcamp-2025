# OPEA Ollama: An In-Depth Guide

This repository contains comprehensive information and step-by-step instructions on how to set up, configure, and utilize **OPEA Ollama** for running language models locally. Whether you aim to test Ollama with Docker, integrate it into larger ecosystems (LangChain, OpenAI, etc.), or simply experiment with model APIs, this guide aims to cover it all.

<br/>

## Table of Contents

1. [Overview](#1-overview)  
2. [Key Features](#2-key-features)  
3. [Project Structure](#3-project-structure)  
4. [Prerequisites](#4-prerequisites)  
5. [Installation and Setup](#5-installation-and-setup)  
   1. [Local IP Configuration](#51-local-ip-configuration)  
   2. [Environment Variables](#52-environment-variables)  
   3. [Launching via Docker Compose](#53-launching-via-docker-compose)  
6. [Model Management](#6-model-management)  
   1. [Pulling (Downloading) a Model](#61-pulling-downloading-a-model)  
   2. [Listing Models](#62-listing-models)  
7. [Generating Responses](#7-generating-responses)  
   1. [Basic Response Generation](#71-basic-response-generation)  
   2. [Non-Streaming Responses](#72-non-streaming-responses)  
8. [Chat Completions](#8-chat-completions)  
   1. [Generate a Chat Completion (Non-Streaming)](#81-generate-a-chat-completion-non-streaming)  
9. [Advanced Usage](#9-advanced-usage)  
   1. [LangChain & OpenAI Integrations](#91-langchain--openai-integrations)  
   2. [Handling Errors & Troubleshooting](#92-handling-errors--troubleshooting)  
10. [Examples](#10-examples)  
11. [Testing](#11-testing)  
12. [Contributing](#12-contributing)  
13. [License](#13-license)  
14. [Contact & Support](#14-contact--support)  

---

## 1. Overview

**OPEA Ollama** is an API interface designed to facilitate seamless local interaction with large language models. It is part of the larger [OPEA](https://opea.dev/) ecosystem, which includes various microservices, tools, and tutorials that you can use to create powerful AI-driven applications.

By following this guide, you will learn how to:

- Configure your system’s IP to expose Ollama’s HTTP endpoints.  
- Deploy Ollama with Docker Compose, including environment variable customization.  
- Pull and list available models for offline usage.  
- Generate responses via RESTful API or chat endpoints.  
- Integrate Ollama with external frameworks like LangChain or OpenAI.  

---

## 2. Key Features

- **Local Deployment**: Run language models fully offline or within your internal network.
- **Docker Compose Integration**: Rapidly configure and launch services without installing dependencies directly on your machine.
- **Multiple Model Support**: Manage various models (e.g., `llama3.2:3b`) effortlessly, switch between them, and list what’s installed.
- **RESTful APIs**: Standard HTTP endpoints for generating text and chat-based conversations.
- **Scalable Architecture**: Simple enough for personal projects yet flexible for large enterprise setups.
- **Seamless Integrations**: Built to work well with frameworks such as **LangChain** and **OpenAI**’s Python libraries.

---

## 3. Project Structure

A high-level look at this repository’s structure:

```
.
├── docker-compose.yaml               # Docker Compose configuration for Ollama
├── scripts/                          # Useful scripts for setup and environment variables
│   ├── init.sh                       # Example init script for environment variables
│   └── ...
├── src/                              # Source code or additional integrations
│   └── chatopenai_langchain_ollama.py
├── docs/                             # Additional documentation or references
│   └── ollama-models/README.md       # Specific doc for Ollama Models
├── tests/                            # (Optional) Testing scripts or test cases
├── .env.example                      # Example environment variable file
├── README.md                         # The file you're currently reading
└── ...
```

> **Note**: Your actual directory structure may vary based on your project’s needs. The above layout is a suggested organization that fosters clarity and ease of navigation.

---

## 4. Prerequisites

Before setting up **OPEA Ollama**, make sure you have:

1. **Docker & Docker Compose**  
   - [Docker Installation Guide](https://docs.docker.com/get-docker/)  
   - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)
2. **Basic Command-Line Knowledge**  
   - Comfort with running commands in a Terminal or PowerShell.
3. **(Optional) Python Environment**  
   - If you wish to run Python integration scripts such as `chatopenai_langchain_ollama.py`, you’ll need a recent Python 3.x version.

> **System Requirements**: Ensure you have enough RAM and disk space to accommodate the models (some can be multiple GB in size) and any local caching performed by Docker.

---

## 5. Installation and Setup

### 5.1 Local IP Configuration

The local IP address is required to expose the Ollama HTTP endpoints, especially if you plan to access the service from other machines on the same network.

#### Retrieving Your Local IP

- **Wi-Fi (en0)**:
  ```bash
  ipconfig getifaddr en0
  ```
- **Ethernet (en1)**:
  ```bash
  ipconfig getifaddr en1
  ```

> **Mac/Linux Users** can also run `ifconfig` to get a full network configuration.

#### Public (External) IP

If you need an externally accessible endpoint, get your public IP:
```bash
curl ifconfig.me
```
or
```bash
curl ipecho.net/plain
```

**Example script to store the public IP in a variable**:
```bash
HOST_IP=$(curl -4 ifconfig.me)
echo "HOST_IP: $HOST_IP"
```

---

### 5.2 Environment Variables

Customize your environment by setting the following variables either in a `.env` file or directly in your shell:

- **`HOST_IP`**: IP address of the host machine.  
- **`NO_PROXY`**: Typically `localhost` or `127.0.0.1` to bypass any system proxy.  
- **`LLM_ENDPOINT_PORT`**: Port on which Ollama will expose its API (default `8008` or custom).  
- **`LLM_MODEL_ID`**: Identifies the model to pull and run (e.g., `llama3.2:3b`).  

Example usage in your shell:
```bash
export HOST_IP=$(curl -4 ifconfig.me)
export NO_PROXY="localhost"
export LLM_ENDPOINT_PORT=9000
export LLM_MODEL_ID="llama3.2:3b"
```

---

### 5.3 Launching via Docker Compose

After setting environment variables, you can bring up the Ollama service with Docker Compose:

1. **Basic Command** (Default Port)
   ```bash
   host_ip=$HOST_IP \
   no_proxy=$NO_PROXY \
   LLM_MODEL_ID=$LLM_MODEL_ID \
   docker-compose up -d
   ```

2. **Custom Endpoint Port**
   ```bash
   host_ip=$HOST_IP \
   no_proxy=$NO_PROXY \
   LLM_ENDPOINT_PORT=$LLM_ENDPOINT_PORT \
   LLM_MODEL_ID=$LLM_MODEL_ID \
   docker-compose up -d
   ```

> The `-d` flag runs containers in detached mode. Omit it if you prefer interactive logs.

You should now have **Ollama** running inside a Docker container, accessible via `http://<HOST_IP>:<LLM_ENDPOINT_PORT>/api/`.

---

## 6. Model Management

### 6.1 Pulling (Downloading) a Model

Ollama allows you to pull specific models either via HTTP or directly from the Docker container.

1. **Using the HTTP API**:
   ```bash
   curl http://localhost:8008/api/pull -d '{ "model": "llama3.2:3b" }'
   ```

2. **Inside the Docker Container**:
   ```bash
   docker exec -it ollama-server ollama pull llama3.2:3b
   ```

> Pulling large models for the first time can take a while. Make sure you have sufficient disk space.

---

### 6.2 Listing Models

After pulling one or more models, confirm their availability.

1. **Via HTTP API**:
   ```bash
   curl http://localhost:8008/api/tags | python -m json.tool
   ```
   Sample JSON output:
   ```json
   {
       "models": [
           {
               "name": "llama3.2:3b",
               "model": "llama3.2:3b",
               "modified_at": "2025-02-20T12:36:19.297875645Z",
               "size": 2019393189,
               "digest": "a80c4f17acd55265feec403c7aef86be0c25983ab279d83f3bcd3abbcb5b8b72",
               "details": {
                   "parent_model": "",
                   "format": "gguf",
                   "family": "llama",
                   "families": ["llama"],
                   "parameter_size": "3.2B",
                   "quantization_level": "Q4_K_M"
               }
           }
       ]
   }
   ```

2. **Using Docker Exec**:
   ```bash
   docker exec -it ollama-server ollama list
   ```
   Typical table output:
   ```
   NAME           ID              SIZE      MODIFIED
   llama3.2:3b    a80c4f17acd5    2.0 GB    About a minute ago
   ```

---

## 7. Generating Responses

### 7.1 Basic Response Generation

Send a JSON payload with a prompt to generate text:

```bash
curl -X POST http://localhost:8008/api/generate \
     -H "Content-Type: application/json" \
     -d '{"model": "llama3.2:3b", "prompt": "Why is the sky blue?"}'
```

Sample (streamed) response:
```json
{
  "model": "llama3.2",
  "created_at": "2023-08-04T19:22:45.499127Z",
  "response": "",
  "done": true,
  "context": [1, 2, 3],
  "total_duration": 10706818083,
  "load_duration": 6338219291,
  "prompt_eval_count": 26,
  "prompt_eval_duration": 130079000,
  "eval_count": 259,
  "eval_duration": 4232710000
}
```

> If streaming is enabled, the response may come back in chunks. Typically, your client would read these chunks until `done` is `true`.

---

### 7.2 Non-Streaming Responses

Disable streaming to receive a single JSON object:

```bash
curl http://localhost:8008/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Why is the sky blue?",
  "stream": false
}' | python -m json.tool
```

Example response:
```json
{
  "model": "llama3.2",
  "created_at": "2023-08-04T19:22:45.499127Z",
  "response": "The sky is blue because it is the color of the sky.",
  "done": true,
  "context": [1, 2, 3],
  "total_duration": 5043500667,
  "load_duration": 5025959,
  "prompt_eval_count": 26,
  "prompt_eval_duration": 325953000,
  "eval_count": 290,
  "eval_duration": 4709213000
}
```

---

## 8. Chat Completions

### 8.1 Generate a Chat Completion (Non-Streaming)

Ollama also supports a chat-like format, sending multiple messages in a conversation array:

```bash
curl http://localhost:8008/api/chat -d '{
  "model": "llama3.2:3b",
  "messages": [{"role": "user", "content": "Why is the sky blue?"}],
  "stream": false
}' | python -m json.tool
```

Example result:
```json
{
    "model": "llama3.2:3b",
    "created_at": "2025-02-20T12:55:12.803987408Z",
    "message": {
        "role": "assistant",
        "content": "The sky appears blue because of a phenomenon called Rayleigh scattering, ..."
    },
    "done_reason": "stop",
    "done": true,
    "total_duration": 28842545447,
    "load_duration": 34789034,
    "prompt_eval_count": 31,
    "prompt_eval_duration": 335000000,
    "eval_count": 275,
    "eval_duration": 28470000000
}
```

Adjust your message content to ask anything:
```bash
curl http://localhost:8008/api/chat -d '{
  "model": "llama3.2:3b",
  "messages": [{"role": "user", "content": "What are LLMs, Agents and RAG?"}],
  "stream": false
}' | python -m json.tool
```

---

## 9. Advanced Usage

### 9.1 LangChain & OpenAI Integrations

For more complex integrations, such as bridging **LangChain** or **OpenAI**:

```bash
python src/chatopenai_langchain_ollama.py
```

- **LangChain**: Provides advanced chaining of prompts, memory, and data retrieval.  
- **OpenAI API**: Simulate or replace calls to OpenAI endpoints with your local Ollama instance, saving on API calls while retaining similar usage patterns.

### 9.2 Handling Errors & Troubleshooting

1. **Port Conflicts**:  
   If `8008` or your chosen port is in use, change `LLM_ENDPOINT_PORT` in your environment variables and re-run Docker Compose.
2. **Insufficient Memory**:  
   Large models can require significant RAM. Check your Docker settings (e.g., Docker Desktop > Resources) to allocate enough memory.
3. **Network Issues**:  
   - Ensure `HOST_IP` is correctly set.  
   - If you’re behind a proxy, confirm `NO_PROXY="localhost,127.0.0.1,<YOUR_HOST_IP>"` to prevent routing local traffic through the proxy.
4. **Model Pull Failure**:  
   Verify your internet connection and that the model name (`llama3.2:3b`) is spelled correctly.  
   Some firewalls or security software may block large file downloads; consider whitelisting or using a VPN.

> **Tip**: Use `docker logs ollama-server` to see any runtime error messages in the Ollama container.

---

## 10. Examples

Below are some quick commands that illustrate typical usage patterns:

1. **Pull a Model**:
   ```bash
   curl http://localhost:8008/api/pull -d '{ "model": "llama3.2:3b" }'
   ```
2. **Generate Basic Response**:
   ```bash
   curl -X POST http://localhost:8008/api/generate \
        -H "Content-Type: application/json" \
        -d '{"model": "llama3.2:3b", "prompt": "Hello, world!"}'
   ```
3. **Chat Mode**:
   ```bash
   curl -X POST http://localhost:8008/api/chat \
        -H "Content-Type: application/json" \
        -d '{
          "model": "llama3.2:3b",
          "messages": [{"role": "user", "content": "Tell me a fun fact about cats."}],
          "stream": false
        }'
   ```
4. **List Models**:
   ```bash
   docker exec -it ollama-server ollama list
   ```

---

## 11. Testing

If you have a testing strategy or suite, document it here. For instance:

- **Unit Tests**: Located in a `tests/` directory, run them with:
  ```bash
  pytest tests/
  ```
- **Integration Tests**: Scripts verifying end-to-end Ollama functionality, e.g.:
  ```bash
  bash tests/integration_test.sh
  ```
- **Continuous Integration (CI)**: If using GitHub Actions or another CI system, describe how your build pipeline is triggered and tested.

> Keeping tests updated ensures consistent reliability and catches regressions early.

---

## 12. Contributing

Contributions are welcome! If you’d like to add features, fix bugs, or enhance documentation:

1. **Fork** this repository.  
2. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/my-awesome-improvement
   ```
3. **Commit** changes and **push** to your branch:
   ```bash
   git commit -m "Add new feature"
   git push origin feature/my-awesome-improvement
   ```
4. **Open a Pull Request (PR)** describing your changes, including relevant screenshots or logs.  

> Please follow any coding standards or linters defined in the repository. For major changes, open an issue first to discuss your idea.

---

## 13. License

Include your chosen license here (e.g., [MIT](https://opensource.org/licenses/MIT), [Apache 2.0](https://opensource.org/licenses/Apache-2.0), etc.). A common format is:

```
MIT License

Copyright (c) 2025, Mesut Oezdil

Permission is hereby granted, free of charge, to any person obtaining a copy ...
```

Make sure to place a full `LICENSE` file in the root of the repository.

---

## 14. Contact & Support

For any questions, bug reports, or feature requests:

- Submit an issue on [GitHub Issues](https://github.com/opea-project/GenAIComps/issues).  
- Reach out via email: `contact@opea.dev` (replace with your actual support email if different).  
- Check the official website [opea.dev](https://opea.dev/) for further documentation and community links.

You’re also welcome to explore:
- [Opea Project on GitHub](https://github.com/opea-project)
- [Opea Comps Repository](https://github.com/opea-project/GenAIComps)
- [Opea Project Comps Documentation](https://opea-project.github.io/latest/GenAIComps/README.html)
- [Opea Tutorial](https://opea-project.github.io/latest/tutorial/index.html)

---

### Final Remarks

By following the steps and best practices outlined in this guide, you should be well-equipped to deploy and manage **OPEA Ollama** locally, integrate it into your AI applications, and collaborate within the OPEA ecosystem. Continue exploring additional examples and advanced configurations to unlock even more potential from your local language model instance.
