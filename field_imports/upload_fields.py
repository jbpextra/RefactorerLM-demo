"""UTF-8 upload adapter for escaped semicolon records.

``parse`` accepts text or UTF-8 bytes and discards one leading BOM. The shared
record parser handles field syntax.
"""

from field_imports.record_fields import parse_record


def parse(text: str | bytes) -> tuple[str, ...]:
    """Decode uploaded content and parse its fields without a leading BOM."""
    if isinstance(text, bytes):
        text = text.decode("utf-8-sig")
    elif isinstance(text, str):
        text = text.removeprefix("\ufeff")
    else:
        raise TypeError("uploaded record must be text or UTF-8 bytes")
    return parse_record(text)
