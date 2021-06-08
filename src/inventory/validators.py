from collections import namedtuple

ValidationValue = namedtuple("ValidationValue", "is_valid, message")


def val_str(data: str) -> ValidationValue[bool, str]:
    try:
        return ValidationValue(True, str(data))
    except ValueError:
        return ValidationValue(False, f"Value '{data}' is not a valid string")


def val_int(data: str) -> ValidationValue[bool, int or str]:
    try:
        return ValidationValue(True, int(data))
    except ValueError:
        return ValidationValue(False, f"Value '{data}' is not a valid integer")


def check_type(data: list, data_type=list) -> ValidationValue[bool, str]:
    if isinstance(data, data_type):
        return ValidationValue(True, data)
    return ValidationValue(False, f"Value '{data}' is not a valid type")
