from typing import get_type_hints, Iterable
import inspect

class TypeException(Exception):
    pass

def type_checker(func):
    type_hints = get_type_hints(func)
    
    def wrapper(*args, **kwargs):
        signature = inspect.signature(func)
        bound_arguments = signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()

        for param_name, param_value in bound_arguments.arguments.items():
            if param_name in type_hints:
                expected_type = type_hints[param_name]
                if not isinstance(param_value, expected_type):
                    if isinstance(param_value, (list, tuple, set)) and isinstance(expected_type, Iterable):
                        expected_element_type = expected_type.__origin__.__args__[0]
                        if not all(isinstance(item, expected_element_type) for item in param_value):
                            raise TypeException(f"Argument '{param_name}' should be of type {expected_type.__name__}, but got {type(param_value).__name__} with elements of type {type(param_value[0]).__name__}.")
                    else:
                        raise TypeException(f"Argument '{param_name}' should be of type {expected_type.__name__}, but got {type(param_value).__name__}.")

        result = func(*args, **kwargs)
        if 'return' in type_hints:
            expected_return_type = type_hints['return']
            if not isinstance(result, expected_return_type):
                raise TypeException(f"Return value should be of type {expected_return_type.__name__}, but got {type(result).__name__}.")

        return result

    return wrapper