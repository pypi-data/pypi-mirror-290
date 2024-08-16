from transformFunctions import transform
from functools import wraps

class TransformStructure:
    def __init__(self,
                    case_type = "snakeToCamel",
                    transform_for  = "return",
                    arg_index  = 0,
                    arg_name = ""
                ):
        self.case_type = case_type
        self.transform_for = transform_for
        self.arg_index = arg_index
        self.arg_name = arg_name

    def __call__(self, func):
        @wraps(func)
        async def wrapper_func(*args, **kwargs):
            if self.transform_for == "argument":
                local_args = list(args)
                local_kwargs = dict(kwargs)
                if len(args) > 0:
                    if isinstance(self.arg_index, (list)):
                        for idx in self.arg_index:
                            local_args[idx] = transform(local_args[idx], self.case_type)
                    else:
                        local_args[self.arg_index] = transform(local_args[self.arg_index], self.case_type)
                if len(list(kwargs.keys())) > 0:
                    if isinstance(self.arg_name, (list)):
                        for key in self.arg_name:
                            if key in local_kwargs:
                                local_kwargs[key] = transform(local_kwargs[key], self.case_type)
                    else:
                        local_kwargs[self.arg_name] = transform(local_kwargs[self.arg_name], self.case_type)

                await func(*local_args, **local_kwargs)
        
            elif self.transform_for == "return":
                return transform(await func(*args, **kwargs), self.case_type)

        return wrapper_func
    

def transform_structure_async(case_type = "snakeToCamel",
        transform_for  = "return",
        arg_index = 0,
        arg_name = ""):
    """Functoin that returnes descriptor to asynchronus transform target function

    Args:
        case_type (str, optional): type of transform rule (`snakeToCamel`, `camelToSnake`). Defaults to "snakeToCamel".
        transform_for (str, optional): target of executon transform (`return`, `argument`). Defaults to "return".
        arg_index (int, optional): Index of argument of target function. Defaults to 0.
        arg_name (str, optional): Name of argument of target function. Defaults to "".
    """
    def decorator(func):
        return TransformStructure(
            case_type,
            transform_for,
            arg_index,
            arg_name
        )(func)
    
    return decorator