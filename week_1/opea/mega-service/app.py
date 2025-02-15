import os
import logging
import requests
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# ---------------------------------------------------------
# FastAPI Application Definition
# ---------------------------------------------------------
app = FastAPI(
    title="OPEA LLM Mega-Service",
    description="A more advanced FastAPI application that interacts with the Ollama server for text generation.",
    version="1.0.0"
)

# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Environment Variables
# ---------------------------------------------------------
OLLAMA_SERVER_HOST = os.getenv("OLLAMA_SERVER_HOST", "localhost")
OLLAMA_SERVER_PORT = os.getenv("OLLAMA_SERVER_PORT", "11434")
DEFAULT_MODEL_ID = os.getenv("LLM_MODEL_ID", "llama3.2:1b")

OLLAMA_API_GENERATE = f"http://{OLLAMA_SERVER_HOST}:{OLLAMA_SERVER_PORT}/api/generate"
OLLAMA_API_PULL = f"http://{OLLAMA_SERVER_HOST}:{OLLAMA_SERVER_PORT}/api/pull"
OLLAMA_API_MODELS = f"http://{OLLAMA_SERVER_HOST}:{OLLAMA_SERVER_PORT}/api/models"

# ---------------------------------------------------------
# Pydantic Models (Optional but Recommended)
# ---------------------------------------------------------
class GenerateRequest(BaseModel):
    model: Optional[str] = None
    prompt: str

class PullRequest(BaseModel):
    model: Optional[str] = None

# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------
@app.get("/", tags=["General"])
def read_root():
    """
    A simple health-check or welcome endpoint.
    """
    logger.info("Accessed root endpoint.")
    return {"message": "Welcome to the advanced OPEA LLM mega-service!"}

# ---------------------------------------------------------
# /v1/generate Endpoint
# ---------------------------------------------------------
@app.post("/v1/generate", tags=["Ollama"])
def generate_text(req_body: GenerateRequest):
    """
    Sends a prompt to the Ollama server for text generation.

    Request Body Example:
    {
      "model": "llama3.2:1b",
      "prompt": "Why is the sky blue?"
    }

    - model (optional): The specific LLM model you want to use.
    - prompt: The text or question you want the LLM to generate a response for.
    """
    model_to_use = req_body.model if req_body.model else DEFAULT_MODEL_ID
    payload = {
        "model": model_to_use,
        "prompt": req_body.prompt
    }

    logger.info(f"Generating text with model='{model_to_use}', prompt='{req_body.prompt[:30]}...'")
    response = requests.post(OLLAMA_API_GENERATE, json=payload)

    if response.status_code != 200:
        logger.error(f"Generation failed: {response.status_code}, {response.text}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Text generation request failed",
                "response": response.text
            }
        )

    return response.json()

# ---------------------------------------------------------
# /v1/pull Endpoint
# ---------------------------------------------------------
@app.post("/v1/pull", tags=["Ollama"])
def pull_model(req_body: PullRequest):
    """
    Pulls (downloads) a new model into the Ollama server's cache.

    Request Body Example:
    {
      "model": "llama3.2:1b"
    }

    - model (optional): The model ID you want to download. If not provided, the default model is used.
    """
    model_to_pull = req_body.model if req_body.model else DEFAULT_MODEL_ID
    logger.info(f"Pulling model: {model_to_pull}")
    response = requests.post(OLLAMA_API_PULL, json={"model": model_to_pull})

    if response.status_code != 200:
        logger.error(f"Model pull failed: {response.status_code}, {response.text}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Model pull request failed",
                "response": response.text
            }
        )

    return {
        "requested_model": model_to_pull,
        "ollama_response": response.json()
    }

# ---------------------------------------------------------
# /v1/models Endpoint (Optional)
# ---------------------------------------------------------
@app.get("/v1/models", tags=["Ollama"])
def list_models():
    """
    Lists models currently available or cached on the Ollama server.

    Useful for checking which models are ready to be used.
    """
    logger.info("Listing models via Ollama's /api/models endpoint.")
    try:
        resp = requests.get(OLLAMA_API_MODELS)
        if resp.status_code != 200:
            logger.warning(f"Failed to retrieve Ollama models list: {resp.text}")
            raise HTTPException(
                status_code=500,
                detail={"error": "Unable to retrieve model list", "response": resp.text}
            )
        return resp.json()
    except requests.exceptions.RequestException as e:
        logger.exception("Error while calling Ollama's /api/models.")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Request to Ollama's /api/models failed",
                "info": str(e)
            }
        )

# ---------------------------------------------------------
# Exception Handlers
# ---------------------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Invalid request format. Please ensure all required parameters are provided.",
            "errors": exc.errors()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred on the server."}
    )