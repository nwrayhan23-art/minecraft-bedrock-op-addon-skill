#!/usr/bin/env python3
"""Static validator for Minecraft Bedrock Add-On pack folders.

This is a lightweight structural checker, not Mojang's full content validator.
It uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
import zipfile
from pathlib import Path
from typing import Any


KNOWN_MODULE_TYPES = {"resources", "data", "world_template", "script", "client_data"}


def load_json(path: Path, errors: list[str]) -> Any | None:
    try:
        with path.open("r", encoding="utf-8-sig") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid JSON: {path}: {exc}")
        return None


def is_uuid(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError):
        return False


def discover_pack_dirs(project: Path) -> list[Path]:
    packs: list[Path] = []
    for manifest in project.rglob("manifest.json"):
        # Only treat manifests directly under a pack directory as pack manifests.
        if manifest.parent != project:
            packs.append(manifest.parent)
    return sorted(set(packs))


def validate(project: Path) -> tuple[list[str], list[str], list[Path]]:
    errors: list[str] = []
    warnings: list[str] = []
    pack_dirs = discover_pack_dirs(project)

    if not project.exists() or not project.is_dir():
        return [f"Project directory does not exist or is not a directory: {project}"], warnings, []
    if not pack_dirs:
        return [f"No pack manifest.json found beneath: {project}"], warnings, []

    # Check every JSON file, not only manifests.
    for json_path in project.rglob("*.json"):
        load_json(json_path, errors)

    manifests: list[tuple[Path, dict[str, Any]]] = []
    header_uuids: dict[str, Path] = {}
    all_uuids: dict[str, Path] = {}

    for pack_dir in pack_dirs:
        manifest_path = pack_dir / "manifest.json"
        data = load_json(manifest_path, errors)
        if not isinstance(data, dict):
            continue
        manifests.append((pack_dir, data))

        if data.get("format_version") not in (2, 3):
            errors.append(
                f"{manifest_path}: format_version should be 2 or 3; verify the current target-version schema."
            )

        header = data.get("header")
        if not isinstance(header, dict):
            errors.append(f"{manifest_path}: missing or invalid 'header' object.")
            header = {}

        header_uuid = header.get("uuid")
        if not is_uuid(header_uuid):
            errors.append(f"{manifest_path}: header.uuid is missing or is not a valid UUID.")
        else:
            normalized = str(uuid.UUID(header_uuid))
            if normalized in all_uuids:
                errors.append(f"Duplicate UUID {normalized}: {manifest_path} and {all_uuids[normalized]}")
            else:
                all_uuids[normalized] = manifest_path
                header_uuids[normalized] = manifest_path

        if not isinstance(header.get("name"), str) or not header.get("name", "").strip():
            errors.append(f"{manifest_path}: header.name must be a non-empty string.")
        if not isinstance(header.get("version"), (list, str)):
            errors.append(f"{manifest_path}: header.version is missing or has an unexpected type.")
        if "min_engine_version" not in header:
            errors.append(f"{manifest_path}: header.min_engine_version is required for Resource and Behavior Packs; set it for the target build.")

        modules = data.get("modules")
        if not isinstance(modules, list) or not modules:
            errors.append(f"{manifest_path}: 'modules' must be a non-empty array.")
            continue

        for index, module in enumerate(modules):
            label = f"{manifest_path}: modules[{index}]"
            if not isinstance(module, dict):
                errors.append(f"{label} must be an object.")
                continue

            module_type = module.get("type")
            if module_type not in KNOWN_MODULE_TYPES:
                warnings.append(f"{label}: unrecognized module type {module_type!r}; verify the current schema.")

            module_uuid = module.get("uuid")
            if not is_uuid(module_uuid):
                errors.append(f"{label}.uuid is missing or is not a valid UUID.")
            else:
                normalized = str(uuid.UUID(module_uuid))
                if normalized in all_uuids:
                    errors.append(f"Duplicate UUID {normalized}: {label} and {all_uuids[normalized]}")
                else:
                    all_uuids[normalized] = manifest_path

            if not isinstance(module.get("version"), (list, str)):
                errors.append(f"{label}.version is missing or has an unexpected type.")

            if module_type == "script":
                entry = module.get("entry")
                if not isinstance(entry, str) or not entry.strip():
                    errors.append(f"{label}: script module requires a non-empty entry path.")
                else:
                    entry_path = (pack_dir / entry).resolve()
                    try:
                        entry_path.relative_to(pack_dir.resolve())
                    except ValueError:
                        errors.append(f"{label}: script entry escapes the pack directory: {entry!r}")
                    else:
                        if not entry_path.is_file():
                            errors.append(f"{label}: script entry file does not exist: {entry_path}")

    # Check pack UUID dependencies after all header UUIDs are known.
    for pack_dir, data in manifests:
        manifest_path = pack_dir / "manifest.json"
        dependencies = data.get("dependencies", [])
        if dependencies is None:
            continue
        if not isinstance(dependencies, list):
            errors.append(f"{manifest_path}: dependencies must be an array when present.")
            continue
        for index, dependency in enumerate(dependencies):
            if not isinstance(dependency, dict):
                errors.append(f"{manifest_path}: dependencies[{index}] must be an object.")
                continue
            dependency_uuid = dependency.get("uuid")
            if dependency_uuid is not None:
                if not is_uuid(dependency_uuid):
                    errors.append(f"{manifest_path}: dependencies[{index}].uuid is not a valid UUID.")
                elif str(uuid.UUID(dependency_uuid)) not in header_uuids:
                    warnings.append(
                        f"{manifest_path}: dependency UUID {dependency_uuid} is not another pack header in this project; it may be an external dependency."
                    )
            elif not isinstance(dependency.get("module_name"), str):
                warnings.append(
                    f"{manifest_path}: dependencies[{index}] has neither a pack UUID nor a module_name; verify the current manifest schema."
                )

    if len(pack_dirs) == 1:
        warnings.append("Only one pack folder was found. A combined .mcaddon usually contains both a Behavior Pack and a Resource Pack when both are required.")

    return errors, warnings, pack_dirs


def create_archive(project: Path, pack_dirs: list[Path], output: Path) -> None:
    """Create a pack archive with each pack directory at the archive root."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for pack_dir in pack_dirs:
            for file_path in pack_dir.rglob("*"):
                if not file_path.is_file():
                    continue
                relative = file_path.relative_to(project)
                archive.write(file_path, relative.as_posix())


def main() -> int:
    parser = argparse.ArgumentParser(description="Run static checks on Minecraft Bedrock Add-On pack folders.")
    parser.add_argument("project", type=Path, help="Project folder containing one or more pack folders.")
    parser.add_argument("--package", action="store_true", help="Create a .mcaddon (two or more packs) or .mcpack (one pack) archive if static checks pass.")
    parser.add_argument("--output", type=Path, help="Optional output archive path. Defaults beside the project folder.")
    args = parser.parse_args()

    project = args.project.expanduser().resolve()
    errors, warnings, pack_dirs = validate(project)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"\nValidation failed: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1

    print(f"Static checks passed for {len(pack_dirs)} pack folder(s), with {len(warnings)} warning(s).")
    print("Reminder: this does not prove that Minecraft will load the pack or that every schema is valid.")

    if args.package:
        extension = ".mcaddon" if len(pack_dirs) >= 2 else ".mcpack"
        output = args.output.expanduser().resolve() if args.output else project.parent / f"{project.name}{extension}"
        create_archive(project, pack_dirs, output)
        print(f"Created archive: {output}")
        print("Inspect and test the archive in Minecraft before describing it as working.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
