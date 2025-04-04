from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime

from agent import Agent, Task, TaskStatus, TaskPriority
from tools import WebSearchTool, CalculatorTool, WeatherTool, TextProcessingTool

# Initialize FastAPI app
app = FastAPI(
    title="Agential Workflow System",
    description="A system demonstrating the Think → Act → Observe → Refine workflow",
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

# Initialize agent and register tools
agent = Agent("WorkflowAgent")
agent.register_tool("web_search", WebSearchTool())
agent.register_tool("calculator", CalculatorTool())
agent.register_tool("weather", WeatherTool())
agent.register_tool("text_processor", TextProcessingTool())

# Request/Response models
class CreateTaskRequest(BaseModel):
    title: str
    description: str
    priority: TaskPriority = TaskPriority.MEDIUM

class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error: Optional[str]

@app.post("/tasks", response_model=TaskResponse)
async def create_task(request: CreateTaskRequest):
    """Create a new task."""
    task = agent.create_task(
        title=request.title,
        description=request.description,
        priority=request.priority
    )
    return task

@app.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None
):
    """List all tasks with optional filtering."""
    return agent.list_tasks(status=status, priority=priority)

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get a specific task by ID."""
    task = agent.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks/{task_id}/execute")
async def execute_task(task_id: str):
    """Execute a specific task."""
    task = agent.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    result = agent.execute_task(task)
    return {
        "task": task,
        "result": result
    }

@app.get("/tools")
async def list_tools():
    """List all available tools."""
    return {
        "tools": list(agent.tools.keys())
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
