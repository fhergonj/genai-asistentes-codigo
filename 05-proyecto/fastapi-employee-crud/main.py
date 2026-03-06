from typing import Annotated, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging

from database import db
from models import Employee
from schemas import EmployeeCreate, EmployeeUpdate, EmployeeRead, CompanyRead

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de la aplicación con mejor documentación
app = FastAPI(
    title="Employee CRUD API",
    version="1.0.0",
    description="API moderna para gestionar empleados y empresas",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# ============================================================================
# MIDDLEWARE - Seguridad y CORS
# ============================================================================

# Middleware de hosts confiables (seguridad)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.example.com"]
)

# Configuración CORS (seguridad - adaptar según tu entorno)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],  # Adapta a tu frontend
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600
)

# ============================================================================
# DEPENDENCIAS - Reutilización de lógica (Best Practice: Depends)
# ============================================================================

def get_employee_with_company(employee_id: int) -> EmployeeRead:
    """
    Obtiene un empleado con su información de empresa asociada.
    Lanza HTTPException si el empleado no existe.
    
    Dependencies como práctica recomendada en FastAPI 0.128.0
    para evitar código repetido en los endpoints.
    """
    employee = db.get_employee(employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )
    return _serialize_employee_with_company(employee)


def _serialize_employee_with_company(employee: Employee) -> EmployeeRead:
    """Helper privado para serializar un empleado con su empresa."""
    company = db.get_company(employee.company_id)
    return EmployeeRead(
        id=employee.id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        full_name=employee.full_name,
        email=employee.email,
        position=employee.position,
        company_id=employee.company_id,
        company=CompanyRead(**company.__dict__) if company else None
    )


# ============================================================================
# RUTAS CRUD - Endpoints con estructura limpia
# ============================================================================

@app.get(
    "/employees",
    response_model=list[EmployeeRead],
    summary="Listar todos los empleados",
    tags=["Employees"]
)
async def list_employees() -> list[EmployeeRead]:
    """
    Obtiene una lista completa de todos los empleados registrados.
    Cada empleado incluye su información de empresa asociada.
    """
    employees = db.list_employees()
    return [_serialize_employee_with_company(emp) for emp in employees]


@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeRead,
    summary="Obtener empleado por ID",
    tags=["Employees"]
)
async def get_employee(
    employee: Annotated[EmployeeRead, Depends(get_employee_with_company)]
) -> EmployeeRead:
    """
    Obtiene un empleado específico por su ID.
    Retorna 404 si el empleado no existe.
    
    Usa Depends para inyectar el empleado validado.
    """
    return employee


@app.post(
    "/employees",
    response_model=EmployeeRead,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo empleado",
    tags=["Employees"]
)
async def create_employee(data: EmployeeCreate) -> EmployeeRead:
    """
    Crea un nuevo empleado. La empresa asociada debe existir.
    
    Validaciones:
    - Email debe ser válido (validación en Pydantic)
    - company_id debe corresponder a una empresa existente
    
    Retorna 400 si la empresa no existe.
    """
    employee = db.create_employee(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        position=data.position,
        company_id=data.company_id
    )
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company no existe"
        )
    return _serialize_employee_with_company(employee)


@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeRead,
    summary="Actualizar empleado",
    tags=["Employees"]
)
async def update_employee(
    employee_id: int,
    data: EmployeeUpdate
) -> EmployeeRead:
    """
    Actualiza un empleado existente con los campos proporcionados.
    Solo actualiza los campos que se proporcionan.
    
    Retorna 404 si el empleado no existe.
    Retorna 400 si la empresa no existe.
    """
    employee = db.update_employee(
        employee_id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        position=data.position,
        company_id=data.company_id
    )
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado o Company inválido"
        )
    return _serialize_employee_with_company(employee)


@app.delete(
    "/employees/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar empleado",
    tags=["Employees"]
)
async def delete_employee(employee_id: int) -> None:
    """
    Elimina un empleado existente.
    Retorna 204 No Content si es exitoso.
    Retorna 404 si el empleado no existe.
    """
    if not db.delete_employee(employee_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )


# ============================================================================
# MANEJADORES DE ERRORES PERSONALIZADOS (Custom Exception Handlers)
# ============================================================================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc: ValueError):
    """Maneja errores de validación custom (ej: email inválido)."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)}
    )
