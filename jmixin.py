import json
from inspect import signature


class JSerializerMixin:
    # todo: refactor into different methods as fit. single responsibility.
    # todo: check type annotations, and check attribute value type against annotations
    # if there aren't annotations, we can't really guarantee safeguards for the user.
    # todo: set class attributes only once? how do we handle these..

    def to_json(self):
        """Return the current instance as a json string."""
        return json.dumps(self.__dict__)

    @staticmethod
    def _annotations_check(cls, json_object):
        """Ensure deserialized json object adheres to type annotations"""
        pass
    
    @classmethod
    def from_json(cls, json_string):
        """Create a new instance of cls from a json string."""
        new_class: type(cls) # uninitialized var of type cls
        json_object = json.loads(json_string)

        # Does cls have a callable __init__ method?
        if hasattr(cls, '__init__') and callable( getattr(cls, '__init__') ):
            # todo: ensure correct class by checking annotations, and raise error if they don't match
            
            init_signature = signature(cls.__init__)
            init_params = dict(init_signature.parameters) # keys are param names. values are just Parameter types (we will not use) 

            # create a set from deserialized instance attrs that doesn't include init params
            # this will allow us to not set the same init instance attrs twice
            json_without_signature = set(json_object.items()) - set(init_params.items())

            # remove self after json_without_signature so that self isn't in difference set
            del init_params['self'] # omit self from arguments to be initialized
            
            # set init param argument values to actual deserialized values (not Parameter type values)
            for key in init_params.keys():
                init_params[key] = json_object[key]

            # finally, initialize out new object with init_params
            new_class = cls(**init_params)
            
            # premature/minute optimization? measure performance with/without and check
            json_object = dict(json_without_signature)
        
        # set instance attributes that aren't in __init_: 
        # is there a way to improve performance here?
        for key, value in json_object.items():
            new_class.__dict__[key] = value
        
        return new_class
