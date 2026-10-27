"""Receipt entry point used by callers of the checkout service."""

import re

import orders
import pricing


def render_receipt(order_id, items, *, member=False):
    """Render the validated input order as a deterministic plain-text receipt."""
    if not isinstance(order_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,32}", order_id.strip()):
        raise ValueError("order_id must contain 1-32 ASCII letters, digits, '_' or '-'")
    if type(member) is not bool:
        raise TypeError("member must be bool")
    lines = orders.normalize_items(items)
    totals = pricing.quote(lines, member=member)
    receipt = [f"Order {order_id.strip()}"]
    receipt.extend(
        f"{quantity} x {sku} @ {unit_cents} = {quantity * unit_cents}"
        for sku, quantity, unit_cents in lines
    )
    receipt.extend([
        f"Subtotal: {totals['subtotal_cents']}",
        f"Discount: {totals['discount_cents']}",
        f"Shipping: {totals['shipping_cents']}",
        f"Total: {totals['total_cents']}",
        f"Items: {totals['item_count']}",
    ])
    return "\n".join(receipt)
