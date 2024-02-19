import json

def is_duplicate(data_list, new_data):
    for data in data_list:
        if data == new_data:
            return True
    return False


def write_to_file_json(filePath, new_data):
    with open(filePath, "r", encoding="utf-8") as json_file:
        try:
            existing_data = json.load(json_file)
        except json.JSONDecodeError:
            existing_data = []

    for object in new_data:
        if not is_duplicate(existing_data, object):
            existing_data.append(object)

            with open(filePath, "w", encoding="utf-8") as json_file:
                json.dump(existing_data, json_file, indent=4)
    
    json_file.close()


def write_to_file_fields(filePath, new_data):
    with open(filePath, "r", encoding="utf-8") as json_file:
        try:
            existing_data = json.load(json_file)
        except json.JSONDecodeError:
            existing_data = {}

    for category in new_data:
        if category in existing_data:
            fields = set(existing_data[category])
            for field in new_data[category]:
                fields.add(field)

            existing_data[category] = list(fields)
        else:
            existing_data[category] = new_data[category]

    with open(filePath, "w", encoding="utf-8") as json_file:
        json.dump(existing_data, json_file, indent=4)
    
    json_file.close()

def read_file_fields(filePath):
    with open(filePath, "r", encoding="utf-8") as json_file:
        try:
            existing_data = json.load(json_file)
        except json.JSONDecodeError:
            existing_data = {}

    return existing_data

def write_to_file_link_list(filePath, links):
    existing_links = set() 
    try:
        with open(filePath, "r", encoding="utf-8") as file:
            for line in file:
                existing_links.add(line.strip())  
    except FileNotFoundError:
        pass  

    new_unique_links = [link for link in links if link not in existing_links]

    with open(filePath, "a", encoding="utf-8") as file:
        for link in new_unique_links:
            file.write(link + "\n")

    file.close()

def write_to_file_link_set(filePath, linkSet):
    existing_pairs = {}
    try:
        with open(filePath, "r", encoding="utf-8") as file:
            for line in file:
                key, value = line.strip().split(",", 1)
                existing_pairs[key] = value
    except FileNotFoundError:
        pass

    new_pairs = {k: v for k, v in linkSet.items() if k not in existing_pairs}

    with open(filePath, "a", encoding="utf-8") as file:
        for key, value in new_pairs.items():
            file.write(f"{key} {value}\n")
    file.close()

def append_to_file_link_list(file_path, link):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(link + "\n")
    file.close()

def append_to_file_link_set(file_path, link, title):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"{link} {title}\n")
    file.close()


def read_file_link_list(filePath):
    existing_links = []
    try:
        with open(filePath, "r", encoding="utf-8") as file:
            for line in file:
                existing_links.append(line.rstrip('\n'))
        file.close()
    except FileNotFoundError:
        pass  
    return list(existing_links)

def read_file_link_set(filePath):
    existing_pairs = {}
    try:
        with open(filePath, "r", encoding="utf-8") as file:
            for line in file:
                key, value = line.rstrip('\n').split(" ", 1)
                existing_pairs[key] = value
        file.close()
    except FileNotFoundError:
        pass
    return existing_pairs

def pop_link(filePath):
    link = ""
    with open(filePath, 'r', encoding="utf-8") as file:
        lines = file.readlines()

    if lines:
        link = lines[-1].rstrip('\n')
        lines = lines[:-1]

    with open(filePath, 'w', encoding="utf-8") as file:
        file.writelines(lines)
    file.close()

    return link

def read_carsdotcom_json(filePath):
    with open(filePath, "r", encoding="utf-8") as json_file:
        try:
            existing_data = json.load(json_file)
        except json.JSONDecodeError:
            existing_data = {}
    return existing_data