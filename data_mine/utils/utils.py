def parse_measurement(s):
    # Remove commas from the string
    s = s.replace(',', '')
    
    # Find the measurement pattern
    pattern = r"(\d+(?:\.\d+)?)\s*([a-zA-Z]+)"
    matches = re.findall(pattern, s)
    
    matches2 = re.findall(r"\(.*\)", s)

    if len(matches) == 1:
        value, unit = matches[0]
        return {"value": float(value), "units": unit}
    elif len(matches) == 2:
        value1, unit1 = matches[0]
        value2, unit2 = matches[1]

        if len(matches2) > 0:
            return {"value": float(value1), "units": unit1}

        else:
            return {"values": [float(value1), float(value2)], "units": unit2}

    else:
        return None