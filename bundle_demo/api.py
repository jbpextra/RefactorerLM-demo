"""Build ordered bundles and preview their text manifests."""

import bundle_demo.bundle as bundle
import bundle_demo.manifest as manifest


def build_bundle(records: list[tuple[str, bytes]]) -> tuple[str, tuple[bytes, ...]]:
    """Return a manifest and an immutable tuple of the original payload values.

    Records retain their input order. Names must be nonempty ASCII strings
    containing only letters, digits, dot, dash or underscore, and must be unique.
    Each manifest line contains the name, decimal payload length and two-digit
    lowercase hexadecimal sum of payload bytes modulo 256, separated by colons
    and followed by a newline. Empty input returns ("", ()).

    Invalid or duplicate names raise ValueError. The input is never mutated.
    """
    return bundle.assemble(records)


def preview_manifest(records: list[tuple[str, bytes]]) -> str:
    """Return the same ordered manifest that build_bundle would return.

    Names must be unique, nonempty ASCII strings using only letters, digits,
    dot, dash or underscore. Lines contain name, decimal byte length and the
    two-digit lowercase hexadecimal byte sum modulo 256, separated by colons
    and terminated by a newline. Empty input returns "". Invalid or duplicate
    names raise ValueError, and the input is never mutated.
    """
    return manifest.format_records(records)
