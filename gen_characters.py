#!/usr/bin/env python3
"""
One-shot characters.md generator for foundation phase.
Reads seed.txt + voice.md + world.md + CRAFT.md, calls writer model.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from deepseek_client import chat_completion
from prompt_config_zh import CHARACTERS_PROMPT, CHARACTERS_SYSTEM

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

WRITER_MODEL = os.environ.get("AUTONOVEL_WRITER_MODEL", "claude-sonnet-4-6")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
API_BASE = os.environ.get("AUTONOVEL_API_BASE_URL", "https://api.anthropic.com")

def call_writer(prompt, max_tokens=16000):
   return chat_completion(
      model=WRITER_MODEL,
      prompt=prompt,
      system=CHARACTERS_SYSTEM,
      max_tokens=max_tokens,
      temperature=0.7,
      timeout=300,
   )

seed = (BASE_DIR / "seed.txt").read_text(encoding="utf-8")
world = (BASE_DIR / "world.md").read_text(encoding="utf-8")

# Voice Part 2 only
voice = (BASE_DIR / "voice.md").read_text(encoding="utf-8")
voice_lines = voice.split('\n')
part2_start = next(i for i, l in enumerate(voice_lines) if 'Part 2' in l)
voice_part2 = '\n'.join(voice_lines[part2_start:])

prompt = CHARACTERS_PROMPT.format(seed=seed, world=world, voice_part2=voice_part2)

print("Calling writer model...", file=sys.stderr)
result = call_writer(prompt)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
characters_path = BASE_DIR / "characters.md"
characters_path.write_text(result, encoding="utf-8")
print(f"Wrote {characters_path.name}", file=sys.stderr)
print(result)
