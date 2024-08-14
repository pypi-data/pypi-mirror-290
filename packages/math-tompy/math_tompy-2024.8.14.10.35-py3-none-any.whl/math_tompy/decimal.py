from decimal import Decimal


def normalize_value(value: Decimal, minimum: Decimal, maximum: Decimal) -> Decimal:
    """Scale value position between minimum and maximum to [0:1] bound"""

    # Scale value and maximum relative to zero to enable finding fractional value by straightforward division
    zero_scaled_value: Decimal = value - minimum
    zero_scaled_maximum: Decimal = maximum - minimum

    # Divide scaled values
    normalized_value: Decimal = zero_scaled_value / zero_scaled_maximum

    return normalized_value


def clamp_or_normalize_value(value: Decimal, minimum: Decimal, maximum: Decimal) -> Decimal:
    new_value: Decimal

    if value < minimum:
        new_value = Decimal("0.0")
    elif value > maximum:
        new_value = Decimal("1.0")
    else:
        new_value = normalize_value(value=value, minimum=minimum, maximum=maximum)

    return new_value
