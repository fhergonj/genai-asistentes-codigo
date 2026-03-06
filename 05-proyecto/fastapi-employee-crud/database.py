from models import Employee, Company
from typing import Optional, List


class Database:
    def __init__(self):
        self.employees: dict[int, Employee] = {}
        self.companies: dict[int, Company] = {}
        self.employee_id_counter = 1
        self.company_id_counter = 1

    # Métodos Company
    def create_company(self, name: str, industry: str) -> Company:
        company = Company(self.company_id_counter, name, industry)
        self.companies[self.company_id_counter] = company
        self.company_id_counter += 1
        return company

    def get_company(self, company_id: int) -> Optional[Company]:
        return self.companies.get(company_id)

    def list_companies(self) -> List[Company]:
        return list(self.companies.values())

    # Métodos Employee
    def create_employee(self, first_name: str, last_name: str, email: str, position: str, company_id: int) -> Optional[Employee]:
        if not self.get_company(company_id):
            return None
        employee = Employee(self.employee_id_counter, first_name, last_name, email, position, company_id)
        self.employees[self.employee_id_counter] = employee
        self.employee_id_counter += 1
        return employee

    def get_employee(self, employee_id: int) -> Optional[Employee]:
        return self.employees.get(employee_id)

    def list_employees(self) -> List[Employee]:
        return list(self.employees.values())

    def update_employee(self, employee_id: int, first_name: str | None = None, last_name: str | None = None,
                       email: str | None = None, position: str | None = None, company_id: int | None = None) -> Optional[Employee]:
        employee = self.get_employee(employee_id)
        if not employee:
            return None
        if first_name:
            employee.first_name = first_name
        if last_name:
            employee.last_name = last_name
        if email:
            employee.email = email
        if position:
            employee.position = position
        if company_id:
            if not self.get_company(company_id):
                return None
            employee.company_id = company_id
        return employee

    def delete_employee(self, employee_id: int) -> bool:
        if employee_id in self.employees:
            del self.employees[employee_id]
            return True
        return False


# Instancia global
db = Database()

# Data inicial
db.create_company("Acme Corp", "Technology")
db.create_company("Global Services", "Consulting")
