"""Clipboard adapter for escaped semicolon records.

``parse`` is the supported public entry point. Clipboard text, including a
leading BOM character, is literal; binary input is not accepted. This adapter
must work independently of the upload adapter. The other functions are parsing
implementation details whose duplication is intentional in this demo.
"""


def scan_fields(text: str) -> tuple[str, ...]:
    fields = []
    current = []
    index = 0
    while index < len(text):
        character = text[index]
        if character == "\\":
            current.append(character)
            index += 1
            if index < len(text):
                current.append(text[index])
        elif character == ";":
            fields.append("".join(current))
            current = []
        else:
            current.append(character)
        index += 1
    fields.append("".join(current))
    return tuple(fields)


def validate_record(fields: tuple[str, ...]) -> None:
    for field in fields:
        index = 0
        while index < len(field):
            if field[index] == "\\":
                if index + 1 == len(field) or field[index + 1] not in (";", "\\"):
                    raise ValueError("invalid escape")
                index += 2
            else:
                index += 1


def decode_escape(field: str) -> str:
    decoded = []
    index = 0
    while index < len(field):
        if field[index] == "\\":
            index += 1
        decoded.append(field[index])
        index += 1
    return "".join(decoded)


def parse(text: str) -> tuple[str, ...]:
    """Parse literal clipboard text, preserving whitespace and BOM characters."""
    if not isinstance(text, str):
        raise TypeError("pasted record must be text")
    fields = scan_fields(text)
    validate_record(fields)
    return tuple(decode_escape(field) for field in fields)
