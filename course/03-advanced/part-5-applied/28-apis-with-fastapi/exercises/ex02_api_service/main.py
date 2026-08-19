"""FastAPI Task Management Service with routing, error handling, and in-memory persistence."""

from __future__ import annotations

from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, status
from models import TaskCreate, TaskResponse, TaskUpdate

app = FastAPI(title="Task Service", version="1.0.0")

# In-memory storage for demonstration
TASKS_DB: Dict[int, TaskResponse] = {}
_ID_COUNTER: int = 0


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> TaskResponse:
    global _ID_COUNTER
    _ID_COUNTER += 1
    task = TaskResponse(
        id=_ID_COUNTER,
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        completed=False
    )
    TASKS_DB[_ID_COUNTER] = task
    return task


@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks(completed: Optional[bool] = None) -> List[TaskResponse]:
    tasks = list(TASKS_DB.values())
    if completed is not None:
        tasks = [t for t in tasks if t.completed == completed]
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int) -> TaskResponse:
    if task_id not in TASKS_DB:
        raise HTTPException(status_code=404, detail="Task not found")
    return TASKS_DB[task_id]


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: TaskUpdate) -> TaskResponse:
    if task_id not in TASKS_DB:
        raise HTTPException(status_code=404, detail="Task not found")
    
    current = TASKS_DB[task_id]
    updated_dict = current.model_dump()
    
    update_data = payload.model_dump(exclude_unset=True)
    updated_dict.update(update_data)
    
    updated_task = TaskResponse(**updated_dict)
    TASKS_DB[task_id] = updated_task
    return updated_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> None:
    if task_id not in TASKS_DB:
        raise HTTPException(status_code=404, detail="Task not found")
    del TASKS_DB[task_id]
