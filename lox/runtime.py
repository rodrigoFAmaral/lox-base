from .ast import Value


def lox_print(value: Value):
    """
    Imprime um valor lox.
    """
    print(lox_show(value))


def lox_show(value: Value) -> str:
    """
    Converte valor lox para string.
    """
    if value is None:
        return "nil"
    elif isinstance(value, str):
        return value
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        else:
            return str(value)
    else:
        return str(value)
