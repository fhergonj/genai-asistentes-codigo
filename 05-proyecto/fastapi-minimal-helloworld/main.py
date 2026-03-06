from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, create_engine, Session, select
from typing import List

# Database setup
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Models
class Greeting(SQLModel, table=True):
    id: int | None = None
    message: str
    author: str

class GreetingCreate(SQLModel):
    message: str
    author: str

class GreetingUpdate(SQLModel):
    message: str | None = None
    author: str | None = None

# FastAPI app
app = FastAPI(title="Greeting API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# CRUD Endpoints
@app.get("/greetings", response_model=List[Greeting])
def list_greetings():
    with Session(engine) as session:
        greetings = session.exec(select(Greeting)).all()
        return greetings

@app.get("/greetings/{id}", response_model=Greeting)
def get_greeting(id: int):
    with Session(engine) as session:
        greeting = session.get(Greeting, id)
        if not greeting:
            raise HTTPException(status_code=404, detail="Not found")
        return greeting

@app.post("/greetings", response_model=Greeting)
def create_greeting(greeting_data: GreetingCreate):
    greeting = Greeting.from_orm(greeting_data)
    with Session(engine) as session:
        session.add(greeting)
        session.commit()
        session.refresh(greeting)
        return greeting

@app.put("/greetings/{id}", response_model=Greeting)
def update_greeting(id: int, greeting_data: GreetingUpdate):
    with Session(engine) as session:
        greeting = session.get(Greeting, id)
        if not greeting:
            raise HTTPException(status_code=404, detail="Not found")

        update_data = greeting_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(greeting, key, value)

        session.add(greeting)
        session.commit()
        session.refresh(greeting)
        return greeting

@app.delete("/greetings/{id}")
def delete_greeting(id: int):
    with Session(engine) as session:
        greeting = session.get(Greeting, id)
        if not greeting:
            raise HTTPException(status_code=404, detail="Not found")
        session.delete(greeting)
        session.commit()
        return {"message": "Deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
