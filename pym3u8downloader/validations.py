def validate_type(value, expected_type, message) -> None:
    """
    Validates if the given value has the expected type.

    :param value: The value to be validated.
    :type value: Any
    :param expected_type: The expected type for the value.
    :type expected_type: type
    :param message: The error message to be raised if the type check fails.
    :type message: str
    """
    if not isinstance(value, expected_type):
        raise TypeError(message)
