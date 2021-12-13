import re

from flask import request


def extract_tx_hash_from_req() -> str:
    """Extract tx hash from request url."""
    hash_match = re.findall(r"(0x)?([A-Fa-f0-9]{63})", request.url)

    return (
        f"{hash_match[0][0]}{hash_match[0][1]}"
        if hash_match and len(hash_match[0]) == 2
        else ""
    )
