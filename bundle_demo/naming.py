"""Utilities for validating bundle member names."""

from string import ascii_letters, digits

_NAME_CHARACTERS = frozenset(ascii_letters + digits + ".-_")


def validate_member_name(name: str) -> None:
    """Reject an empty name or a character outside the member-name alphabet."""
    if not name or any(character not in _NAME_CHARACTERS for character in name):
        raise ValueError("Invalid member name")
