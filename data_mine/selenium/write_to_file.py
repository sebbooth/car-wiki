import json

def is_duplicate(data_list, new_data):
    for data in data_list:
        if data == new_data:
            return True
    return False

def write_to_file(filename, new_data):
    with open(filename, "r") as json_file:
        try:
            existing_data = json.load(json_file)
        except json.JSONDecodeError:
            existing_data = []

    for object in new_data:
        if not is_duplicate(existing_data, object):
            existing_data.append(object)

            with open(filename, "w") as json_file:
                json.dump(existing_data, json_file, indent=4)