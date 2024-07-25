def is_positive_number(value):
    try:
        number_string = float(value)
        return number_string > 0
    except (ValueError, TypeError):
        return False
