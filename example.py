from jmixin import JSerializerMixin


class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Employee(JSerializerMixin, Person):
    def __init__(self, name, age, salary):
        super().__init__(name, age) # init person
        self.salary = salary
        self._hidden_var = "This variable was rehydrated too!"
        
    def greeting(self):
        print("hello!")


def main():
    """Put entry-point body into local scope instead of global. This helps
    programs that import this module to avoid name conflicts."""
    employee = Employee('Jorgn', 44, 100_000)
    
    employee_json = employee.to_json()
    employe_from_json = Employee.from_json(employee_json)
    
    employe_from_json.greeting()
    print(employe_from_json._hidden_var)
    
    # Success!

    
if __name__ == "__main__":
    main()
