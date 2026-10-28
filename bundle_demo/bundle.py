"""Validate member names and assemble payload bundles."""

from string import ascii_letters, digits

import bundle_demo.manifest as manifest

_NAME_CHARACTERS = frozenset(ascii_letters + digits + ".-_")


def validate_member_name(name: str) -> None:
    """Reject an empty name or a character outside the member-name alphabet."""
    if not name or any(character not in _NAME_CHARACTERS for character in name):
        raise ValueError("Invalid member name")


def assemble(records: list[tuple[str, bytes]]) -> tuple[str, tuple[bytes, ...]]:
    """Assemble a manifest and an ordered payload tuple from member records."""
    text = manifest.format_records(records)
    payloads = tuple(payload for _, payload in records)
    return text, payloads
