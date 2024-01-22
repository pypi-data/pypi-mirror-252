import math


def format_two_decimals(num: float) -> float:
    """
    Returns a float rounded to two decimal places using math.ceil

    Args:
        num (float): a float number

    Returns:
        _type_: a float number rounded up to two decimal places
    """
    return math.ceil((num) * 100) / 100


def round_two_decimals(num: float) -> float:
    """
    Returns a float rounded to two decimal places using round

    Args:
        num (float): a float number

    Returns:
        _type_: a float number rounded to two decimal places using round
    """
    return round(num, 2)


def display_float_with_2_decimals(num: float) -> float:
    return f"{num:.2f}"
