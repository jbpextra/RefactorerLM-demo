"""Public coordinate-label functions."""

import app.screen_coordinates as screen_coordinates


def screen_label(x: int, y: int, limit: int) -> str:
    """Return the bounded coordinates as canonical decimal text ``x,y``.

    Inputs are integers excluding bool. Each coordinate is clamped into
    [0, limit]. A negative limit raises ValueError.
    """
    bounded_x, bounded_y = screen_coordinates.normalise(x, y, limit)
    return screen_coordinates.render(bounded_x, bounded_y)


def print_label(x: int, y: int, limit: int) -> str:
    """Return the bounded coordinates as canonical decimal text ``x,y``.

    Inputs are integers excluding bool. Each coordinate is clamped into
    [0, limit]. A negative limit raises ValueError.
    """
    bounded_x, bounded_y = screen_coordinates.normalise(x, y, limit)
    return screen_coordinates.render(bounded_x, bounded_y)
