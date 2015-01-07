from functools import partial


def int_or_default(value, default=None):
    try:
        return abs(int(value))
    except (ValueError, TypeError):
        return default


int_or_zero = partial(int_or_default, default=0)
