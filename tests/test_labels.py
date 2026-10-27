"""Public coordinate-label checks."""

import pytest

from app.api import print_label, screen_label


@pytest.mark.parametrize("route", [screen_label, print_label])
@pytest.mark.parametrize(
    "x, y, limit, expected",
    [
        (2, 4, 9, "2,4"),
        (0, 3, 9, "0,3"),
        (5, 1, 5, "5,1"),
        (-2, 4, 9, "0,4"),
        (3, 12, 9, "3,9"),
    ],
)
def test_labels(route, x, y, limit, expected):
    assert route(x, y, limit) == expected


@pytest.mark.parametrize("route", [screen_label, print_label])
@pytest.mark.parametrize("limit", [-1, -8])
def test_negative_limit(route, limit):
    with pytest.raises(ValueError):
        route(2, 4, limit)


@pytest.mark.parametrize("route", [screen_label, print_label])
def test_keyword_arguments(route):
    assert route(x=2, y=4, limit=9) == "2,4"
