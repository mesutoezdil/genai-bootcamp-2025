from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from datetime import datetime

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    created_at: datetime = datetime.now()
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = {}
    subtasks: List["Task"] = []
    parent_id: Optional[str] = None

class ThinkResult(BaseModel):
    plan: List[str]
    required_tools: List[str]
    estimated_steps: int
    risks: List[str]

class ActionResult(BaseModel):
    success: bool
    output: Any
    error: Optional[str] = None
    metrics: Dict[str, Any] = {}

class ObservationResult(BaseModel):
    matches_expected: bool
    differences: List[str]
    metrics: Dict[str, Any] = {}

class RefinementResult(BaseModel):
    adjustments: List[str]
    new_plan: Optional[List[str]] = None
