from typing import get_type_hints, Iterable
import inspect

class TypeException(Exception):
    pass

def type_checker(func):
    type_hints = get_type_hints(func)

    def check_type(param_value, expected_type):
        if isinstance(expected_type, type):
            # Direct type check
            if not isinstance(param_value, expected_type):
                raise TypeException(f"Expected type {expected_type.__name__}, but got {type(param_value).__name__}.")
        elif hasattr(expected_type, '__origin__'):
            # Handle generic types
            origin = expected_type.__origin__
            if origin in (list, tuple, set):
                if not isinstance(param_value, origin):
                    raise TypeException(f"Expected type {expected_type.__name__}, but got {type(param_value).__name__}.")
                
                # Check the type of elements
                element_type = expected_type.__args__[0]
                if not all(isinstance(item, element_type) for item in param_value):
                    raise TypeException(f"Expected all elements to be of type {element_type.__name__}, but got elements of type {[type(item).__name__ for item in param_value]}.")
            elif origin is dict:
                if not isinstance(param_value, dict):
                    raise TypeException(f"Expected type {expected_type.__name__}, but got {type(param_value).__name__}.")
                
                key_type, value_type = expected_type.__args__
                if not all(isinstance(k, key_type) for k in param_value.keys()):
                    raise TypeException(f"Expected all keys to be of type {key_type.__name__}, but got keys of type {[type(k).__name__ for k in param_value.keys()]}.")
                if not all(isinstance(v, value_type) for v in param_value.values()):
                    raise TypeException(f"Expected all values to be of type {value_type.__name__}, but got values of type {[type(v).__name__ for v in param_value.values()]}.")
            else:
                raise TypeException(f"Unsupported generic type {expected_type}.")
        else:
            raise TypeException(f"Unsupported type {expected_type}.")

    def wrapper(*args, **kwargs):
        signature = inspect.signature(func)
        bound_arguments = signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()

        for param_name, param_value in bound_arguments.arguments.items():
            if param_name in type_hints:
                expected_type = type_hints[param_name]
                check_type(param_value, expected_type)

        result = func(*args, **kwargs)
        return result

    return wrapper