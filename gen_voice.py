#!/usr/bin/env python3
"""Generate the novel-specific voice identity in voice.md Part 2."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from deepseek_client import chat_completion
from prompt_config_zh import VOICE_PROMPT, VOICE_SYSTEM

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

WRITER_MODEL = os.environ.get("AUTONOVEL_WRITER_MODEL", "claude-sonnet-4-6")
VOICE_MARKER = "## Part 2: Voice Identity (generated per novel)"


def call_writer(prompt: str, max_tokens: int = 5000) -> str:
    return chat_completion(
        model=WRITER_MODEL,
        prompt=prompt,
        system=VOICE_SYSTEM,
        max_tokens=max_tokens,
        temperature=0.6,
        timeout=300,
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> None:
    seed = read_text(BASE_DIR / "seed.txt")
    world = read_text(BASE_DIR / "world.md")
    characters = read_text(BASE_DIR / "characters.md")
    outline_path = BASE_DIR / "outline.md"
    outline_part1_path = BASE_DIR / "outline_part1.md"
    if outline_path.exists():
        outline = read_text(outline_path)
    elif outline_part1_path.exists():
        outline = read_text(outline_part1_path)
    else:
        outline = ""

    prompt = VOICE_PROMPT.format(
        seed=seed,
        world=world,
        characters=characters,
        outline=outline,
    )

    print("Calling writer model...", file=sys.stderr)
    part2 = call_writer(prompt)
    existing = read_text(BASE_DIR / "voice.md") if (BASE_DIR / "voice.md").exists() else ""
    if VOICE_MARKER in existing:
        prefix = existing.split(VOICE_MARKER, 1)[0].rstrip()
    else:
        prefix = existing.rstrip()
    final_text = prefix + "\n\n" + VOICE_MARKER + "\n\n" + part2.strip() + "\n"
    voice_path = BASE_DIR / "voice.md"
    voice_path.write_text(final_text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(f"Wrote {voice_path.name}", file=sys.stderr)
    print(part2)


if __name__ == "__main__":
    main()
