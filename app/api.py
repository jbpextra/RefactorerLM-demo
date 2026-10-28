"""Public coordinate-label functions."""

import app.print_coordinates as print_coordinates


def screen_label(x: int, y: int, limit: int) -> str:
    """Return the bounded coordinates as canonical decimal text ``x,y``.

    Inputs are integers excluding bool. Each coordinate is clamped into
    [0, limit]. A negative limit raises ValueError.
    """
    bounded_x, bounded_y = print_coordinates.normalise(x, y, limit)
    return print_coordinates.render(bounded_x, bounded_y)


def print_label(x: int, y: int, limit: int) -> str:
    """Return the bounded coordinates as canonical decimal text ``x,y``.

    Inputs are integers excluding bool. Each coordinate is clamped into
    [0, limit]. A negative limit raises ValueError.
    """
    bounded_x, bounded_y = print_coordinates.normalise(x, y, limit)
    return print_coordinates.render(bounded_x, bounded_y)
