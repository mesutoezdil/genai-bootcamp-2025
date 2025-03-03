# OPEA Ollama: An In-Depth Guide

This document provides an extensive guide to using OPEA Ollama, including links to key resources, detailed instructions for setting up Ollama locally, and step-by-step commands for interacting with the model API. Whether you are testing locally or integrating with other systems like LangChain or OpenAI, this guide will walk you through each step.

---

## 1. Essential Resources

Below are several useful links related to OPEA and its components:

1. **[opea.dev](https://opea.dev/)**  
   The official website providing comprehensive information on OPEA and its projects.

2. **[Opea Project on GitHub](https://github.com/opea-project)**  
   Explore the source code and contributions to various OPEA projects.

3. **[Opea Comps Repository](https://github.com/opea-project/GenAIComps)**  
   A collection of microservices and components that power OPEA.

4. **[Opea Project Comps Documentation](https://opea-project.github.io/latest/GenAIComps/README.html)**  
   Detailed documentation for OPEA components, including setup and integration instructions.

5. **[Opea Tutorial](https://opea-project.github.io/latest/tutorial/index.html)**  
   A series of tutorials to help you get started with OPEA projects.

---

## 2. Setting Up Ollama Locally

Ollama provides an API interface to interact with language models locally. For more details on available models and API endpoints, refer to the [Ollama Models API Documentation](../ollama-models/README.md).

### 2.1 Determining Your Host IP

To set up Ollama, you first need to determine your host's IP address. This IP is used to expose the API endpoints and connect to the Ollama server.

#### Retrieve Local and Public IP Addresses

**For Local (Internal) IP:**

- **Wi-Fi (en0):**
  ```bash
  ipconfig getifaddr en0
  ```
- **Ethernet (en1):**
  ```bash
  ipconfig getifaddr en1
  ```

**For Detailed Network Information:**

```bash
ifconfig
```

**For Public (External) IP:**

- Using `curl` to obtain your public IP:
  ```bash
  curl ifconfig.me
  ```
- Or an alternative service:
  ```bash
  curl ipecho.net/plain
  ```

**Example Script to Retrieve and Display Your Host IP:**

```sh
HOST_IP=$(curl ifconfig.me)
echo "HOST_IP: $HOST_IP"
```

*If you require IPv4 explicitly (in case of IPv6 responses):*

```sh
HOST_IP=$(curl -4 ifconfig.me)
echo "HOST_IP: $HOST_IP"
```

---

## 3. Running Ollama with Docker Compose

Before launching Ollama, set up some environment variables for configuring your container:

```sh
NO_PROXY=localhost
LLM_ENDPOINT_PORT=9000
LLM_MODEL_ID="llama3.2:3b"
```

You can then start the Docker containers with one of the following commands:

- **Basic Command (using default endpoint port):**
  ```sh
  host_ip=$HOST_IP no_proxy=$NO_PROXY LLM_MODEL_ID=$LLM_MODEL_ID docker-compose up -d
  ```

- **With Custom Endpoint Port:**
  ```sh
  host_ip=$HOST_IP no_proxy=$NO_PROXY LLM_ENDPOINT_PORT=$LLM_ENDPOINT_PORT LLM_MODEL_ID=$LLM_MODEL_ID docker-compose up -d
  ```

These commands configure your container environment with your host IP, disable proxy for localhost, and specify the model ID and endpoint port.

---

## 4. Managing Models with Ollama

### 4.1 Downloading (Pulling) a Model

To download or update a model locally, use one of the following commands:

- **Using HTTP API:**
  ```sh
  curl http://localhost:8008/api/pull -d '{ "model": "llama3.2:3b" }'
  ```

- **Using Docker Exec:**
  ```sh
  docker exec -it ollama-server ollama pull llama3.2:3b
  ```

### 4.2 Listing Available Models

To view the list of models available on your Ollama server, you can issue a request:

#### Via HTTP API:

```sh
curl http://localhost:8008/api/tags | python -m json.tool
```

This returns a JSON object similar to:

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

#### Or by using Docker Exec:

```sh
docker exec -it ollama-server ollama list
```

This command outputs a table like:

```
NAME           ID              SIZE      MODIFIED
llama3.2:3b    a80c4f17acd5    2.0 GB    About a minute ago
```

---

## 5. Generating Responses

### 5.1 Basic Response Generation

You can send a prompt to the model and receive a generated response using the following command:

```sh
curl -X POST http://localhost:8008/api/generate \
     -H "Content-Type: application/json" \
     -d '{"model": "llama3.2:3b", "prompt": "Why is the sky blue?"}'
```

#### Sample Response:

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

### 5.2 Non-Streaming Response Mode

When streaming is disabled, the response will be delivered as a single JSON object:

```sh
curl http://localhost:8008/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Why is the sky blue?",
  "stream": false
}' | python -m json.tool
```

#### Expected Response:

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

## 6. Chat Completions

You can also engage in a chat-based conversation with the model.

### 6.1 Generate a Chat Completion (Non-Streaming)

Send a series of messages to simulate a conversation:

```sh
curl http://localhost:8008/api/chat -d '{
  "model": "llama3.2:3b",
  "messages": [{"role": "user", "content": "Why is the sky blue?"}],
  "stream": false
}' | python -m json.tool
```

#### Sample Chat Response:

```json
{
    "model": "llama3.2:3b",
    "created_at": "2025-02-20T12:55:12.803987408Z",
    "message": {
        "role": "assistant",
        "content": "The sky appears blue because of a phenomenon called Rayleigh scattering, ... (detailed explanation)"
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

You can modify the message content to explore different queries. For example:

```sh
curl http://localhost:8008/api/chat -d '{
  "model": "llama3.2:3b",
  "messages": [{"role": "user", "content": "What are LLMs, Agents and RAG?"}],
  "stream": false
}' | python -m json.tool
```

#### Detailed Chat Response:

```json
{
    "model": "llama3.2:3b",
    "created_at": "2025-02-20T16:05:24.324253789Z",
    "message": {
        "role": "assistant",
        "content": "LLMs (Large Language Models), Agents, and RAG are all related concepts in AI... (detailed explanation)"
    },
    "done_reason": "stop",
    "done": true,
    "total_duration": 83143571850,
    "load_duration": 36057011197,
    "prompt_eval_count": 36,
    "prompt_eval_duration": 2376000000,
    "eval_count": 357,
    "eval_duration": 44701000000
}
```

---

## 7. Testing the API with LangChain and OpenAI

For advanced integrations, such as using LangChain or OpenAI's API framework, you can run:

```sh
python chatopenai_langchain_ollama.py
```

This script demonstrates how to interact with the Ollama API using LangChain, providing a bridge between different language model interfaces.

---

## Conclusion

This comprehensive guide has walked you through the setup and use of OPEA Ollama locally. You now know how to:
- Retrieve your host IP address.
- Configure and run Docker Compose for Ollama.
- Pull and list models.
- Generate responses via REST API.
- Engage in chat-based interactions.
- Test API integrations using LangChain and OpenAI.

By following these steps, you can effectively deploy and interact with your local Ollama instance, unlocking the full potential of your language models.

Happy exploring and building with OPEA Ollama!
