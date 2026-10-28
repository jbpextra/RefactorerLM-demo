"""Public field-record ingestion."""

import field_imports.upload_fields as upload_fields
import field_imports.paste_fields as paste_fields


def parse_upload(text: str) -> tuple[str, ...]:
    """Parse a semicolon-separated record into an immutable tuple.

    Backslash escapes only semicolon or backslash. Empty fields and whitespace
    are retained exactly. Empty text is one empty field. Invalid or dangling
    escapes raise ValueError. There are no side effects.
    """
    return upload_fields.parse(text)


def parse_paste(text: str) -> tuple[str, ...]:
    """Parse a semicolon-separated record into an immutable tuple.

    Backslash escapes only semicolon or backslash. Empty fields and whitespace
    are retained exactly. Empty text is one empty field. Invalid or dangling
    escapes raise ValueError. There are no side effects.
    """
    return paste_fields.parse(text)
