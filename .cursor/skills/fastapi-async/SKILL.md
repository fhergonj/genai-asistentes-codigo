---
name: fastapi-async
description: Guía para usar async/await en FastAPI: endpoints asíncronos, operaciones de base de datos async, llamadas HTTP externas, background tasks y dependencias async. Use cuando implemente endpoints FastAPI, necesite operaciones I/O asíncronas, o cuando el usuario pregunte sobre asincronía en FastAPI.
---

# Asincronía en FastAPI

## Principios Básicos

FastAPI está construido sobre Starlette y soporta nativamente async/await. Usa `async def` para endpoints que realizan operaciones I/O (base de datos, HTTP, archivos).

**Regla general**: Usa `async def` cuando haya operaciones I/O bloqueantes. Para operaciones CPU-intensivas, considera `BackgroundTasks` o ejecutores.

## Endpoints Asíncronos

### Formato Básico

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    # Operaciones async aquí
    return {"item_id": item_id}
```

### Endpoints Síncronos (cuándo usarlos)

Solo usa `def` (sin async) si:
- La función es puramente CPU-bound
- No hay operaciones I/O
- Es una función simple de cálculo

```python
@app.get("/compute")
def compute_sum(a: int, b: int):
    # Operación CPU-bound, no necesita async
    return {"result": a + b}
```

## Operaciones de Base de Datos Async

### SQLAlchemy Async

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends

# Crear engine async
engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency para obtener sesión
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# Endpoint usando la sesión async
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404)
    return user
```

### Operaciones CRUD Async

```python
# CREATE
@app.post("/users", status_code=201)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = User(**user_data.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# READ
@app.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

# UPDATE
@app.put("/users/{user_id}")
async def update_user(
    user_id: int, 
    user_data: UserUpdate, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404)
    
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    
    await db.commit()
    await db.refresh(user)
    return user

# DELETE
@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404)
    
    await db.delete(user)
    await db.commit()
```

## Llamadas HTTP Externas Async

### httpx (recomendado)

```python
import httpx
from fastapi import HTTPException

@app.get("/external-data")
async def fetch_external_data():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("https://api.example.com/data", timeout=5.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=503, detail=f"External API error: {str(e)}")
```

### Múltiples llamadas paralelas

```python
@app.get("/aggregated-data")
async def fetch_aggregated_data():
    async with httpx.AsyncClient() as client:
        # Ejecutar múltiples requests en paralelo
        results = await asyncio.gather(
            client.get("https://api1.example.com/data"),
            client.get("https://api2.example.com/data"),
            client.get("https://api3.example.com/data"),
            return_exceptions=True  # No fallar si una falla
        )
        
        data = []
        for result in results:
            if isinstance(result, Exception):
                continue  # O manejar el error
            data.append(result.json())
        
        return {"data": data}
```

## Background Tasks

Para operaciones que deben ejecutarse después de enviar la respuesta:

```python
from fastapi import BackgroundTasks

def send_notification(email: str, message: str):
    # Operación síncrona (envío de email, logging, etc.)
    print(f"Sending email to {email}: {message}")

@app.post("/users", status_code=201)
async def create_user(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    user = User(**user_data.dict())
    db.add(user)
    await db.commit()
    
    # Agregar tarea en background
    background_tasks.add_task(send_notification, user.email, "Welcome!")
    
    return user
```

## Dependencias Async

Las dependencias también pueden ser async:

```python
from fastapi import Depends, HTTPException, status

async def verify_token(token: str = Header(...)):
    # Verificación async (ej: consulta a base de datos)
    if not await is_valid_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

async def get_current_user(token: str = Depends(verify_token)):
    user = await get_user_by_token(token)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/protected")
async def protected_route(current_user = Depends(get_current_user)):
    return {"user": current_user}
```

## Manejo de Errores en Async

```python
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

@app.post("/users")
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = User(**user_data.dict())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="User already exists")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
```

## Mejores Prácticas

### ✅ DO

1. **Usa `async def` para endpoints con I/O**:
   ```python
   @app.get("/items")
   async def get_items():
       items = await db.fetch_all("SELECT * FROM items")
       return items
   ```

2. **Usa `await` para todas las operaciones async**:
   ```python
   result = await db.execute(query)  # ✅ Correcto
   result = db.execute(query)  # ❌ Incorrecto - bloquea el event loop
   ```

3. **Maneja excepciones y rollbacks**:
   ```python
   try:
       await db.commit()
   except Exception:
       await db.rollback()
       raise
   ```

4. **Usa context managers para recursos**:
   ```python
   async with httpx.AsyncClient() as client:
       response = await client.get(url)
   ```

### ❌ DON'T

1. **No bloquees el event loop**:
   ```python
   # ❌ Mal - bloquea el event loop
   @app.get("/slow")
   async def slow_endpoint():
       time.sleep(5)  # NO hacer esto
       return {"done": True}
   
   # ✅ Bien - usa asyncio.sleep
   @app.get("/slow")
   async def slow_endpoint():
       await asyncio.sleep(5)
       return {"done": True}
   ```

2. **No mezcles código síncrono bloqueante con async**:
   ```python
   # ❌ Mal
   @app.get("/data")
   async def get_data():
       result = requests.get("https://api.example.com")  # Bloqueante
       return result.json()
   
   # ✅ Bien
   @app.get("/data")
   async def get_data():
       async with httpx.AsyncClient() as client:
           result = await client.get("https://api.example.com")
           return result.json()
   ```

3. **No olvides `await` en operaciones async**:
   ```python
   # ❌ Mal - retorna una coroutine, no el resultado
   @app.get("/items")
   async def get_items():
       return db.execute(query)  # Falta await
   
   # ✅ Bien
   @app.get("/items")
   async def get_items():
       result = await db.execute(query)
       return result.scalars().all()
   ```

## Patrones Comunes

### Operaciones secuenciales

```python
@app.get("/user-profile/{user_id}")
async def get_user_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    # Ejecutar en secuencia
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404)
    
    posts = await db.execute(select(Post).where(Post.user_id == user_id))
    
    return {
        "user": user,
        "posts": posts.scalars().all()
    }
```

### Operaciones paralelas

```python
@app.get("/user-profile/{user_id}")
async def get_user_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    # Ejecutar en paralelo
    user_task = db.get(User, user_id)
    posts_task = db.execute(select(Post).where(Post.user_id == user_id))
    
    user, posts_result = await asyncio.gather(user_task, posts_task)
    
    if not user:
        raise HTTPException(status_code=404)
    
    return {
        "user": user,
        "posts": posts_result.scalars().all()
    }
```

## Testing Async Endpoints

```python
from httpx import AsyncClient
from fastapi.testclient import TestClient

# Opción 1: TestClient (síncrono, más simple)
def test_endpoint():
    client = TestClient(app)
    response = client.get("/items/1")
    assert response.status_code == 200

# Opción 2: AsyncClient (async, más realista)
@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/items/1")
        assert response.status_code == 200
```

## Resumen de Decisiones

| Escenario | Solución |
|-----------|----------|
| Endpoint con I/O (DB, HTTP, archivos) | `async def` + `await` |
| Endpoint CPU-bound simple | `def` (sin async) |
| Múltiples operaciones independientes | `asyncio.gather()` |
| Operación después de respuesta | `BackgroundTasks` |
| Dependencia con I/O | `async def` dependency |
| Llamadas HTTP externas | `httpx.AsyncClient` |
| Base de datos | SQLAlchemy async + `AsyncSession` |
