import time
import uuid
from typing import List, Dict, Any, Optional
from openai import OpenAI, RateLimitError
from tenacity import retry, stop_after_attempt, wait_exponential
import tiktoken

from .config import ChatConfig
from .models import Conversation, Message

class QASystem:
    """QA system using OpenAI's chat models."""
    
    def __init__(self, config: ChatConfig):
        """Initialize the QA system."""
        self.config = config
        self.client = OpenAI(api_key=config.api_key)
        self.conversations: Dict[str, Conversation] = {}
        self.last_request_time = 0
        self.encoding = tiktoken.encoding_for_model(config.model_name)
    
    def _count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoding.encode(text))
    
    def _rate_limit(self) -> None:
        """Implement rate limiting."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        min_interval = 60.0 / self.config.requests_per_minute
        
        if time_since_last_request < min_interval:
            time.sleep(min_interval - time_since_last_request)
        
        self.last_request_time = time.time()
    
    def create_conversation(self) -> str:
        """Create a new conversation."""
        conv_id = str(uuid.uuid4())
        self.conversations[conv_id] = Conversation(id=conv_id)
        return conv_id
    
    def get_conversation(self, conv_id: str) -> Optional[Conversation]:
        """Get a conversation by ID."""
        return self.conversations.get(conv_id)
    
    def _prepare_messages(self, conversation: Conversation) -> List[Dict[str, str]]:
        """Prepare messages for the API call."""
        messages = [{"role": "system", "content": self.config.system_prompt}]
        
        for msg in conversation.get_context_window():
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        return messages
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    async def get_answer(self, conv_id: str, question: str) -> str:
        """Get an answer to a question."""
        conversation = self.get_conversation(conv_id)
        if not conversation:
            raise ValueError(f"Conversation {conv_id} not found")
        
        # Add user question
        conversation.add_message("user", question)
        
        # Prepare messages
        messages = self._prepare_messages(conversation)
        
        # Rate limit
        self._rate_limit()
        
        try:
            # Get completion
            response = await self.client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            # Extract answer
            answer = response.choices[0].message.content
            
            # Add assistant response
            conversation.add_message("assistant", answer)
            
            return answer
            
        except RateLimitError as e:
            print(f"Rate limit exceeded: {e}")
            raise
            
        except Exception as e:
            print(f"Error in chat completion: {e}")
            raise
