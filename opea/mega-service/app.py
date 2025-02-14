import os
import requests
from fastapi import FastAPI, Request

app = FastAPI()

OLLAMA_SERVER_HOST = os.getenv("OLLAMA_SERVER_HOST", "localhost")
OLLAMA_SERVER_PORT = os.getenv("OLLAMA_SERVER_PORT", "11434")
OLLAMA_API_GENERATE = f"http://{OLLAMA_SERVER_HOST}:{OLLAMA_SERVER_PORT}/api/generate"
OLLAMA_API_PULL = f"http://{OLLAMA_SERVER_HOST}:{OLLAMA_SERVER_PORT}/api/pull"


@app.get("/")
def read_root():
    return {"message": "Welcome to the improved OPEA LLM service!"}


@app.post("/v1/generate")
async def generate_text(request: Request):
    """
    Accepts a JSON payload containing:
    {
      "model": "some-model-id",
      "prompt": "User question or message"
      ...
    }
    and sends it to Ollama's /api/generate endpoint.
    """
    data = await request.json()

    # Make sure we include a default model ID if none is provided in the request
    if "model" not in data:
        data["model"] = os.getenv("LLM_MODEL_ID", "llama3.2:1b")

    response = requests.post(OLLAMA_API_GENERATE, json=data)
    return response.json()


@app.post("/v1/pull")
async def pull_model(request: Request):
    """
    Pulls a new model into Ollama's cache.
    Example request payload:
    {
      "model": "llama3.2:1b"
    }
    """
    data = await request.json()
    response = requests.post(OLLAMA_API_PULL, json=data)
    return {
        "requested_model": data.get("model"),
        "ollama_response": response.json()
    }
