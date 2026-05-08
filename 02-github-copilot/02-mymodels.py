class MyCompany:
    def __init__(self, name, employees):
        self.name = name
        self.employees = employees

    def add_employee(self, employee):
        self.employees.append(employee)

    def get_employee_count(self):
        return len(self.employees)
    
class MyEmployee:
    def __init__(self, first_name : str, last_name : str, email : str, my_company : MyCompany):
        self.first_name = first_name
        self.last_name = last_name
        self.email = self.validate_email()
        if not self.email:
            raise ValueError("Invalid email address")
        self.my_company = my_company

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def validate_email(self) -> bool:
        return "@" in self.email and "." in self.email.split("@")[-1]
    
# Nueva clase MyProject con asociacion Many To Many con MyEmployee
class MyProject:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.employees = []  # Lista para almacenar empleados asociados al proyecto

    def add_employee(self, employee):
        if employee not in self.employees:
            self.employees.append(employee)

    def remove_employee(self, employee):
        if employee in self.employees:
            self.employees.remove(employee)