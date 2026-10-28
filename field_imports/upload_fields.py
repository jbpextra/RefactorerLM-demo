"""Escaped semicolon field records."""


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
    fields = scan_fields(text)
    validate_record(fields)
    return tuple(decode_escape(field) for field in fields)
