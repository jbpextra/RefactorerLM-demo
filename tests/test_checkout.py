import pytest

import checkout
import orders
import pricing


def test_normalized_snapshot_and_subtotal():
    items = [[" pen ", 2, 125], ["pen", 1, 200]]
    assert orders.normalize_items(items) == (("pen", 2, 125), ("pen", 1, 200))
    assert orders.subtotal(items) == 450
    assert items == [[" pen ", 2, 125], ["pen", 1, 200]]


def test_member_quote_and_summary():
    items = [("pen", 2, 125)]
    totals = {
        "subtotal_cents": 250,
        "discount_cents": 25,
        "shipping_cents": 499,
        "total_cents": 724,
        "item_count": 2,
    }
    assert pricing.quote(items, member=True) == totals
    assert orders.summarize(items, member=True) == {"items": tuple(items), "totals": totals}


@pytest.mark.parametrize("value,shipping", [(4999, 499), (5000, 0)])
def test_shipping_boundary(value, shipping):
    assert pricing.quote([("parcel", 1, value)])["shipping_cents"] == shipping


def test_empty_order():
    assert orders.normalize_items([]) == ()
    assert orders.subtotal([]) == 0
    assert all(value == 0 for value in pricing.quote([], member=True).values())


def test_receipt_for_external_caller():
    assert checkout.render_receipt(" R-1 ", [("pen", 2, 125)], member=True) == (
        "Order R-1\n2 x pen @ 125 = 250\nSubtotal: 250\nDiscount: 25\n"
        "Shipping: 499\nTotal: 724\nItems: 2"
    )


def test_generator_input():
    items = (("pen", 1, cents) for cents in [125, 200])
    assert orders.summarize(items)["totals"]["subtotal_cents"] == 325


@pytest.mark.parametrize("items", [[("pen", 0, 1)], [("pen", 1, -1)], [("", 1, 1)], [("pen", 1)]])
def test_invalid_items(items):
    with pytest.raises(ValueError):
        pricing.quote(items)


def test_member_must_be_boolean():
    with pytest.raises(TypeError, match="^member must be bool$"):
        orders.summarize([], member=1)
