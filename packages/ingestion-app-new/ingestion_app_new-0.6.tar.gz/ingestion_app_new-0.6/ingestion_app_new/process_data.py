CSV_SEPARATOR = ','


def read_input_file(input_file_path):
    try:
        with open(input_file_path, 'r') as file:
            input_data = file.read()
        return input_data
    except FileNotFoundError:
        print(f"Error: File '{input_file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading file '{input_file_path}': {e}")
        return None
    
def process_data(input_data, important_keys):
    """
    Process input data and extract important keys.

    Args:
        input_data (str): Raw input data.
        important_keys (list): List of keys to extract from input data.

    Returns:
        list: List of dictionaries containing processed data.
    """
    processed_data = []

    for line in input_data.split('\n'):
        if line.strip():
            entity = {}
            fields = line.split(CSV_SEPARATOR)

            for field in fields:
                key, value = field.split('=')
                if key in important_keys:
                    entity[key] = value

            processed_data.append(entity)

    return processed_data

def sort_data_by_hierarchy(processed_data, type_hierarchy):
    """
    Sort processed data by a specified type hierarchy.

    Args:
        processed_data (list): List of dictionaries containing processed data.
        type_hierarchy (list): List specifying the order for sorting by 'type'.

    Returns:
        list: Sorted list of dictionaries.
    """
    data_with_type = [row for row in processed_data if 'type' in row]
    sorted_data = sorted(data_with_type, key=lambda x: type_hierarchy.index(x.get('type')))
    # sorted_data = sorted(data_with_type, key=lambda x: type_hierarchy.index(x.get('type')) if x.get('type') in type_hierarchy else len(type_hierarchy))
    return sorted_data

def validate_data(data, key_data_types):
    """
    Validate data types in a list of dictionaries.

    Args:
        data (list): List of dictionaries containing data to be validated.
        key_data_types (dict): Dictionary mapping keys to their expected data types.

    Returns:
        list: List of dictionaries containing validated data.
    """
    validated_data = []

    for row in data:
        validated_row = {}
        skip_row = False  # Flag to determine whether to skip the entire row

        for key, data_type in key_data_types.items():
            value = row.get(key, '')

            # Validate data type
            try:
                if data_type == 'int':
                    validated_value = int(value)
                elif data_type == 'str':
                    validated_value = str(value)
                else:
                    validated_value = value  # No validation for other data types (you can add more cases)

                # Add the validated value to the row
                validated_row[key] = validated_value
            except (ValueError, TypeError):
                skip_row = True  # Skip row if a data type validation error occurs
                break

        # Append the validated row to the list only if no data type validation errors occurred
        if not skip_row:
            validated_data.append(validated_row)

    return validated_data

def print_values_in_csv_format(val_data, header):
    csv_output = []
    for row in val_data:
        values = [str(row.get(key, '')) for key in header]
        csv_output.append(CSV_SEPARATOR.join(values))
    return csv_output



def sort_data_by_hierarchy_updated(processed_data, type_hierarchy):
    """
    Sort processed data by a specified type hierarchy.

    Args:
        processed_data (list): List of dictionaries containing processed data.
        type_hierarchy (list): List specifying the order for sorting by 'type'.

    Returns:
        list: Sorted list of dictionaries.
    """
    data_with_type = [row for row in processed_data if 'type' in row]
    sorted_data = sorted(data_with_type, key=lambda x: type_hierarchy.index(x.get('type')))
    return sorted_data