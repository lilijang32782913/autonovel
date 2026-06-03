#!/usr/bin/env python3
"""Archive current novel outputs and reset workspace for a new novel."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ARCHIVE_ROOT = BASE_DIR / "archives"

VOICE_MARKER = "## Part 2: Voice Identity (generated per novel)"

FILES_TO_ARCHIVE = [
    "seed.txt",
    "world.md",
    "characters.md",
    "outline.md",
    "outline_part1.md",
    "outline_output.md",
    "canon.md",
    "voice.md",
    "MYSTERY.md",
    "state.json",
    "results.tsv",
    "manuscript.md",
    "arc_summary.md",
    "reviews.md",
    "typeset/chapters_content.tex",
    "typeset/novel.pdf",
]

DIRS_TO_ARCHIVE = [
    "chapters",
    "briefs",
    "edit_logs",
    "eval_logs",
    "art",
    "audio",
]

RESET_TEXTS = {
    "seed.txt": "# Write your new seed concept here.\n",
    "world.md": "# WORLD BIBLE\n\nPopulate this file in foundation.\n",
    "characters.md": "# CHARACTER REGISTRY\n\nPopulate this file in foundation.\n",
    "outline.md": "# OUTLINE\n\nPopulate this file in foundation.\n",
    "canon.md": "# CANON\n\nPopulate this file in foundation.\n",
    "MYSTERY.md": "# MYSTERY\n\nAuthor-only central mystery notes.\n",
}

DEFAULT_STATE = {
    "phase": "foundation",
    "current_focus": "planning",
    "iteration": 0,
    "foundation_score": 0.0,
    "lore_score": 0.0,
    "chapters_drafted": 0,
    "chapters_total": 0,
    "novel_score": 0.0,
    "revision_cycle": 0,
    "debts": [],
}

MAX_ARCHIVE_SLUG = 56
WINDOWS_RESERVED_NAMES = {
    "con", "prn", "aux", "nul",
    "com1", "com2", "com3", "com4", "com5", "com6", "com7", "com8", "com9",
    "lpt1", "lpt2", "lpt3", "lpt4", "lpt5", "lpt6", "lpt7", "lpt8", "lpt9",
}


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9_-]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "novel"


def make_safe_archive_slug(text: str, max_len: int = MAX_ARCHIVE_SLUG) -> str:
    raw = (text or "novel").strip()
    base = slugify(raw)
    if base in WINDOWS_RESERVED_NAMES:
        base = f"novel-{base}"

    # Keep directory names short for Windows compatibility.
    short = base[:max_len].rstrip("-") or "novel"
    digest = hashlib.sha1(raw.encode("utf-8", errors="ignore")).hexdigest()[:8]
    return f"{short}-{digest}"


def infer_title() -> str:
    outline_path = BASE_DIR / "outline.md"
    if outline_path.exists():
        lines = outline_path.read_text(encoding="utf-8", errors="replace").splitlines()
        for line in lines[:20]:
            s = line.strip()
            if not s:
                continue
            if s.startswith("#"):
                return s.lstrip("# ").strip()[:120]
            return s[:120]

    seed_path = BASE_DIR / "seed.txt"
    if seed_path.exists():
        first = seed_path.read_text(encoding="utf-8", errors="replace").splitlines()
        if first:
            return first[0][:80]

    return "novel"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def copy_if_exists(rel_path: str, archive_dir: Path) -> bool:
    src = BASE_DIR / rel_path
    if not src.exists():
        return False

    dst = archive_dir / rel_path
    ensure_parent(dst)
    if src.is_dir():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
    return True


def archive_outputs(tag: str | None) -> Path:
    title = make_safe_archive_slug(tag if tag else infer_title())
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_dir = ARCHIVE_ROOT / f"{stamp}_{title}"
    archive_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    for rel in FILES_TO_ARCHIVE:
        if copy_if_exists(rel, archive_dir):
            copied.append(rel)

    for rel in DIRS_TO_ARCHIVE:
        if copy_if_exists(rel, archive_dir):
            copied.append(rel + "/")

    manifest = {
        "created_at": datetime.now().isoformat(),
        "source": str(BASE_DIR),
        "archive": str(archive_dir),
        "copied_items": copied,
    }
    (archive_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return archive_dir


def clear_directory_contents(rel_dir: str) -> None:
    path = BASE_DIR / rel_dir
    if not path.exists() or not path.is_dir():
        return
    for child in path.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def reset_voice_file() -> None:
    path = BASE_DIR / "voice.md"
    if not path.exists():
        return

    text = path.read_text(encoding="utf-8", errors="replace")
    if VOICE_MARKER in text:
        prefix = text.split(VOICE_MARKER, 1)[0].rstrip()
    else:
        prefix = text.rstrip()

    fresh = (
        f"{prefix}\n\n{VOICE_MARKER}\n\n"
        "(Pending generation for the new novel.)\n"
    )
    path.write_text(fresh, encoding="utf-8")


def reset_workspace() -> None:
    for rel, content in RESET_TEXTS.items():
        (BASE_DIR / rel).write_text(content, encoding="utf-8")

    state_path = BASE_DIR / "state.json"
    state_path.write_text(
        json.dumps(DEFAULT_STATE, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    reset_voice_file()

    for rel_dir in ["chapters", "briefs", "edit_logs", "eval_logs"]:
        clear_directory_contents(rel_dir)

    for rel_file in [
        "results.tsv",
        "manuscript.md",
        "arc_summary.md",
        "reviews.md",
        "outline_part1.md",
        "outline_output.md",
        "typeset/chapters_content.tex",
        "typeset/novel.pdf",
    ]:
        path = BASE_DIR / rel_file
        if path.exists():
            path.unlink()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Archive current novel outputs and reset workspace for a new book.",
    )
    p.add_argument("--tag", help="Optional tag used in archive folder name.")
    p.add_argument(
        "--archive-only",
        action="store_true",
        help="Archive outputs but do not reset files.",
    )
    p.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation prompt.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    print("This will archive current novel outputs.")
    if not args.archive_only:
        print("It will also clear chapter/review logs and reset planning files for a new book.")

    if not args.yes:
        answer = input("Continue? [y/N]: ").strip().lower()
        if answer not in {"y", "yes"}:
            print("Cancelled.")
            return

    archive_dir = archive_outputs(args.tag)
    print(f"Archived to: {archive_dir}")

    if not args.archive_only:
        reset_workspace()
        print("Workspace reset complete.")
        print("Next step: edit seed.txt, then run foundation.")


if __name__ == "__main__":
    main()
