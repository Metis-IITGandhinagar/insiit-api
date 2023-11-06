def json_to_sql(json_data):
    if isinstance(json_data, dict):
        items = []
        for key, value in json_data.items():
            items.append(json_to_sql(key))
            items.append(json_to_sql(value))
        return f'JSON_BUILD_OBJECT({", ".join(items)})'
    elif isinstance(json_data, list):
        elements = [json_to_sql(element) for element in json_data]
        return f'JSON_BUILD_ARRAY({", ".join(elements)})'
    elif isinstance(json_data, str):
        return f"'{json_data}'"
    elif isinstance(json_data, (int, float)):  # Handle numeric values
        return str(json_data)
    else:
        return str(json_data)
