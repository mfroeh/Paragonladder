def nice_number(number: int) -> str:
    if number >= 1_000_000_000_000_000:
        return str(round(number / 1_000_000_000_000_000, 2)) + " Quadrillion"
    elif number >= 1_000_000_000_000:
        return str(round(number / 1_000_000_000_000, 2)) + " Trillion"
    elif number >= 1_000_000_000:
        return str(round(number / 1_000_000_000, 2)) + " Billion"
    elif number >= 1_000_000:
        return str(round(number / 1_000_000, 2)) + " Million"

    return str(round(number))
