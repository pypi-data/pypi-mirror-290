# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long
# pylint: disable=missing-class-docstring
# pylint: disable=broad-exception-caught

def list_as_strings(*enums):
    """Converts a list of Enum members to their string values."""
    return [str(enum) for enum in enums]
