#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

try:
    from validate_lot_contract import parse_simple_yaml
except Exception:
    parse_simple_yaml = None


VALID_STATUSES = {
    "proposed",
    "planned",
    "validated",
    "in_progress",
    "done",
    "user_testing",
    "blocked",
    "superseded",
}
VALID_PRIORITIES = {"low", "medium", "high", "critical"}
VALID_E2E_MODES = {"per_lot", "grouped_at_pass_end", "not_required"}
REQUIRED_PASS_FIELDS = ["pass_id", "title", "status", "lots", "preflight", "e2e_strategy", "stop_on"]


def load_yaml(path: Path) -> dict:
    try:
        import yaml  # type: ignore
    except Exception:
        yaml = None
    if yaml:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    text = path.read_text(encoding="utf-8")
    if "\npasses:" in f"\n{text}":
        return parse_pass_subset(text)
    if parse_simple_yaml is None:
        raise ValueError("PyYAML unavailable and fallback parser unavailable")
    return parse_simple_yaml(path)


def parse_scalar(value: str):
    value = value.strip()
    if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
        value = value[1:-1]
    if value == "[]":
        return []
    if value == "null":
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    return value


def parse_pass_subset(text: str) -> dict:
    passes = []
    current = None
    current_list_key = None
    current_object_key = None
    current_object_list_key = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped.startswith("- pass_id:"):
            if current:
                passes.append(current)
            current = {"pass_id": parse_scalar(stripped.split(":", 1)[1].strip())}
            current_list_key = None
            current_object_key = None
            current_object_list_key = None
            continue
        if current is None:
            continue
        if raw.startswith("    ") and not raw.startswith("      ") and ":" in stripped and not stripped.startswith("- "):
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                current[key] = parse_scalar(value)
                current_list_key = None
                current_object_key = None
                current_object_list_key = None
            else:
                if key in {"sequencing", "preflight", "e2e_strategy", "gates"}:
                    current[key] = {}
                    current_object_key = key
                    current_object_list_key = None
                    current_list_key = None
                else:
                    current[key] = []
                    current_list_key = key
                    current_object_key = None
                    current_object_list_key = None
            continue
        if raw.startswith("      ") and current_object_key and ":" in stripped and not stripped.startswith("- "):
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            target = current.setdefault(current_object_key, {})
            if value:
                target[key] = parse_scalar(value)
                current_object_list_key = None
            else:
                target[key] = []
                current_object_list_key = key
            continue
        if raw.startswith("        - ") and current_object_key and current_object_list_key:
            target = current.setdefault(current_object_key, {})
            target.setdefault(current_object_list_key, []).append(parse_scalar(stripped[2:].strip()))
            continue
        if raw.startswith("      - ") and current_list_key:
            current.setdefault(current_list_key, []).append(parse_scalar(stripped[2:].strip()))
    if current:
        passes.append(current)
    return {"passes": passes}


def load_lots(path: Path) -> dict[str, dict]:
    data = load_yaml(path)
    lots = data.get("lots")
    if not isinstance(lots, list):
        raise ValueError(f"{path}: missing lots list")
    result = {}
    for lot in lots:
        if isinstance(lot, dict) and isinstance(lot.get("lot_id"), str):
            result[lot["lot_id"]] = lot
    return result


def as_list(value) -> list:
    return value if isinstance(value, list) else []


