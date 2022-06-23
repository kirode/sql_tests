def update_query(query_dict: dict) -> str:
    values = ''
    for key, value in query_dict.items():
        values += f'{key}=\'{value}\', '
    index = values.rfind(',')
    return values[:index] + ' '


def insert_query(query_dict: dict) -> tuple[tuple, tuple]:
    columns = []
    values = []
    for key, value in query_dict.items():
        columns.append(key)
        values.append(value)
    return tuple(columns), tuple(values)

