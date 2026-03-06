from datetime import datetime


class Company:
    def __init__(self, id: int, name: str, industry: str, employee_count: int = 0):
        self.id = id
        self.name = name
        self.industry = industry
        self.employee_count = employee_count

    def __repr__(self):
        return f"Company(id={self.id}, name={self.name}, industry={self.industry})"


class Department:
    def __init__(self, id: int, name: str, company_id: int, manager_id: int | None = None):
        self.id = id
        self.name = name
        self.company_id = company_id
        self.manager_id = manager_id
        self.employee_count = 0

    def set_manager(self, manager_id: int):
        """Asigna un manager al departamento."""
        self.manager_id = manager_id

    def remove_manager(self):
        """Remueve el manager del departamento."""
        self.manager_id = None

    def increment_employee_count(self):
        """Incrementa el contador de empleados."""
        self.employee_count += 1

    def decrement_employee_count(self):
        """Decrementa el contador de empleados."""
        if self.employee_count > 0:
            self.employee_count -= 1

    def __repr__(self):
        manager_info = f", manager_id={self.manager_id}" if self.manager_id else ""
        return f"Department(id={self.id}, name={self.name}, company_id={self.company_id}{manager_info}, employee_count={self.employee_count})"


class Empleado:
    def __init__(self, id: int, first_name: str, last_name: str, email: str, position: str, company_id: int):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.position = position
        self.company_id = company_id

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def validate_email(self) -> bool:
        return "@" in self.email and "." in self.email.split("@")[1]

    def __repr__(self):
        return f"Employee(id={self.id}, full_name={self.full_name}, email={self.email}, position={self.position})"


class Project:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.employees = []

    def add_employee(self, employee: Empleado):
        if employee not in self.employees:
            self.employees.append(employee)

    def remove_employee(self, employee: Empleado):
        if employee in self.employees:
            self.employees.remove(employee)

    def __repr__(self):
        return f"Project(name={self.name}, description={self.description}, employees={[emp.full_name for emp in self.employees]})"

# Nueva clase Task con asociacion Many To Many con Employee
class Task:
    def __init__(
        self,
        title: str,
        description: str,
        assignee: Empleado | None = None,
        project: Project | None = None,
        date_created: datetime = datetime.now()
    ):
        self.title = title
        self.description = description
        self.assignee = assignee
        self.completed = False
        self.project = project
        self.date_created = date_created


    def mark_done(self):
        self.completed = True

    def __repr__(self):
        return f"Task(title={self.title}, description={self.description}, assignee={self.assignee.full_name}, completed={self.completed})"

class Comment:
    def __init__(self, content: str, author: Empleado, task: Task, created_at: datetime = datetime.now()):
        self.content = content
        self.author = author
        self.task = task
        self.created_at = created_at

    def __repr__(self):
        return f"Comment(content={self.content}, author={self.author.full_name}, task={self.task.title}, created_at={self.created_at})"
