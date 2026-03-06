# SQLModel Basics

## Model Definition

```python
from sqlmodel import SQLModel
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = None
    name: str
    email: str
    age: int
```

### Key Points

- `table=True` - Creates a database table
- `Optional[int] = None` - Auto-increment primary key (id = None means insert new)
- Type hints define columns and validation

## Request/Response Schemas

Create separate classes without `table=True` for API requests:

```python
class UserCreate(SQLModel):
    name: str
    email: str
    age: int

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
```

## Database Operations

### Create (Insert)
```python
user = User(name="John", email="john@example.com", age=30)
session.add(user)
session.commit()
session.refresh(user)  # Reload from DB to get id
```

### Read
```python
from sqlmodel import select

user = session.get(User, 1)  # By ID
users = session.exec(select(User)).all()  # All records
```

### Update
```python
user = session.get(User, 1)
user.name = "Jane"
session.add(user)
session.commit()
session.refresh(user)
```

### Delete
```python
user = session.get(User, 1)
session.delete(user)
session.commit()
```

## Engine & Session

```python
from sqlmodel import create_engine, Session

engine = create_engine("sqlite:///./database.db", connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session
```

## Field Validation

```python
from sqlmodel import Field

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
```
