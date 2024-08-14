import json


def str_decode(b: str):
    """字符串解码"""
    if isinstance(b, bytes):
        return b.decode('utf-8', errors='ignore')
    else:
        return str(b)


def data_encode(input_dict: dict):
    """编码成json格式的数据"""
    return json.dumps(input_dict)


def data_decode(input_dict: str):
    """解码json格式的数据"""
    return json.loads(input_dict)


def process_dict_recursively(data, process_fn, parent_key=None, **kwargs):
    """
    Recursively process each element in a dictionary.

    :param data: The dictionary to process.
    :param process_fn: A function that takes a key and value as arguments and performs some operation.
    :param parent_key: The key of the parent element in case of nested dictionaries.
    :param kwargs: Any parameter.
    :return: A new dictionary with the processed elements.
    """
    if isinstance(data, dict):
        return {k: process_dict_recursively(v, process_fn, k, **kwargs) for k, v in data.items()}
    elif isinstance(data, list):
        return [process_dict_recursively(element, process_fn, parent_key, **kwargs) for element in data]
    else:
        return process_fn(parent_key, data, **kwargs)