from datetime import datetime
def toIntSafe(value):
    return int(value) if value else None

def toFloatSafe(value):
    return float(value) if value else None

def transformBoolean(value, inputs=['t', 'f']):
    """
    Converts a value to boolean based on the provided true/false inputs.
    Args:
        value: The input value to convert.
        inputs: List where the first element is considered True, the second False.
    Returns:
        bool: True or False.
    """
    if value == inputs[0]:
        return True
    elif value == inputs[1]:
        return False
    else:
        raise ValueError(f"Value '{value}' is not recognized as boolean input.")
code = {
    "Entire home/apt": 'entire',
    "Private room": 'private',
    "Hotel room": 'hotel',
    "Shared room": 'shared'
}
def transformCode(value, _code=code):
    return _code[value]

def toDateSafe(date_string, fmt="%Y-%m-%d"):
    if not date_string:
        return None
    try:
        return datetime.strptime(date_string, fmt).date()
    except ValueError:
        return None

