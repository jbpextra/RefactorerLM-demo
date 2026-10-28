"""Format member records as ordered text manifests."""

from bundle_demo.naming import validate_member_name


def format_entry(name: str, payload: bytes) -> str:
    """Format one member after validating its name."""
    validate_member_name(name)
    checksum = sum(payload) % 256
    return f"{name}:{len(payload)}:{checksum:02x}\n"


def format_records(records: list[tuple[str, bytes]]) -> str:
    """Format records in order, rejecting repeated member names."""
    seen: set[str] = set()
    entries: list[str] = []
    for name, payload in records:
        if name in seen:
            raise ValueError("Duplicate member name")
        entries.append(format_entry(name, payload))
        seen.add(name)
    return "".join(entries)
