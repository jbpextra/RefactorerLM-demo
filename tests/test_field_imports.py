import pytest

from field_imports.api import parse_paste, parse_upload


@pytest.mark.parametrize("route", [parse_upload, parse_paste])
@pytest.mark.parametrize("text, expected", [
    ("first;second;third", ("first", "second", "third")),
    (r"a\;b;c", ("a;b", "c")),
    (r"path\\file;end", ("path\\file", "end")),
])
def test_records(route, text, expected):
    assert route(text) == expected


@pytest.mark.parametrize("route", [parse_upload, parse_paste])
@pytest.mark.parametrize("text", ["bad\\", r"bad\q"])
def test_invalid_escape(route, text):
    with pytest.raises(ValueError):
        route(text)
