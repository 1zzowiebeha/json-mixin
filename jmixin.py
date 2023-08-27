import json
from inspect import signature


class JSerializerMixin: # mixin should not have conflicting __init__ method
    def to_json(self):
        # todo: ensure security by checking annotations
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_string):
        new_class: type(cls) # uninitialized var of type cls
        json_object = json.loads(json_string)

        # Does cls have an __init__ method?
        if hasattr(cls, '__init__') and callable( getattr(cls, '__init__') ):
            init_signature = signature(cls.__init__)
            init_params = dict(init_signature.parameters) # keys are param names. values are just Parameter types (we will not use) 

            # create a set from deserialized instance attrs that doesn't include init params
            # this will allow us to not set the same init instance attrs twice
            json_without_signature = set(json_object.items()) - set(init_params.items())

            del init_params['self'] # omit self from arguments to be initialized
            
            # set init param argument values to actual deserialized values (not Parameter type values)
            for key in init_params.keys():
                init_params[key] = json_object[key]

            # finally, initialize out new object with init_params
            new_class = cls(**init_params)
            
            # premature/minute optimization? measure performance with/without and check
            json_object = dict(json_without_signature)
        
        # set instance attributes that aren't in __init_: 
        # improve performance for this with vars() maybe?
        for key, value in json_object.items():
            new_class.__dict__[key] = value
        
        return new_class
