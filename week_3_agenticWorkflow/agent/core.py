from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from .models import (
    Task, TaskStatus, TaskPriority,
    ThinkResult, ActionResult, ObservationResult, RefinementResult
)

class Agent:
    def __init__(self, name: str):
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.current_task: Optional[Task] = None
        self.tools: Dict[str, Any] = {}
        
    def create_task(
        self,
        title: str,
        description: str,
        priority: TaskPriority = TaskPriority.MEDIUM
    ) -> Task:
        """Create a new task."""
        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority
        )
        self.tasks[task_id] = task
        return task

    def think(self, task: Task) -> ThinkResult:
        """
        Analyze the task and create a plan.
        This is where the agent would use LLM capabilities to analyze and plan.
        """
        # Example implementation
        plan = [
            f"1. Analyze task: {task.title}",
            "2. Identify required tools",
            "3. Break down into subtasks if needed",
            "4. Execute the plan"
        ]
        
        return ThinkResult(
            plan=plan,
            required_tools=list(self.tools.keys()),
            estimated_steps=len(plan),
            risks=["Potential tool unavailability"]
        )

    def act(self, task: Task, plan: List[str]) -> ActionResult:
        """
        Execute the planned actions for the task.
        This is where the agent would use tools to complete the task.
        """
        try:
            task.status = TaskStatus.IN_PROGRESS
            task.started_at = datetime.now()
            
            # Example implementation
            output = f"Executed plan for task: {task.title}"
            
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            
            return ActionResult(
                success=True,
                output=output,
                metrics={"duration": (task.completed_at - task.started_at).seconds}
            )
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            return ActionResult(
                success=False,
                output=None,
                error=str(e)
            )

    def observe(self, task: Task, action_result: ActionResult) -> ObservationResult:
        """
        Observe and analyze the results of the action.
        This is where the agent would evaluate the outcome.
        """
        matches_expected = action_result.success
        differences = []
        
        if not matches_expected:
            differences.append(f"Task failed: {action_result.error}")
        
        return ObservationResult(
            matches_expected=matches_expected,
            differences=differences,
            metrics=action_result.metrics
        )

    def refine(
        self,
        task: Task,
        observation: ObservationResult
    ) -> RefinementResult:
        """
        Refine the approach based on observations.
        This is where the agent would adjust its strategy.
        """
        adjustments = []
        new_plan = None
        
        if not observation.matches_expected:
            adjustments.append("Task failed, needs retry with modifications")
            new_plan = [
                "1. Analyze failure reason",
                "2. Modify approach",
                "3. Retry execution"
            ]
        
        return RefinementResult(
            adjustments=adjustments,
            new_plan=new_plan
        )

    def execute_task(self, task: Task) -> ActionResult:
        """Execute a complete Think → Act → Observe → Refine cycle."""
        self.current_task = task
        
        # Think
        think_result = self.think(task)
        
        # Act
        action_result = self.act(task, think_result.plan)
        
        # Observe
        observation = self.observe(task, action_result)
        
        # Refine if needed
        if not observation.matches_expected:
            refinement = self.refine(task, observation)
            if refinement.new_plan:
                # Retry with refined plan
                action_result = self.act(task, refinement.new_plan)
        
        self.current_task = None
        return action_result

    def register_tool(self, name: str, tool: Any) -> None:
        """Register a new tool that the agent can use."""
        self.tools[name] = tool

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by its ID."""
        return self.tasks.get(task_id)

    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None
    ) -> List[Task]:
        """List tasks with optional filtering."""
        tasks = list(self.tasks.values())
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
            
        return tasks
