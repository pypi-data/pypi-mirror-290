import json
from pathlib import Path
from typing import Any, Dict


def lower_key_from_nested_dict(obj) -> Dict[str, Any]:  # noqa: ANN001
    """Lower case all keys from nested dicts."""
    if isinstance(obj, dict):
        return {k.lower(): lower_key_from_nested_dict(v) for k, v in obj.items()}
    elif isinstance(obj, (list, set, tuple)):  # noqa: RET505
        t = type(obj)
        return t(lower_key_from_nested_dict(o) for o in obj)
    else:
        return obj


def read_json_file(file: Path, *, lower_keys: bool = False) -> Dict[str, Any]:
    for encoding in ("utf-8", "iso-8859-1"):
        try:
            with file.open(encoding=encoding) as fp:
                return lower_key_from_nested_dict(json.load(fp)) if lower_keys else json.load(fp)  # type: ignore[no-any-return]
        except UnicodeDecodeError:
            pass
    raise RuntimeError(f"Failed to decode file {file}")
