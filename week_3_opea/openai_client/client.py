from typing import List, Optional, Dict, Any
import time
from openai import OpenAI, RateLimitError
from tenacity import retry, stop_after_attempt, wait_exponential
import tiktoken

from .config import OpenAIConfig

class OpenAIClient:
    """
    A robust OpenAI API client with rate limiting, retries, and token counting.
    """
    
    def __init__(self, config: OpenAIConfig):
        """Initialize the OpenAI client with configuration."""
        self.config = config
        self.client = OpenAI(api_key=config.api_key)
        self.last_request_time = 0
        self.encoding = tiktoken.encoding_for_model(config.model_name)
        
    def _count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text string."""
        return len(self.encoding.encode(text))
    
    def _rate_limit(self) -> None:
        """Implement rate limiting."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        min_interval = 60.0 / self.config.requests_per_minute
        
        if time_since_last_request < min_interval:
            time.sleep(min_interval - time_since_last_request)
            
        self.last_request_time = time.time()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Any:
        """
        Send a chat completion request to OpenAI with automatic retries and rate limiting.
        
        Args:
            messages: List of message dictionaries (role, content)
            temperature: Override default temperature
            max_tokens: Override default max tokens
            stream: Whether to stream the response
            
        Returns:
            OpenAI chat completion response
        """
        self._rate_limit()
        
        # Count total tokens in messages
        total_tokens = sum(self._count_tokens(msg["content"]) for msg in messages)
        if total_tokens > self.config.max_tokens:
            raise ValueError(f"Input tokens ({total_tokens}) exceed maximum ({self.config.max_tokens})")
        
        try:
            response = await self.client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                temperature=temperature or self.config.temperature,
                max_tokens=max_tokens or self.config.max_tokens,
                stream=stream
            )
            return response
            
        except RateLimitError as e:
            print(f"Rate limit exceeded: {e}")
            raise
            
        except Exception as e:
            print(f"Error in chat completion: {e}")
            raise
    
    async def embed_text(self, text: str) -> List[float]:
        """
        Get embeddings for a text string.
        
        Args:
            text: Text to embed
            
        Returns:
            List of embedding values
        """
        self._rate_limit()
        
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
            
        except Exception as e:
            print(f"Error in text embedding: {e}")
            raise
    
    async def moderate_text(self, text: str) -> Dict[str, Any]:
        """
        Check text for potentially harmful content.
        
        Args:
            text: Text to moderate
            
        Returns:
            Moderation results
        """
        self._rate_limit()
        
        try:
            response = await self.client.moderations.create(input=text)
            return response.results[0]
            
        except Exception as e:
            print(f"Error in content moderation: {e}")
            raise
