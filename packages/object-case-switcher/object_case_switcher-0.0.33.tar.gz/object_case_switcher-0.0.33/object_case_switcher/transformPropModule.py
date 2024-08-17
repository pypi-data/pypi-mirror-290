from .TransformStructure import transform_structure_async
from .transformFunctions import transform_structure_sync


def transform_structure(
        case_type = "snakeToCamel",
        transform_for  = "return",
        arg_index  = 0,
        arg_name = "",
        _async=True
):
    """Main function to create neccessary decorator by provided _async value

    Args:
        case_type (str, optional): Type of transform rule (`snakeToCamel`, `camelToSnake`). Defaults to "snakeToCamel".
        transform_for (str, optional): Target of executon transform (`return`, `argument`). Defaults to "return".
        arg_index (int, optional): Index of argument of target function. Defaults to 0.
        arg_name (str, optional): Name of argument of target function. Defaults to "".
        _async (bool, optional): Is synchronus or asynchronus target function . Defaults to True.

    Returns:
        decorator: Neccessary decorator
    """
    if _async:
        return transform_structure_async(case_type,
            transform_for,
            arg_index,
            arg_name,
        )
    return transform_structure_sync(case_type,
        transform_for,
        arg_index,
        arg_name,
    )
