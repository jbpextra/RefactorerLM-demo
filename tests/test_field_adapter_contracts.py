"""The upload and clipboard adapters are independent public integrations."""

from pathlib import Path
import subprocess
import sys

import pytest

import field_imports.paste_fields as paste_fields
import field_imports.upload_fields as upload_fields
from field_imports.api import parse_paste, parse_upload


@pytest.mark.parametrize("route", [upload_fields.parse, parse_upload])
@pytest.mark.parametrize(
    "payload, expected",
    [
        ("\ufefffirst;second", ("first", "second")),
        (b"\xef\xbb\xbffirst;second", ("first", "second")),
        ("\ufeff\ufefffirst;second", ("\ufefffirst", "second")),
        (b"\xef\xbb\xbf\xef\xbb\xbffirst;second", ("\ufefffirst", "second")),
        ("caf\u00e9;\u8336".encode("utf-8"), ("caf\u00e9", "\u8336")),
        (b"a\\;b;c", ("a;b", "c")),
        (b"", ("",)),
        ("\ufeff", ("",)),
    ],
)
def test_upload_decoding_and_bom_handling(route, payload, expected):
    assert route(payload) == expected


@pytest.mark.parametrize("route", [paste_fields.parse, parse_paste])
def test_pasted_bom_is_literal_text(route):
    assert route("\ufefffirst; second ") == ("\ufefffirst", " second ")


@pytest.mark.parametrize("route", [paste_fields.parse, parse_paste])
@pytest.mark.parametrize("payload", [b"first;second", b"\xff", bytearray(b"text")])
def test_paste_rejects_binary_input(route, payload):
    with pytest.raises(TypeError, match="pasted record must be text"):
        route(payload)


@pytest.mark.parametrize("route", [upload_fields.parse, parse_upload])
def test_upload_rejects_invalid_utf8(route):
    with pytest.raises(UnicodeDecodeError):
        route(b"\xff;second")


@pytest.mark.parametrize("route", [upload_fields.parse, parse_upload])
@pytest.mark.parametrize("payload", [None, 42, bytearray(b"text")])
def test_upload_rejects_unsupported_input_types(route, payload):
    with pytest.raises(TypeError, match="uploaded record must be text or UTF-8 bytes"):
        route(payload)


@pytest.mark.parametrize(
    "module_name, unavailable_peer, payload, expected",
    [
        (
            "field_imports.paste_fields",
            "field_imports.upload_fields",
            "\ufefffirst;second",
            ("\ufefffirst", "second"),
        ),
        (
            "field_imports.upload_fields",
            "field_imports.paste_fields",
            b"\xef\xbb\xbffirst;second",
            ("first", "second"),
        ),
    ],
)
def test_adapter_works_when_its_peer_is_unavailable(
    module_name, unavailable_peer, payload, expected
):
    # A fresh interpreter prevents earlier imports from hiding a dependency.
    script = f"""
import importlib
import importlib.abc
import sys

class UnavailablePeer(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == {unavailable_peer!r} or fullname.startswith({unavailable_peer!r} + '.'):
            raise ModuleNotFoundError('The other adapter is not installed')
        return None

sys.meta_path.insert(0, UnavailablePeer())
adapter = importlib.import_module({module_name!r})
assert adapter.parse({payload!r}) == {expected!r}
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
