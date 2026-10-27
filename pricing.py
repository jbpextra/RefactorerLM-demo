"""Integer-cent member discounts and shipping quotes."""

from order_lines import normalize_items


def quote(items, *, member=False):
    """Calculate a fresh quote after validating the supplied order lines."""
    if type(member) is not bool:
        raise TypeError("member must be bool")
    lines = normalize_items(items)
    subtotal_cents = sum(quantity * unit_cents for _, quantity, unit_cents in lines)
    discount_cents = subtotal_cents // 10 if member else 0
    net_cents = subtotal_cents - discount_cents
    shipping_cents = 0 if not lines or net_cents >= 5_000 else 499
    return {
        "subtotal_cents": subtotal_cents,
        "discount_cents": discount_cents,
        "shipping_cents": shipping_cents,
        "total_cents": net_cents + shipping_cents,
        "item_count": sum(quantity for _, quantity, _ in lines),
    }
