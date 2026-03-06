---
name: FastAPI Hello World Project
overview: "Crear un nuevo proyecto FastAPI moderno en `05-proyecto/fastapi-helloworld/` con tres endpoints: uno de hola mundo, otro que devuelve la fecha actual, y un tercero que lee un parámetro por URL y lo devuelve concatenado con la fecha actual, usando `uv` como gestor de dependencias."
todos:
  - id: create-directory
    content: Crear directorio 05-proyecto/fastapi-helloworld/
    status: completed
  - id: create-pyproject
    content: Crear pyproject.toml con configuración de uv y dependencias FastAPI
    status: completed
  - id: create-main
    content: Crear main.py con aplicación FastAPI y tres endpoints (GET /, GET /date, y GET /date/{texto})
    status: completed
  - id: create-readme
    content: Crear README.md con documentación e instrucciones de uso
    status: completed
isProject: false
---

# Plan: Proyecto FastAPI Hello World

## Objetivo

Crear un proyecto FastAPI minimalista y moderno con tres endpoints básicos siguiendo las mejores prácticas de FastAPI y usando `uv` como gestor de dependencias.

## Estructura del Proyecto

El proyecto se creará en `05-proyecto/fastapi-helloworld/` con la siguiente estructura:

```
05-proyecto/fastapi-helloworld/
├── pyproject.toml          # Configuración de dependencias con uv
├── main.py                 # Aplicación FastAPI con los tres endpoints
└── README.md              # Documentación del proyecto
```

## Archivos a Crear

### 1. `pyproject.toml`

- Configurar proyecto con `uv` compatible con Python 3.13.5
- Incluir dependencia `fastapi[standard]` (versión moderna, similar a `fastapi-employee-crud`)
- Configurar metadata básica del proyecto

### 2. `main.py`

Aplicación FastAPI con:

- Configuración básica de FastAPI con título, versión y descripción
- Endpoint `GET /` que devuelve `{"message": "Hello World"}`
- Endpoint `GET /date` que devuelve la fecha actual en formato ISO 8601
- Endpoint `GET /date/{texto}` que lee un parámetro de la URL y lo devuelve concatenado con la fecha actual
- Documentación automática habilitada en `/docs`
- Type hints explícitos siguiendo buenas prácticas
- Docstrings en los endpoints para documentación automática

### 3. `README.md`

Documentación que incluya:

- Descripción del proyecto
- Instrucciones de instalación usando `uv`
- Comandos para ejecutar la aplicación
- URLs de acceso (API, docs, OpenAPI JSON)
- Ejemplos de uso de los tres endpoints

## Detalles de Implementación

### Endpoint Hello World

- Ruta: `GET /`
- Respuesta: `{"message": "Hello World"}`
- Tags: `["Hello"]` para organización en la documentación

### Endpoint Fecha Actual

- Ruta: `GET /date`
- Respuesta: `{"current_date": "2026-01-30T..."}` (formato ISO 8601)
- Usar `datetime.now()` de Python estándar
- Tags: `["Date"]` para organización en la documentación

### Endpoint Fecha con Parámetro

- Ruta: `GET /date/{texto}` donde `{texto}` es un path parameter
- Respuesta: `{"message": "{texto} - 2026-01-30T..."}` (parámetro concatenado con fecha actual en formato ISO 8601)
- Ejemplo: `GET /date/hola` devuelve `{"message": "hola - 2026-01-30T12:34:56.789123"}`
- Usar `datetime.now()` de Python estándar para obtener la fecha actual
- Tags: `["Date"]` para organización en la documentación
- Validación automática del path parameter por FastAPI

### Configuración FastAPI

- Título: "Hello World API"
- Versión: "1.0.0"
- Descripción: Breve descripción del propósito
- Habilitar documentación en `/docs` y `/redoc`
- Habilitar OpenAPI JSON en `/openapi.json`

## Consideraciones Técnicas

- Usar `uv` para gestión de dependencias (no `requirements.txt`)
- Python 3.13.5 como versión objetivo
- FastAPI con todas las dependencias estándar (`fastapi[standard]`)
- Código limpio con type hints y docstrings
- Estructura simple pero extensible para futuras mejoras

