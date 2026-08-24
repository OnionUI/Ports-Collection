#!/usr/bin/env python3
"""Generate the manifest for a Ports Collection release."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote


ARCHIVE_PREFIX = "-Onion-Ports-Collection_v"
GITHUB_ASSET_SAFE_RE = re.compile(r"[^A-Za-z0-9_-]+")
LAUNCHER_RE = re.compile(r"launch_([A-Za-z0-9_]+)\.sh")
ASSIGNMENT_RE = re.compile(
    r"^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)$"
)
LICENSE_NAMES = {
    "authors",
    "copying",
    "credits",
    "license",
    "licence",
    "copyright",
}


def github_asset_name(filename: str) -> str:
    """GitHub renames uploaded release assets: each run of chars outside [A-Za-z0-9_-] (including literal dots) collapses to a single '.'."""
    return GITHUB_ASSET_SAFE_RE.sub(".", filename)


def release_url(repository: str, tag: str, filename: str) -> str:
    return f"https://github.com/{repository}/releases/download/{tag}/{github_asset_name(filename)}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    data = path.read_bytes()
    if data.startswith((b"\xff\xfe", b"\xfe\xff", b"\xef\xbb\xbf")):
        for encoding in ("utf-16", "utf-8-sig"):
            try:
                return data.decode(encoding)
            except UnicodeDecodeError:
                pass
    if data.count(b"\x00") > max(1, len(data) // 20):
        try:
            return data.decode("utf-16")
        except UnicodeDecodeError:
            pass
    return data.decode("utf-8", errors="replace")


def shell_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_shortcut(path: Path, port_root: Path) -> dict[str, object]:
    values: dict[str, str] = {}
    launcher_type = None
    for line in read_text(path).splitlines():
        match = ASSIGNMENT_RE.match(line.strip())
        if match:
            values[match.group(1)] = shell_value(match.group(2))
        if launcher_type is None:
            launcher_match = LAUNCHER_RE.search(line)
            if launcher_match:
                launcher_type = launcher_match.group(1)

    fields = (
        "GameName",
        "Core",
        "GameDir",
        "GameExecutable",
        "GameDataFile",
        "RomDir",
        "RomFile",
        "Arguments",
        "KillAudioserver",
        "PerformanceMode",
    )
    metadata: dict[str, object] = {
        "path": path.relative_to(port_root).as_posix(),
        "menu_category": path.parent.name,
        "launcher_type": launcher_type,
        "configuration": {field: values[field] for field in fields if field in values},
        "environment": {
            key: value for key, value in values.items() if key not in fields
        },
    }
    return metadata


def relative_files(root: Path, predicate) -> list[str]:
    return sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and predicate(path)
    )


def port_record(port_root: Path, repo_root: Path, archive_dir: Path, repository: str, tag: str) -> dict[str, object]:
    port_name = port_root.name
    archive = archive_dir / f"{port_name}.7z"
    if not archive.is_file():
        raise SystemExit(f"Missing archive for port: {archive.name}")

    ports_root = port_root / "Roms" / "PORTS"
    images = sorted(
        path for path in (ports_root / "Imgs").glob("*.png") if path.is_file()
    )
    required = sorted(ports_root.glob("Games/*/_required_files.txt"))
    shortcut_paths = sorted(
        path
        for path in (ports_root / "Shortcuts").rglob("*")
        if path.is_file() and path.suffix in {".port", ".notfound"}
    )
    game_root = ports_root / "Games"
    runtime_libraries = relative_files(
        game_root,
        lambda path: "lib" in path.parts and path.is_file(),
    ) if game_root.is_dir() else []
    documentation = relative_files(
        port_root,
        lambda path: path.name.lower().split(".")[0] in LICENSE_NAMES
        or path.name.lower().startswith(("license", "licence", "copying", "authors", "credits", "copyright")),
    )
    manuals = relative_files(
        ports_root / "Manuals",
        lambda path: True,
    ) if (ports_root / "Manuals").is_dir() else []

    source_files = [path for path in port_root.rglob("*") if path.is_file()]
    required_documents = []
    for path in required:
        required_documents.append({
            "path": path.relative_to(port_root).as_posix(),
            "text": read_text(path),
        })

    record: dict[str, object] = {
        "id": port_name,
        "name": port_name,
        "category": "engine" if required else "complete",
        "requires_user_files": bool(required),
        "archive": {
            "filename": archive.name,
            "url": release_url(repository, tag, archive.name),
            "size_bytes": archive.stat().st_size,
            "sha256": sha256(archive),
        },
        "icons": [
            {
                "path": image.relative_to(repo_root).as_posix(),
                "url": f"https://github.com/{repository}/raw/{tag}/{quote(image.relative_to(repo_root).as_posix())}",
            }
            for image in images
        ],
        "shortcuts": [parse_shortcut(path, port_root) for path in shortcut_paths],
        "required_files": required_documents,
        "runtime_libraries": runtime_libraries,
        "documentation": documentation,
        "manuals": manuals,
        "source": {
            "file_count": len(source_files),
            "size_bytes": sum(path.stat().st_size for path in source_files),
        },
    }
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--output", type=Path, default=Path("ports-manifest.json"))
    args = parser.parse_args()

    repo_root = Path.cwd().resolve()
    archive_dir = repo_root
    ports = sorted(
        path
        for path in repo_root.iterdir()
        if path.is_dir()
        and not path.name.startswith(".")
        and (path / "Roms" / "PORTS").is_dir()
    )
    aggregate_name = f"{ARCHIVE_PREFIX}{args.version}.7z"
    aggregate = archive_dir / aggregate_name
    if not aggregate.is_file():
        raise SystemExit(f"Missing aggregate archive: {aggregate_name}")

    records = [
        port_record(path, repo_root, archive_dir, args.repository, args.tag)
        for path in ports
    ]
    expected_archives = {record["archive"]["filename"] for record in records}
    actual_archives = {
        path.name for path in archive_dir.glob("*.7z") if path.name != aggregate_name
    }
    if expected_archives != actual_archives:
        missing = sorted(expected_archives - actual_archives)
        unexpected = sorted(actual_archives - expected_archives)
        raise SystemExit(f"Archive mismatch; missing={missing}, unexpected={unexpected}")

    manifest = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": args.repository,
        "source_commit": args.commit,
        "release": {
            "tag": args.tag,
            "version": args.version,
            "archive": {
                "filename": aggregate.name,
                "url": release_url(args.repository, args.tag, aggregate.name),
                "size_bytes": aggregate.stat().st_size,
                "sha256": sha256(aggregate),
            },
        },
        "ports": records,
    }
    output = args.output if args.output.is_absolute() else repo_root / args.output
    output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    json.loads(output.read_text(encoding="utf-8"))
    print(f"Generated {output} for {len(records)} ports")


if __name__ == "__main__":
    main()
