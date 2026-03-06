from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional


class CompanyRead(BaseModel):
    """Esquema de lectura para Company (reporte)."""
    id: int
    name: str
    industry: str
    employee_count: int
    
    model_config = ConfigDict(
        from_attributes=True,  # Permite lectura desde atributos de objetos
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Tech Corp",
                "industry": "Technology",
                "employee_count": 150
            }
        }
    )


class EmployeeCreate(BaseModel):
    """Esquema para crear un nuevo empleado."""
    first_name: str
    last_name: str
    email: str
    position: str
    company_id: int

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        """Valida formato de email."""
        if "@" not in v or "." not in v.split("@")[1]:
            raise ValueError("Email debe contener @ y un dominio válido")
        return v.lower()  # Normaliza a minúsculas

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names(cls, v: str) -> str:
        """Valida que nombres no estén vacíos y sean texto válido."""
        if not v or not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()

    @field_validator("position")
    @classmethod
    def validate_position(cls, v: str) -> str:
        """Valida que el puesto no esté vacío."""
        if not v or not v.strip():
            raise ValueError("El puesto no puede estar vacío")
        return v.strip()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "Juan",
                "last_name": "García",
                "email": "juan.garcia@example.com",
                "position": "Senior Developer",
                "company_id": 1
            }
        }
    )


class EmployeeUpdate(BaseModel):
    """Esquema para actualizar un empleado (todos los campos opcionales)."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    company_id: Optional[int] = None

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: Optional[str]) -> Optional[str]:
        """Valida email si se proporciona."""
        if v and ("@" not in v or "." not in v.split("@")[1]):
            raise ValueError("Email debe contener @ y un dominio válido")
        return v.lower() if v else None

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_names(cls, v: Optional[str]) -> Optional[str]:
        """Valida nombres si se proporcionan."""
        if v and not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip() if v else None

    @field_validator("position")
    @classmethod
    def validate_position(cls, v: Optional[str]) -> Optional[str]:
        """Valida puesto si se proporciona."""
        if v and not v.strip():
            raise ValueError("El puesto no puede estar vacío")
        return v.strip() if v else None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "Juan",
                "email": "juan.new@example.com"
            }
        }
    )


class EmployeeRead(BaseModel):
    """Esquema de lectura para Empleado (reporte con empresa)."""
    id: int
    first_name: str
    last_name: str
    full_name: str
    email: str
    position: str
    company_id: int
    company: Optional[CompanyRead] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "first_name": "Juan",
                "last_name": "García",
                "full_name": "Juan García",
                "email": "juan.garcia@example.com",
                "position": "Senior Developer",
                "company_id": 1,
                "company": {
                    "id": 1,
                    "name": "Tech Corp",
                    "industry": "Technology",
                    "employee_count": 150
                }
            }
        }
    )
