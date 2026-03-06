"""
Tests para la API Employee CRUD

Uso:
  python -m pytest test_api.py -v
  python -m pytest test_api.py -v --cov=. --cov-report=html
"""

import pytest
from fastapi.testclient import TestClient
from main import app
from database import db


@pytest.fixture
def client():
    """Cliente de prueba para la API."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reinicia la base de datos antes de cada test."""
    db.employees.clear()
    db.companies.clear()
    db.employee_id_counter = 1
    db.company_id_counter = 1
    yield


@pytest.fixture
def sample_company():
    """Crea una empresa de prueba."""
    return db.create_company("Tech Corp", "Technology")


class TestListEmployees:
    """Tests para listar empleados."""
    
    def test_list_empty_employees(self, client):
        """Debe retornar lista vacía cuando no hay empleados."""
        response = client.get("/employees")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_employees_with_data(self, client, sample_company):
        """Debe retornar lista de empleados con su empresa."""
        db.create_employee(
            first_name="Juan",
            last_name="García",
            email="juan@example.com",
            position="Developer",
            company_id=sample_company.id
        )
        
        response = client.get("/employees")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["first_name"] == "Juan"
        assert data[0]["company"]["name"] == "Tech Corp"


class TestGetEmployee:
    """Tests para obtener un empleado específico."""
    
    def test_get_nonexistent_employee(self, client):
        """Debe retornar 404 para empleado inexistente."""
        response = client.get("/employees/999")
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"]

    def test_get_existing_employee(self, client, sample_company):
        """Debe retornar el empleado con su empresa."""
        emp = db.create_employee(
            first_name="Ana",
            last_name="López",
            email="ana@example.com",
            position="Manager",
            company_id=sample_company.id
        )
        
        response = client.get(f"/employees/{emp.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Ana López"
        assert data["email"] == "ana@example.com"
        assert data["company"]["name"] == "Tech Corp"


class TestCreateEmployee:
    """Tests para crear empleados."""
    
    def test_create_employee_success(self, client, sample_company):
        """Debe crear un empleado exitosamente."""
        payload = {
            "first_name": "Carlos",
            "last_name": "Ruiz",
            "email": "carlos@example.com",
            "position": "Architect",
            "company_id": sample_company.id
        }
        
        response = client.post("/employees", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["full_name"] == "Carlos Ruiz"
        assert data["id"] == 1

    def test_create_employee_invalid_email(self, client, sample_company):
        """Debe rechazar email inválido."""
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "email": "invalid-email",  # ❌ Sin @
            "position": "Dev",
            "company_id": sample_company.id
        }
        
        response = client.post("/employees", json=payload)
        assert response.status_code == 422
        assert "email" in str(response.json())

    def test_create_employee_nonexistent_company(self, client):
        """Debe retornar 400 si la empresa no existe."""
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "position": "Dev",
            "company_id": 999  # ❌ Empresa inexistente
        }
        
        response = client.post("/employees", json=payload)
        assert response.status_code == 400
        assert "Company" in response.json()["detail"]

    def test_create_employee_email_normalized(self, client, sample_company):
        """Debe normalizar el email a minúsculas."""
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "email": "TEST@EXAMPLE.COM",  # Mayúsculas
            "position": "Dev",
            "company_id": sample_company.id
        }
        
        response = client.post("/employees", json=payload)
        assert response.status_code == 201
        assert response.json()["email"] == "test@example.com"  # ✅ Normalizado

    def test_create_employee_empty_name(self, client, sample_company):
        """Debe rechazar nombres vacíos."""
        payload = {
            "first_name": "",  # ❌ Vacío
            "last_name": "User",
            "email": "test@example.com",
            "position": "Dev",
            "company_id": sample_company.id
        }
        
        response = client.post("/employees", json=payload)
        assert response.status_code == 422


class TestUpdateEmployee:
    """Tests para actualizar empleados."""
    
    def test_update_employee_success(self, client, sample_company):
        """Debe actualizar empleado parcialmente."""
        emp = db.create_employee(
            first_name="Original",
            last_name="Name",
            email="original@example.com",
            position="Dev",
            company_id=sample_company.id
        )
        
        payload = {
            "position": "Senior Developer",
            "email": "new@example.com"
        }
        
        response = client.put(f"/employees/{emp.id}", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["position"] == "Senior Developer"
        assert data["email"] == "new@example.com"
        assert data["first_name"] == "Original"  # No cambió

    def test_update_nonexistent_employee(self, client):
        """Debe retornar 404 para empleado inexistente."""
        response = client.put("/employees/999", json={"position": "Dev"})
        assert response.status_code == 404

    def test_update_with_invalid_company(self, client, sample_company):
        """Debe rechazar company_id inexistente."""
        emp = db.create_employee(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            position="Dev",
            company_id=sample_company.id
        )
        
        response = client.put(
            f"/employees/{emp.id}",
            json={"company_id": 999}
        )
        assert response.status_code == 400


class TestDeleteEmployee:
    """Tests para eliminar empleados."""
    
    def test_delete_employee_success(self, client, sample_company):
        """Debe eliminar un empleado."""
        emp = db.create_employee(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            position="Dev",
            company_id=sample_company.id
        )
        
        response = client.delete(f"/employees/{emp.id}")
        assert response.status_code == 204
        
        # Verificar que fue eliminado
        response = client.get(f"/employees/{emp.id}")
        assert response.status_code == 404

    def test_delete_nonexistent_employee(self, client):
        """Debe retornar 404 al eliminar inexistente."""
        response = client.delete("/employees/999")
        assert response.status_code == 404


class TestOpenAPI:
    """Tests para documentación OpenAPI."""
    
    def test_openapi_schema(self, client):
        """Debe generar esquema OpenAPI válido."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert schema["openapi"] == "3.1.0"
        assert "paths" in schema
        assert "/employees" in schema["paths"]

    def test_api_docs_available(self, client):
        """Debe estar disponible la documentación interactiva."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "html" in response.headers["content-type"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
