from __future__ import annotations

from pathlib import Path
from typing import Any

import orjson


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _write_jsonl_row(record: dict[str, Any], path: str | Path) -> None:
    output_path = Path(path)
    _ensure_parent(output_path)
    with output_path.open("a", encoding="utf-8") as handle:
        handle.write(orjson.dumps(record, option=orjson.OPT_SORT_KEYS).decode("utf-8"))
        handle.write("\n")


def write_attempt_record(record: dict[str, Any], path: str | Path) -> None:
    _write_jsonl_row(record, path)


def write_selected_run_view(record: dict[str, Any], path: str | Path) -> None:
    _write_jsonl_row(record, path)


def write_step_record(record: dict[str, Any], path: str | Path) -> None:
    _write_jsonl_row(record, path)


def write_message_record(record: dict[str, Any], path: str | Path) -> None:
    _write_jsonl_row(record, path)


def load_attempt_records(path: str | Path) -> list[dict[str, Any]]:
    return _load_jsonl(path)


def load_selected_run_views(path: str | Path) -> list[dict[str, Any]]:
    return _load_jsonl(path)


def load_message_records(path: str | Path) -> list[dict[str, Any]]:
    return _load_jsonl(path)


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    output_path = Path(path)
    _ensure_parent(output_path)
    output_path.write_bytes(
        orjson.dumps(payload, option=orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2)
    )


def _load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    input_path = Path(path)
    if not input_path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with input_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(orjson.loads(line))
    return rows
                
