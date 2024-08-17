from .utils import *
from functools import wraps

import asyncio
# isAsyncFunc = asyncio.iscoroutinefunction(func)

ATOMIC_CLASSES = (str, int, float)
FUNCTIONS = {
    "snakeToCamel": snake_to_camel,
    "camelToSnake": camel_to_snake,
}

def transform(object, case_type = "snakeToCamel"):
    """Recursive funtion transform provided `object`'s properties by `case_type`

    Args:
        object (object): target object to transform
        case_type (str, optional): Type of transform rule (`snakeToCamel`, `camelToSnake`). *Defaults to "snakeToCamel"*.

    Returns:
        object: Transformed object
    """
    if not isinstance(object, (list, dict)): return object

    res: list | dict = {}
    is_list: bool = False
    if isinstance(object, (list)):
        res = []
        is_list = True

    for key in object if not is_list else range(len(object)):
        if isinstance(object[key], ATOMIC_CLASSES) or object[key] is None:
            if is_list:
                res.append(object[key])
            else:
                res[FUNCTIONS[case_type](key)] = object[key]
        elif isinstance(object[key], (list, dict)):
            if is_list:
                res.append(transform(object[key], case_type))
            else:
                res[FUNCTIONS[case_type](key)] = transform(object[key], case_type)
    return res


def transform_structure_sync(

        case_type = "snakeToCamel",
        transform_for  = "return",
        arg_index  = 0,
        arg_name = ""

    ):
    """Functoin that returnes descriptor to synchronus transform target function

    Args:
        case_type (str, optional): type of transform rule (`snakeToCamel`, `camelToSnake`). Defaults to "snakeToCamel".
        transform_for (str, optional): target of executon transform (`return`, `argument`). Defaults to "return".
        arg_index (int, optional): Index of argument of target function. Defaults to 0.
        arg_name (str, optional): Name of argument of target function. Defaults to "".
    """
    def decorator(func):
        @wraps(func)
        def wrapper_func(*args, **kwargs):
            if transform_for == "argument":
                local_args = list(args)
                local_kwargs = dict(kwargs)
                if len(args) > 0:
                    if isinstance(arg_index, (list)):
                        for idx in arg_index:
                            local_args[idx] = transform(local_args[idx], case_type)
                    else:
                        local_args[arg_index] = transform(local_args[arg_index], case_type)
                if len(list(kwargs.keys())) > 0:
                    if isinstance(arg_name, (list)):
                        for key in arg_name:
                            if key in local_kwargs:
                                local_kwargs[key] = transform(local_kwargs[key], case_type)
                    else:
                        local_kwargs[arg_name] = transform(local_kwargs[arg_name], case_type)

                func(*local_args, **local_kwargs)
        
            elif transform_for == "return":
                return transform(func(*args, **kwargs), case_type)
    
        return wrapper_func
    
    return decorator