"""Argument contract validation with exact keys and strict scalar types."""


class ContractError(ValueError):
    pass


def validate(arguments, required):
    if not isinstance(arguments, dict) or set(arguments) != set(required):
        raise ContractError("Tool arguments do not match declared fields")
    for name, kind in required.items():
        value = arguments[name]
        if kind not in (str, int, float, bool):
            raise ContractError("Only simple scalar contracts are supported")
        if kind is int and type(value) is bool:
            raise ContractError(f"{name} must be integer")
        if kind is float and type(value) not in (float, int):
            raise ContractError(f"{name} must be numeric")
        if kind is not float and not isinstance(value, kind):
            raise ContractError(f"{name} must be {kind.__name__}")
    return True
