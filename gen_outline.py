#!/usr/bin/env python3
"""Generate outline.md from seed + world + characters + mystery + craft."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from deepseek_client import chat_completion
from prompt_config_zh import OUTLINE_PROMPT, OUTLINE_SYSTEM

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

WRITER_MODEL = os.environ.get("AUTONOVEL_WRITER_MODEL", "claude-sonnet-4-6")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
API_BASE = os.environ.get("AUTONOVEL_API_BASE_URL", "https://api.anthropic.com")

def call_writer(prompt, max_tokens=16000):
    return chat_completion(
        model=WRITER_MODEL,
        prompt=prompt,
        system=OUTLINE_SYSTEM,
        max_tokens=max_tokens,
        temperature=0.5,
        timeout=600,
    )

seed = (BASE_DIR / "seed.txt").read_text(encoding="utf-8")
world = (BASE_DIR / "world.md").read_text(encoding="utf-8")
characters = (BASE_DIR / "characters.md").read_text(encoding="utf-8")
mystery_path = BASE_DIR / "MYSTERY.md"
mystery = mystery_path.read_text(encoding="utf-8") if mystery_path.exists() else ""
craft = (BASE_DIR / "CRAFT.md").read_text(encoding="utf-8")

# Voice Part 2 only
voice = (BASE_DIR / "voice.md").read_text(encoding="utf-8")
voice_lines = voice.split('\n')
part2_start = next(i for i, l in enumerate(voice_lines) if 'Part 2' in l)
voice_part2 = '\n'.join(voice_lines[part2_start:])

prompt = OUTLINE_PROMPT.format(
        seed=seed,
        mystery=mystery,
        world=world,
        characters=characters,
        voice_part2=voice_part2,
        craft=craft,
)

print("Calling writer model...", file=sys.stderr)
result = call_writer(prompt)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
outline_part1 = BASE_DIR / "outline_part1.md"
outline_output = BASE_DIR / "outline_output.md"
outline_part1.write_text(result, encoding="utf-8")
outline_output.write_text(result, encoding="utf-8")
print(f"Wrote {outline_part1.name} and {outline_output.name}", file=sys.stderr)
print(result)
