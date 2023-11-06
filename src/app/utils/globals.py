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
