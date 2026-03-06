from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, create_engine, Session, select
from typing import List

# Database setup
DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Models
class Task(SQLModel, table=True):
    id: int | None = None
    title: str
    description: str | None = None
    completed: bool = False

class TaskCreate(SQLModel):
    title: str
    description: str | None = None

class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

# FastAPI app
app = FastAPI(
    title="Task API",
    description="Simple Task Management API with FastAPI and SQLModel",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# CRUD Endpoints
@app.get("/tasks", response_model=List[Task])
def list_tasks():
    """Get all tasks"""
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Get a task by ID"""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

@app.post("/tasks", response_model=Task)
def create_task(task_data: TaskCreate):
    """Create a new task"""
    task = Task.from_orm(task_data)
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskUpdate):
    """Update a task"""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        update_data = task_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task"""
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(task)
        session.commit()
        return {"message": "Task deleted successfully"}

@app.get("/")
def root():
    """API root endpoint"""
    return {
        "message": "Welcome to Task API",
        "docs": "/docs",
        "endpoints": {
            "GET /tasks": "List all tasks",
            "GET /tasks/{id}": "Get task by ID",
            "POST /tasks": "Create new task",
            "PUT /tasks/{id}": "Update task",
            "DELETE /tasks/{id}": "Delete task"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
