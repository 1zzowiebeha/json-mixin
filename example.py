from jmixin import JSerializerMixin

class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        string = f"{type(self).__name__}("
        
        for key, value in self.__dict__.items():
            string += f"{key} = {value},"

        string = ")"


class Employee(JSerializerMixin, Person):
    def __init__(self, name, age, salary):
        super().__init__(name, age) # init person
        self.salary = salary
        self._spooky = True
        
        self.to_json() # must reference self
        
    def greeting(self):
        print("hello!")


def main():
    employee = Employee('Jogn', 44, 12000)
    employee2 = Employee.from_json(employee.to_json())
    
    employee2.greeting()
    print(employee2._spooky)

    
if __name__ == "__main__":
    main()
