"""Validate member names and assemble payload bundles."""

import bundle_demo.manifest as manifest
from bundle_demo.utils import validate_member_name


def assemble(records: list[tuple[str, bytes]]) -> tuple[str, tuple[bytes, ...]]:
    """Assemble a manifest and an ordered payload tuple from member records."""
    text = manifest.format_records(records)
    payloads = tuple(payload for _, payload in records)
    return text, payloads
