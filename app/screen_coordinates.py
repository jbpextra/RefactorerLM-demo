"""Bound and format coordinates."""

from decimal import Decimal


def normalise(x: int, y: int, limit: int) -> tuple[int, int]:
    """Return independently bounded coordinates for a nonnegative limit."""
    if limit < 0:
        raise ValueError("limit must be nonnegative")
    return clamp(x, limit), clamp(y, limit)


def clamp(value: int, limit: int) -> int:
    """Return a value in the closed interval from zero to limit."""
    if value < 0:
        return 0
    if value > limit:
        return limit
    return value


def render(x: int, y: int) -> str:
    """Return canonical decimal coordinates with a comma and no spaces."""
    return f"{Decimal(x):f},{Decimal(y):f}"
