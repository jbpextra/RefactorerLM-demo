"""Public field-record ingestion."""

import field_imports.upload_fields as upload_fields
import field_imports.paste_fields as paste_fields


def parse_upload(text: str | bytes) -> tuple[str, ...]:
    """Parse uploaded text or UTF-8 bytes into an immutable tuple.

    One leading BOM is discarded. Invalid UTF-8 raises UnicodeDecodeError.
    Backslash escapes only semicolon or backslash. Empty fields and whitespace
    are retained exactly. Empty text is one empty field. Invalid or dangling
    escapes raise ValueError. There are no side effects.
    """
    return upload_fields.parse(text)


def parse_paste(text: str) -> tuple[str, ...]:
    """Parse literal pasted text into an immutable tuple.

    Binary input raises TypeError. A leading BOM character is preserved.
    Backslash escapes only semicolon or backslash. Empty fields and whitespace
    are retained exactly. Empty text is one empty field. Invalid or dangling
    escapes raise ValueError. There are no side effects.
    """
    return paste_fields.parse(text)
