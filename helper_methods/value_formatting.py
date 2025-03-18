def format_price_value_to_float(price_value: str) -> float:
    return float(price_value.replace("$", ""))


def round_value_to_two_decimal_places(value: float) -> float:
    return round(value, 2)


def format_value_to_two_decimal_places(value: float) -> str:
    return f"{value:.2f}"
