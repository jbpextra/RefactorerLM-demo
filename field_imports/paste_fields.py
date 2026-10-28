"""Clipboard adapter for escaped semicolon records.

``parse`` accepts literal clipboard text, including a leading BOM character;
binary input is not accepted. The shared record parser handles field syntax.
"""

from field_imports.record_fields import parse_record


def parse(text: str) -> tuple[str, ...]:
    """Parse literal clipboard text, preserving whitespace and BOM characters."""
    if not isinstance(text, str):
        raise TypeError("pasted record must be text")
    return parse_record(text)
