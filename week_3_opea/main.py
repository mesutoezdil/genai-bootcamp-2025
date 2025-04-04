from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn

from openai_client import OpenAIClient, OpenAIConfig

# Initialize FastAPI app
app = FastAPI(
    title="OpenAI API Integration",
    description="A robust OpenAI API integration with rate limiting and best practices",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
config = OpenAIConfig.from_env()
client = OpenAIClient(config)

# Request/Response models
class ChatRequest(BaseModel):
    messages: List[Dict[str, str]]
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    stream: bool = False

class EmbeddingRequest(BaseModel):
    text: str

class ModerationRequest(BaseModel):
    text: str

@app.post("/chat")
async def create_chat_completion(request: ChatRequest):
    """Create a chat completion."""
    try:
        response = await client.chat_completion(
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=request.stream
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/embed")
async def create_embedding(request: EmbeddingRequest):
    """Create text embeddings."""
    try:
        embedding = await client.embed_text(request.text)
        return {"embedding": embedding}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/moderate")
async def moderate_content(request: ModerationRequest):
    """Check content for potential violations."""
    try:
        result = await client.moderate_text(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
