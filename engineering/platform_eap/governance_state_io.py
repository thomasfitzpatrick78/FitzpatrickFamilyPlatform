"""Confined deterministic I/O for governance-state interfaces."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class GovernanceStateDataError(ValueError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def governance_state_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_governance_state(path_text: str, repository_root: Path) -> Any:
    candidate = Path(path_text)
    if candidate.is_absolute() or ".." in candidate.parts or "." in candidate.parts or "\\" in path_text:
        raise GovernanceStateDataError("governance state path must be a safe repository-relative path")
    unresolved = repository_root / candidate
    if unresolved.is_symlink():
        raise GovernanceStateDataError("governance state path must not be a symlink")
    root = repository_root.resolve()
    try:
        resolved = unresolved.resolve(strict=True)
    except OSError as exc:
        raise GovernanceStateDataError(f"governance state cannot be resolved: {exc}") from exc
    if resolved != root and root not in resolved.parents:
        raise GovernanceStateDataError("governance state path escapes the repository")
    if not resolved.is_file():
        raise GovernanceStateDataError("governance state path must be a regular file")
    try:
        return json.loads(resolved.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise GovernanceStateDataError(f"governance state cannot be read: {exc}") from exc