def validate_pass(item: dict, index: int, lots_by_id: dict[str, dict] | None) -> list[str]:
    errors = []
    prefix = f"pass[{index}]"
    for field in REQUIRED_PASS_FIELDS:
        if field not in item or item[field] in (None, "", []):
            errors.append(f"{prefix}: missing or empty {field}")
    status = item.get("status")
    if status and status not in VALID_STATUSES:
        errors.append(f"{prefix}: invalid status {status!r}")
    priority = item.get("priority")
    if priority is not None and priority not in VALID_PRIORITIES:
        errors.append(f"{prefix}: invalid priority {priority!r}")
    lots = item.get("lots")
    if lots is not None and not isinstance(lots, list):
        errors.append(f"{prefix}: lots must be a list")
        lots = []
    if isinstance(lots, list) and len(lots) != len(set(lots)):
        errors.append(f"{prefix}: lots must not contain duplicates")

    preflight = item.get("preflight")
    if preflight is not None:
        if not isinstance(preflight, dict):
            errors.append(f"{prefix}: preflight must be an object")
        else:
            for key in (
                "required_before_start",
                "secrets_required",
                "external_actions_required",
                "human_validation_required",
                "migrations_required",
                "open_questions",
            ):
                if key in preflight and not isinstance(preflight[key], list):
                    errors.append(f"{prefix}: preflight.{key} must be a list")

    sequencing = item.get("sequencing", {})
    if sequencing is not None and not isinstance(sequencing, dict):
        errors.append(f"{prefix}: sequencing must be an object")
        sequencing = {}
    overrides = as_list(sequencing.get("dependency_overrides")) if isinstance(sequencing, dict) else []
    if overrides and not all(isinstance(value, str) and value.strip() for value in overrides):
        errors.append(f"{prefix}: sequencing.dependency_overrides must contain non-empty strings")

    e2e = item.get("e2e_strategy")
    if e2e is not None:
        if not isinstance(e2e, dict):
            errors.append(f"{prefix}: e2e_strategy must be an object")
        else:
            mode = e2e.get("mode")
            if mode not in VALID_E2E_MODES:
                errors.append(f"{prefix}: e2e_strategy.mode must be one of {sorted(VALID_E2E_MODES)}")
            items = e2e.get("items")
            if items is not None and not isinstance(items, list):
                errors.append(f"{prefix}: e2e_strategy.items must be a list")
            if mode != "not_required" and not items:
                errors.append(f"{prefix}: e2e_strategy.items must not be empty unless mode is not_required")

    for list_field in ("shared_sources", "stop_on", "notes"):
        if list_field in item and not isinstance(item[list_field], list):
            errors.append(f"{prefix}: {list_field} must be a list")

    if lots_by_id is not None and isinstance(lots, list):
        lot_positions = {lot_id: pos for pos, lot_id in enumerate(lots)}
        for lot_id in lots:
            if lot_id not in lots_by_id:
                errors.append(f"{prefix}: lots references unknown lot_id {lot_id!r}")
                continue
            lot = lots_by_id[lot_id]
            lot_status = lot.get("status")
            if item.get("status") in {"validated", "in_progress"} and lot_status in {"blocked", "proposed", "superseded"}:
                errors.append(f"{prefix}: executable pass includes non-executable lot {lot_id!r} with status {lot_status!r}")
            for dependency in as_list(lot.get("depends_on")):
                if dependency in lot_positions and lot_positions[dependency] > lot_positions[lot_id]:
                    if not overrides:
                        errors.append(f"{prefix}: lot {lot_id!r} appears before dependency {dependency!r}")
                elif dependency not in lot_positions:
                    dependency_lot = lots_by_id.get(dependency)
                    if dependency_lot and dependency_lot.get("status") not in {"done", "user_testing"}:
                        errors.append(f"{prefix}: lot {lot_id!r} depends on unfinished lot {dependency!r} outside pass")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a SR_PASSES.yaml file.")
    parser.add_argument("--file", required=True, help="Path to SR_PASSES.yaml")
    parser.add_argument("--lots-file", help="Path to SR_LOTS.yaml for reference checks")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"missing file: {path}", file=sys.stderr)
        return 1
    try:
        data = load_yaml(path)
        lots_by_id = load_lots(Path(args.lots_file)) if args.lots_file else None
    except Exception as exc:
        print(f"Pass contract errors:\n- {exc}", file=sys.stderr)
        return 1

    passes = data.get("passes")
    if not isinstance(passes, list) or not passes:
        print("SR_PASSES must contain a non-empty `passes` list", file=sys.stderr)
        return 1

    errors = []
    seen = set()
    for index, item in enumerate(passes):
        if not isinstance(item, dict):
            errors.append(f"pass[{index}]: must be an object")
            continue
        pass_id = item.get("pass_id")
        if pass_id in seen:
            errors.append(f"pass[{index}]: duplicate pass_id {pass_id!r}")
        seen.add(pass_id)
        errors.extend(validate_pass(item, index, lots_by_id))

    if errors:
        print("Pass contract errors:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK: {len(passes)} pass(es) valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
