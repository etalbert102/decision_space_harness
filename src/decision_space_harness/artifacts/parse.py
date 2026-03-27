from __future__ import annotations


def parse_prefixed_value(raw_output: str, prefix: str) -> str | None:
    for line in raw_output.splitlines():
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip() or None
    return None
