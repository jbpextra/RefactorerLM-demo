"""Ordinary checks for the public bundle API."""

import pytest

from bundle_demo.api import build_bundle, preview_manifest


def test_single_member_bundle():
    records = [("a.txt", b"AB")]
    assert build_bundle(records) == ("a.txt:2:83\n", (b"AB",))


def test_single_member_preview():
    assert preview_manifest([("a.txt", b"AB")]) == "a.txt:2:83\n"


def test_several_members():
    records = [("readme.md", b"Hi"), ("image-2.bin", b"\x10\x20")]
    text = "readme.md:2:b1\nimage-2.bin:2:30\n"
    assert build_bundle(records) == (text, (b"Hi", b"\x10\x20"))
    assert preview_manifest(records) == text


@pytest.mark.parametrize("operation", [build_bundle, preview_manifest])
@pytest.mark.parametrize("name", ["asset", "FILE_2.dat", ".", "-", "_"])
def test_member_name_alphabet(operation, name):
    result = operation([(name, b"X")])
    text = result[0] if operation is build_bundle else result
    assert text == f"{name}:1:58\n"


@pytest.mark.parametrize("operation", [build_bundle, preview_manifest])
@pytest.mark.parametrize("name", ["", "has space", "folder/file", "bad:name", "café"])
def test_invalid_names(operation, name):
    with pytest.raises(ValueError):
        operation([(name, b"X")])


@pytest.mark.parametrize("operation", [build_bundle, preview_manifest])
def test_duplicate_names(operation):
    with pytest.raises(ValueError):
        operation([("a", b"one"), ("b", b"two"), ("a", b"three")])
