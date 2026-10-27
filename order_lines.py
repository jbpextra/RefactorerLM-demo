"""Shared validation for order-line items."""

import re


def normalize_items(items):
    """Return validated immutable lines without merging duplicate product codes."""
    try:
        iterator = iter(items)
    except TypeError:
        raise TypeError("items must be iterable") from None

    normalized = []
    for item in iterator:
        if not isinstance(item, (list, tuple)) or len(item) != 3:
            raise ValueError("each item must be a (sku, quantity, unit_cents) triple")
        sku, quantity, unit_cents = item
        if not isinstance(sku, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,16}", sku.strip()):
            raise ValueError("sku must contain 1-16 ASCII letters, digits, '_' or '-'")
        if type(quantity) is not int or not 1 <= quantity <= 99:
            raise ValueError("quantity must be an integer from 1 to 99")
        if type(unit_cents) is not int or not 0 <= unit_cents <= 1_000_000:
            raise ValueError("unit_cents must be an integer from 0 to 1000000")
        normalized.append((sku.strip(), quantity, unit_cents))
    return tuple(normalized)
