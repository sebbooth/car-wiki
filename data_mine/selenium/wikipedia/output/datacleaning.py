import json
import re


def clean_json_data(data):

    def split_newlines(value):
        if not isinstance(value, str):
            return value
        if '\n' not in value:
            return value
        return value.split("\n")

    def split_u2013(value):
        if not isinstance(value, str):
            return value
        
        if '\u2013' not in value:
            return value
        
        match = re.split(r'\u2013', value)
        return {"start": match[0], "end": match[1]}

    def split_colon(value):
        if not isinstance(value, str):
            return value
        
        if ':' not in value or value.rstrip()[-1] == ':':
            return value
        
        match = re.split(r':', value, maxsplit=1)
        if (match[0] == "https") or (match[0] == "http"):
            return value
        return {match[0].strip(): match[1].strip()}

    def restructure_list(lst):
        if not isinstance(lst, list):
            return lst
        
        result = {}
        current_key = None
        for item in lst:
            if re.match(r'.+:$', item):
                current_key = item[:-1]
                result[current_key] = []
            elif current_key is not None:
                result[current_key].append(item)
        if result == {}:
            return lst
        return result

    def remove_bracketed_numbers(s):
        if not isinstance(s, str):
            return s
        return re.sub(r'\[\d+\]', '', s)

    def split_and(s):
        if not isinstance(s, str):
            return s
        if '&' not in s:
            return s
        return [value.strip() for value in s.split("&")]

    def parse_measurement(s):
        if not isinstance(s, str):
            return s
        match = re.match(r'([\d,]+)\s+(\w+)', s)
        if match:
            value = match.group(1).replace(',', '')
            units = match.group(2)
            return {"value": float(value) if '.' in value else int(value), "units": units}
        else:
            return s
        
    def parse_body_type(s):
        if not isinstance(s, str):
            return s
        match = re.match(r'(\d+)-door\s*(\w+)\s*(\(.*\))?', s)
        if match:
            doors = int(match.group(1))
            body_type = match.group(2)
            notes = match.group(3) if match.group(3) else ""
            return {"doors": doors, "body-type": body_type, "notes": notes}
        else:
            return s
        
    def parse_engine_type(s):
        if not isinstance(s, str):
            return s
        match = re.match(r'(\d+\.\d+)\s*L\s*(.*)\s*(\w+\d+)', s)
        if match:
            displacement = {"value": float(match.group(1)), "units": "L"}
            engine_code = match.group(2).strip()
            engine_type = match.group(3)
            return {"displacement": displacement, "engine-code": engine_code, "engine-type": engine_type}
        else:
            return s
 

    orig = None
    if isinstance(data, dict):
        orig = dict(data)

        for key, value in data.items():
            data[key] = clean_json_data(value)

    else:
        if isinstance(data, list):
            for i, item in enumerate(data):
                data[i] = clean_json_data(item)

        elif isinstance(data, str):
            data = split_newlines(data)
            data = split_colon(data)
            data = split_and(data)
            data = split_u2013(data)
            data = restructure_list(data)
            data = remove_bracketed_numbers(data)
            data = parse_measurement(data)
            data = parse_body_type(data)
            data = parse_engine_type(data)
    if orig != None and orig != data:
        clean_json_data(data)
    return data


with open('data.json') as f:
    data = json.load(f)

data = clean_json_data(data)

# Print the cleaned JSON data
print(json.dumps(data, indent=4))