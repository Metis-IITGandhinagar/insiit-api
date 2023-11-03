def json_to_sql(json_data):
    if isinstance(json_data, dict):
        items = []
        for key, value in json_data.items():
            items.append(json_to_sql(key))
            items.append(json_to_sql(value))
        return f'JSON_OBJECT({", ".join(items)})'
    elif isinstance(json_data, list):
        elements = [json_to_sql(element) for element in json_data]
        return f'JSON_ARRAY({", ".join(elements)})'
    elif isinstance(json_data, str):
        return f"'{json_data}'"
    elif isinstance(json_data, (int, float)):  # Handle numeric values
        return str(json_data)
    else:
        return str(json_data)


def obj_to_json(obj):
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj

    if isinstance(obj, dict):
        serialized_dict = {}
        for key, value in obj.items():
            serialized_dict[key] = obj_to_json(value)
        return serialized_dict

    if isinstance(obj, list):
        serialized_list = []
        for item in obj:
            serialized_list.append(obj_to_json(item))
        return serialized_list

    if hasattr(obj, "__dict__"):
        obj_dict = obj.__dict__
        serialized_obj = {}
        for key, value in obj_dict.items():
            serialized_obj[key] = obj_to_json(value)
        return serialized_obj

    return str(obj)
