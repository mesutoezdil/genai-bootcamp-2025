from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Message(BaseModel):
    """A chat message."""
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

class Conversation(BaseModel):
    """A conversation consisting of multiple messages."""
    id: str
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def add_message(self, role: str, content: str) -> None:
        """Add a new message to the conversation."""
        self.messages.append(Message(role=role, content=content))
        self.updated_at = datetime.now()
    
    def get_context_window(self, max_messages: int = 10) -> List[Message]:
        """Get the most recent messages as context."""
        return self.messages[-max_messages:]
