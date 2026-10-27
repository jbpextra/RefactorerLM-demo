"""Order-line validation and order summaries for the small checkout service."""

import pricing
from order_lines import normalize_items


def subtotal(items):
    """Return the undiscounted value in integer cents."""
    return sum(quantity * unit_cents for _, quantity, unit_cents in normalize_items(items))


def summarize(items, *, member=False):
    """Attach a price quote to a snapshot of the validated order lines."""
    if type(member) is not bool:
        raise TypeError("member must be bool")
    lines = normalize_items(items)
    return {"items": lines, "totals": pricing.quote(lines, member=member)}
