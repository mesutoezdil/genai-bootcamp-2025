import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ChatConfig(BaseModel):
    """Configuration for Chat QA system."""
    api_key: str
    model_name: str
    max_tokens: int
    temperature: float
    system_prompt: str
    requests_per_minute: int
    retry_limit: int
    retry_initial_delay: float

    @classmethod
    def from_env(cls) -> "ChatConfig":
        """Create configuration from environment variables."""
        return cls(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            model_name=os.getenv("MODEL_NAME", "gpt-4-turbo-preview"),
            max_tokens=int(os.getenv("MAX_TOKENS", "4000")),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            system_prompt=os.getenv("SYSTEM_PROMPT", "You are a helpful assistant."),
            requests_per_minute=int(os.getenv("REQUESTS_PER_MINUTE", "50")),
            retry_limit=int(os.getenv("RETRY_LIMIT", "3")),
            retry_initial_delay=float(os.getenv("RETRY_INITIAL_DELAY", "1.0"))
        )
