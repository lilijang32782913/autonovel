#!/usr/bin/env python3
"""
One-shot world.md generator for foundation phase.
Reads seed.txt + voice.md, calls the writer model, outputs world.md content.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from deepseek_client import chat_completion
from prompt_config_zh import WORLD_PROMPT, WORLD_SYSTEM

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

WRITER_MODEL = os.environ.get("AUTONOVEL_WRITER_MODEL", "claude-sonnet-4-6")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
API_BASE = os.environ.get("AUTONOVEL_API_BASE_URL", "https://api.anthropic.com")

def call_writer(prompt, max_tokens=16000):
  return chat_completion(
    model=WRITER_MODEL,
    prompt=prompt,
    system=WORLD_SYSTEM,
    max_tokens=max_tokens,
    temperature=0.7,
    timeout=300,
  )

seed = (BASE_DIR / "seed.txt").read_text(encoding="utf-8")
voice = (BASE_DIR / "voice.md").read_text(encoding="utf-8")
craft = (BASE_DIR / "CRAFT.md").read_text(encoding="utf-8")

# Extract voice Part 2 only (the novel-specific voice)
voice_lines = voice.split('\n')
part2_start = next(i for i, l in enumerate(voice_lines) if 'Part 2' in l)
voice_part2 = '\n'.join(voice_lines[part2_start:])

prompt = WORLD_PROMPT.format(seed=seed, voice_part2=voice_part2, craft=craft)

print("Calling writer model...", file=sys.stderr)
result = call_writer(prompt)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
world_path = BASE_DIR / "world.md"
world_path.write_text(result, encoding="utf-8")
print(f"Wrote {world_path.name}", file=sys.stderr)
print(result)
