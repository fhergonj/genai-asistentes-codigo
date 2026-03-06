
class Company:
    
    def __init__(self, name: str, industry: str, num_employees: int):
        self.name = name
        self.industry = industry
        self.num_employees = num_employees

    def __repr__(self):
        return f"Company(name={self.name}, industry={self.industry}, num_employees={self.num_employees})"
    

class Employee:
    
    def __init__(self, first_name: str, last_name: str, email: str, position: str, company: Company):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.position = position
        self.company = company
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def validate_email(self) -> bool:
        return "@" in self.email and "." in self.email.split("@")[-1]

    def __repr__(self):
        return f"Employee(first_name={self.first_name}, last_name={self.last_name}, email={self.email}, position={self.position}, company={self.company.name})"
    
    
# Nueva clase Project con asociacion Many To Many con Employee
class Project:
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.employees = []  # Lista para almacenar empleados asociados al proyecto

    def add_employee(self, employee: Employee):
        if employee not in self.employees:
            self.employees.append(employee)

    def remove_employee(self, employee: Employee):
        if employee in self.employees:
            self.employees.remove(employee)

    def __repr__(self):
        return f"Project(name={self.name}, description={self.description}, employees={[emp.first_name + ' ' + emp.last_name for emp in self.employees]})"
    
    

# Nueva clase Team
class Team:
    """Equipo dentro de una empresa."""
    def __init__(self, name: str, company: 'Company'):
        self.name = name
        self.company = company
        self.members: list[Employee] = []

    def add_member(self, e: Employee):
        if e not in self.members:
            self.members.append(e)

    def __repr__(self):
        return f"Team(name={self.name}, company={self.company.name})"


# Nueva clase Task
class Task:
    """Tarea asignable a empleados y proyectos."""
    def __init__(self, title: str, description: str, assignee: Employee | None = None):
        self.title = title
        self.description = description
        self.assignee = assignee
        self.completed = False

    def mark_done(self):
        self.completed = True

    def __repr__(self):
        return f"Task(title={self.title}, assignee={self.assignee.full_name if self.assignee else None})"


# Nueva clase Issue
class Issue:
    """Issue / bug report simple."""
    def __init__(self, title: str, reporter: Employee, project: 'Project'):
        self.title = title
        self.reporter = reporter
        self.project = project
        self.open = True

    def close(self):
        self.open = False

    def __repr__(self):
        return f"Issue(title={self.title}, project={self.project.name}, open={self.open})"


# Nueva clase PullRequest
class PullRequest:
    """Representación pedagógica de un PR."""
    def __init__(self, title: str, author: Employee, project: 'Project'):
        self.title = title
        self.author = author
        self.project = project
        self.merged = False

    def merge(self):
        self.merged = True

    def __repr__(self):
        return f"PullRequest(title={self.title}, author={self.author.full_name}, merged={self.merged})"


# Nueva clase TestCase
class TestCase:
    """Caso de prueba simple para vincular a Task/Project."""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.passed = None  # None = no ejecutado, True/False = resultado

    def run(self, result: bool):
        self.passed = result

    def __repr__(self):
        return f"TestCase(name={self.name}, passed={self.passed})"
