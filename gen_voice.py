#!/usr/bin/env python3
"""Generate the novel-specific voice identity in voice.md Part 2."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from deepseek_client import chat_completion

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

WRITER_MODEL = os.environ.get("AUTONOVEL_WRITER_MODEL", "claude-sonnet-4-6")
VOICE_MARKER = "## Part 2: Voice Identity (generated per novel)"


def call_writer(prompt: str, max_tokens: int = 5000) -> str:
    return chat_completion(
        model=WRITER_MODEL,
        prompt=prompt,
        system=(
            "You are a literary voice designer. You write a novel-specific voice "
            "identity that is concrete, usable, and distinct. Avoid generic praise. "
            "Focus on sentence rhythm, diction, metaphor fields, sensory preference, "
            "dialogue cadence, and anti-examples."
        ),
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

    prompt = f"""Design the novel-specific voice for this story and write the Part 2 content for voice.md.

NOVEL SEED:
{seed}

WORLD:
{world}

CHARACTERS:
{characters}

OUTLINE:
{outline}

Write a usable voice bible with these sections:
## Voice Thesis
## Sentence Rhythm
## Diction and Metaphor Fields
## Dialogue Habits
## Sensory Preferences
## Exemplar Passage 1
## Exemplar Passage 2
## Anti-Exemplar
## Calibration Notes

Requirements:
- Make it specific to this story's sound, not generic literary advice.
- Ground it in the story's world (sound, resonance, memory, salt, hands, weight, pressure).
- Include concrete do/don't rules a drafting model can follow.
- Include at least one short exemplar paragraph and one anti-exemplar paragraph.
- Keep it compact but useful, about 900-1400 words.
"""

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
