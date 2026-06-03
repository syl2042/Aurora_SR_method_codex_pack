#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


REQUIRED_LOT_FIELDS = [
    "lot_id",
    "title",
    "status",
    "objective",
    "acceptance_criteria",
    "verification_commands",
    "stop_conditions",
]

VALID_STATUSES = {
    "proposed",
    "planned",
    "validated",
    "in_progress",
    "done",
    "user_testing",
    "reopened",
    "blocked",
    "deferred",
    "superseded",
}


def parse_simple_yaml(path: Path) -> dict:
    try:
        import yaml  # type: ignore
    except Exception:
        yaml = None
    if yaml:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data or {}
    return parse_template_subset(path)


def parse_template_subset(path: Path) -> dict:
    """Very small YAML subset parser for this pack's sr_lots template.

    It is intentionally limited: it extracts top-level `lots` entries and common
    scalar/list fields so the validator can run without PyYAML.
    """
    lots = []
    current = None
    current_list_key = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped.startswith("- lot_id:"):
            if current:
                lots.append(current)
            current = {"lot_id": value_after_colon(stripped)}
            current_list_key = None
            continue
        if current is None:
            continue
        if raw.startswith("    ") and ":" in stripped and not stripped.startswith("- "):
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                current[key] = strip_quotes(value)
                current_list_key = None
            else:
                current[key] = []
                current_list_key = key
            continue
        if raw.startswith("      - ") and current_list_key:
            current.setdefault(current_list_key, []).append(strip_quotes(stripped[2:].strip()))
    if current:
        lots.append(current)
    return {"lots": lots}


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
        return value[1:-1]
    return value


def value_after_colon(value: str) -> str:
    return strip_quotes(value.split(":", 1)[1].strip())


def validate_lot(lot: dict, index: int) -> list[str]:
    errors = []
    prefix = f"lot[{index}]"
    for field in REQUIRED_LOT_FIELDS:
        if field not in lot or lot[field] in (None, "", []):
            errors.append(f"{prefix}: missing or empty {field}")
    status = lot.get("status")
    if status and status not in VALID_STATUSES:
        errors.append(f"{prefix}: invalid status {status!r}")
    for list_field in ("acceptance_criteria", "verification_commands", "stop_conditions"):
        if list_field in lot and not isinstance(lot[list_field], list):
            errors.append(f"{prefix}: {list_field} must be a list")
    if lot.get("allowed_paths") and not isinstance(lot.get("allowed_paths"), list):
        errors.append(f"{prefix}: allowed_paths must be a list when present")
    if lot.get("forbidden_paths") and not isinstance(lot.get("forbidden_paths"), list):
        errors.append(f"{prefix}: forbidden_paths must be a list when present")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="Path to SR_LOTS.yaml")
    args = ap.parse_args()
    path = Path(args.file)
    if not path.exists():
        print(f"missing file: {path}", file=sys.stderr)
        return 1
    data = parse_simple_yaml(path)
    lots = data.get("lots")
    if not isinstance(lots, list) or not lots:
        print("SR_LOTS must contain a non-empty `lots` list", file=sys.stderr)
        return 1
    errors = []
    seen = set()
    for i, lot in enumerate(lots):
        if not isinstance(lot, dict):
            errors.append(f"lot[{i}]: must be an object")
            continue
        lot_id = lot.get("lot_id")
        if lot_id in seen:
            errors.append(f"lot[{i}]: duplicate lot_id {lot_id!r}")
        seen.add(lot_id)
        errors.extend(validate_lot(lot, i))
    if errors:
        print("Lot contract errors:")
        for err in errors:
            print(f"- {err}")
        return 1
    print(f"OK: {len(lots)} lot(s) valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
