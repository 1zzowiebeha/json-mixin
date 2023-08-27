import json
from inspect import signature


class SerializerMixin: # mixin should not have conflicting __init__ method
    def to_json(self):
        # todo: ensure security by checking annotations
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_string, *args):
        new_class: type(cls)
        json_object = json.loads(json_string)

        # Does cls have an __init__ method?
        if hasattr(cls, '__init__') and callable( getattr(cls, '__init__') ):
            init_signature = signature(cls.__init__)
            new_class = cls(**init_signature.parameters) # initialize our object with keyword args
            
            # take right venn diagram so we don't set the same variables again
            json_object = json_object ^ init_signature
             
        # set unset instance methods:
        # improve performance for this with vars() maybe?
        for key, value in json_object.items():
            new_class.__dict__[key] = value
        
        return new_class


class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        string = f"{type(self).__name__}("
        
        for key, value in self.__dict__.items():
            string += f"{key} = {value},"

        string = ")"


class Employee(SerializerMixin, Person):
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

    
if __name__ == "__main__":
    main()
