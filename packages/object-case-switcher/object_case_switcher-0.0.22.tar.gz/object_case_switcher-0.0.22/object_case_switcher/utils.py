def snake_to_camel(key):
    """Function transform provided string (key) from snake_case to camelCase

    Args:
        key (str): target string (key)

    Returns:
        string: transformed string
    """
    nameValues = key.split("_")
    return nameValues[0] + "".join(map(lambda x: x[0].upper() + x[1:], nameValues[1:]))


def camel_to_snake(key):
    """Function transform provided string (key) from camelCase to snake_case

    Args:
        key (str): target string (key)

    Returns:
        string: transformed string
    """
    nameValues = get_list_of_names(key)
    return "_".join(map(lambda x: x if x.isupper() else x[0].lower() + x[1:], nameValues))


def get_list_of_names(key):
    """Function returnes list of words in camelCase string

    Args:
        key (str): target string

    Returns:
        list: list of words
    """
    startIndex = 0
    res = []
    for i in range(len(key) - 1):
        if key[i].isupper() and key[i + 1].islower():
            res.append(key[startIndex : i])
            startIndex = i

    res.append(key[startIndex:])
    return res