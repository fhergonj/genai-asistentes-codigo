# Curso de asistentes de código para desarrolladores

[![Python](https://img.shields.io/badge/Python-3.13.5-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128.0-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![uv](https://img.shields.io/badge/uv-Package_Manager-8B5CF6?style=flat)](https://docs.astral.sh/uv/)
[![Pydantic](https://img.shields.io/badge/Pydantic-V2-E92063?style=flat&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![SQLModel](https://img.shields.io/badge/SQLModel-0.0.31-009688?style=flat)](https://sqlmodel.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Curso de Agentes de IA Generativa para generación de código.

Autor: Alan Sastre

---

## Contenido del curso

El curso se estructura en módulos que abarcan desde la introducción al panorama actual de los asistentes de código hasta la implementación práctica de proyectos.

### Módulo 1 - Panorama de herramientas IA

Introducción al ecosistema de asistentes de código con IA:

- Introducción a la IA generativa en desarrollo de software
- Extensiones de IDE con capacidades de IA
- IDEs con IA integrada
- Herramientas CLI
- Agentes en la nube
- Estrategias de contexto para agentes

### Módulo 2 - GitHub Copilot

Guía completa de GitHub Copilot:

- Configuración inicial y setup
- Autocompletado de código (Completions)
- Chat integrado y prompts
- Modo agente
- Model Context Protocol (MCP)

### Módulo 3 - Cursor IDE

Dominio del IDE Cursor:

- Instalación y configuración
- Tab completion
- Edición en línea (Inline Edit)
- Modos de chat (Ask, Agent, Edit)
- Gestión de contexto

### Módulo 4 - Claude Code

Uso avanzado de Claude Code:

- Setup y configuración
- Referencia de comandos CLI
- Agent Skills
- Subagentes

---

## Proyectos prácticos

Los proyectos de ejemplo se encuentran en el directorio `05-proyecto/`. Cada uno demuestra patrones y buenas prácticas desarrollados con asistencia de IA.

### fastapi-helloworld

API minimalista de ejemplo con dos endpoints básicos.

**Características:**
- Endpoint Hello World
- Endpoint de fecha actual con parámetros de ruta
- Documentación OpenAPI automática

**Ejecutar:**
```bash
cd 05-proyecto/fastapi-helloworld
uv sync
fastapi dev main.py
```

### fastapi-minimal

API de gestión de tareas con persistencia SQLite.

**Características:**
- CRUD completo de tareas (Task)
- Persistencia con SQLModel y SQLite
- Validación de datos

**Ejecutar:**
```bash
cd 05-proyecto/fastapi-minimal
uv sync
fastapi dev main.py
```

### fastapi-minimal-helloworld

API de saludos con operaciones CRUD y base de datos.

**Características:**
- CRUD de mensajes de saludo (Greeting)
- Persistencia SQLite
- Estructura minimalista

**Ejecutar:**
```bash
cd 05-proyecto/fastapi-minimal-helloworld
uv venv
uv pip install fastapi sqlmodel uvicorn
fastapi dev main.py
```

### fastapi-with-testing

API de productos con arquitectura en capas y tests.

**Características:**
- CRUD de productos (Product)
- Separación en capas (models, schemas, database)
- Middleware CORS configurado
- Suite de tests con pytest

**Ejecutar:**
```bash
cd 05-proyecto/fastapi-with-testing
uv venv
uv pip install -r requirements.txt
fastapi dev main.py

# Ejecutar tests
pytest test_api.py -v
```

### fastapi-employee-crud

Proyecto de referencia con arquitectura completa de producción.

**Características:**
- CRUD de empleados con relación a empresas
- Inyección de dependencias (Depends)
- Validación avanzada con Pydantic V2
- Middleware de seguridad (CORS, TrustedHost)
- Manejo de errores personalizado
- Tests completos con cobertura

**Ejecutar:**
```bash
cd 05-proyecto/fastapi-employee-crud
uv venv
uv pip install -r requirements.txt
fastapi dev main.py

# Ejecutar tests
pytest test_api.py -v
```

---

## Requisitos previos

- Python 3.13.5
- uv (gestor de paquetes Python)
- Git

---

## Instalación

### 1. Instalar uv

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Instalar Python 3.13.5 con uv

```bash
uv python install 3.13.5
```

### 3. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/genai-devtools.git
cd genai-devtools
```

### 4. Configurar un proyecto

Para cualquier proyecto en `05-proyecto/`:

```bash
cd 05-proyecto/fastapi-helloworld
uv sync
```

Este comando crea automáticamente el entorno virtual y sincroniza las dependencias.

### 5. Ejecutar la aplicación

```bash
fastapi dev main.py
```

La documentación interactiva estará disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Estructura del repositorio

```
genai-devtools/
├── 01-landscape/          # Panorama de herramientas IA
│   ├── 01-introduccion.ipynb
│   ├── 02-extensiones-ide.ipynb
│   ├── 03-ides.ipynb
│   ├── 04-clis.ipynb
│   ├── 05-cloud-agents.ipynb
│   └── 06-contexto-para-agentes.ipynb
│
├── 02-github-copilot/     # Módulo GitHub Copilot
│   ├── 01-setup.ipynb
│   ├── 02-completions.ipynb
│   ├── 03-chat.ipynb
│   ├── 04-agent-mode.ipynb
│   └── 05-mcp.ipynb
│
├── 03-cursor/             # Módulo Cursor IDE
│   ├── 01-setup.ipynb
│   ├── 02-tab.ipynb
│   ├── 03-inline-edit.ipynb
│   ├── 04-chat-modes.ipynb
│   └── 05-contexto.ipynb
│
├── 04-claude-code/        # Módulo Claude Code
│   ├── 01-setup.ipynb
│   ├── 02-cli-reference.ipynb
│   ├── 03-agent-skills.ipynb
│   └── 04-subagents.ipynb
│
├── 05-proyecto/           # Proyectos prácticos
│   ├── fastapi-helloworld/
│   ├── fastapi-minimal/
│   ├── fastapi-minimal-helloworld/
│   ├── fastapi-with-testing/
│   └── fastapi-employee-crud/
│
├── .cursor/               # Configuración Cursor IDE
├── .claude/               # Configuración Claude Code
├── .github/               # Configuración GitHub Copilot
└── README.md              # Este fichero
```

---

## Tecnologías utilizadas

| Tecnología | Versión | Descripción |
|------------|---------|-------------|
| Python | 3.13.5 | Lenguaje de programación |
| FastAPI | 0.128.0 | Framework web asíncrono |
| Pydantic | V2 | Validación de datos |
| SQLModel | 0.0.31 | ORM para SQLite |
| uv | latest | Gestor de paquetes Python |
| pytest | 7.4.4 | Framework de testing |
| Uvicorn | 0.30.0 | Servidor ASGI |

---

## Asistentes de código tratados

- **GitHub Copilot**: Asistente de código integrado en VS Code y otros editores
- **Cursor**: IDE completo con IA integrada basado en VS Code
- **Claude Code**: Asistente CLI de Anthropic para desarrollo

---

## Licencia

MIT.
