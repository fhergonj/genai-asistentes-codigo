---
name: fastapi-crud-minimal
description: Generate minimal FastAPI REST APIs with CRUD operations using SQLModel and SQLite. Use when creating a new FastAPI project with basic CRUD endpoints (GET all, GET by ID, POST create, PUT update, DELETE) for simple entities without relationships. Stack includes FastAPI 0.128.0, uv package manager, SQLModel ORM, and SQLite database - all in a single main.py file.
---

# FastAPI CRUD Minimal Skill

Generate production-ready FastAPI REST APIs with CRUD endpoints for simple entities, all in a single `main.py` file using SQLModel and SQLite.

## Quick Start Workflow

### Step 1: Create Project with uv

```bash
mkdir my-api
cd my-api
uv init
uv add fastapi sqlmodel uvicorn
uv sync
```

See [uv-setup.md](references/uv-setup.md) for full setup details and commands.

### Step 2: Generate main.py from Template

Use the template at `assets/main.py.template` and customize:

**Placeholders to replace:**
- `{{EntityName}}` - Entity name (PascalCase): `User`, `Product`, `Post`
- `{{entity}}` - Lowercase singular: `user`, `product`, `post`
- `{{entity_plural}}` - Lowercase plural: `users`, `products`, `posts`
- `{{fields}}` - Entity fields (one per line): `name: str` `email: str` `age: int`
- `{{fields_create}}` - Create schema fields (same as fields without id)
- `{{fields_update}}` - Update schema fields (all Optional): `name: str | None = None`
- `{{API_Title}}` - API title: `"User API"`, `"Product API"`

### Step 3: Example - Create User API

Replace placeholders in template:

```python
class User(SQLModel, table=True):
    id: int | None = None
    name: str
    email: str
    age: int

class UserCreate(SQLModel):
    name: str
    email: str
    age: int

class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    age: int | None = None
```

Endpoints generated:
- `GET /users` - List all users
- `GET /users/{id}` - Get user by ID
- `POST /users` - Create user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Step 4: Run the API

```bash
uv run uvicorn main:app --reload
```

Access:
- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Model Definition Best Practices

### Required vs Optional Fields

```python
# Required field (no default)
name: str

# Optional field with default
description: str | None = None

# Optional field in Create schema (user provides)
email: str

# Optional field in Update schema (can skip)
email: str | None = None
```

### Field Validation

For field constraints, use SQLModel's `Field`:

```python
from sqlmodel import Field

class Product(SQLModel, table=True):
    id: int | None = None
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)  # Must be > 0
    quantity: int = Field(ge=0)  # Must be >= 0
```

See [sqlmodel-basics.md](references/sqlmodel-basics.md) for more options.

## Schema Separation

Always create three schemas:
1. **Table model** (`table=True`) - Database representation with id
2. **Create schema** - Request body for POST (no id field)
3. **Update schema** - Request body for PUT (all fields Optional)

This prevents exposing id in requests and supports partial updates.

## Common Customizations

### Add timestamps
```python
from datetime import datetime

class {{EntityName}}(SQLModel, table=True):
    id: int | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Add unique constraint
```python
class User(SQLModel, table=True):
    id: int | None = None
    email: str = Field(unique=True)
```

### Change database name
```python
DATABASE_URL = "sqlite:///./my_database.db"
```

## Deployment

For production:
1. Use PostgreSQL instead of SQLite: `DATABASE_URL = "postgresql+psycopg://user:pass@localhost/db"`
2. Use environment variables for DATABASE_URL
3. Use separate `SessionLocal` dependency instead of inline sessions
4. Add proper error handling and logging

See [sqlmodel-basics.md](references/sqlmodel-basics.md) for advanced patterns.

## Tips

- Keep entities simple (no relationships) for this template
- Test endpoints with Swagger UI at `/docs`
- Database file `database.db` is created automatically on first run
- Remove `database.db` to reset the database
