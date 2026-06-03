#!/usr/bin/env python3
"""
Generate canon.md by extracting all hard facts from world.md + characters.md.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from deepseek_client import chat_completion
from prompt_config_zh import CANON_PROMPT, CANON_SYSTEM

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

WRITER_MODEL = os.environ.get("AUTONOVEL_WRITER_MODEL", "claude-sonnet-4-6")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
API_BASE = os.environ.get("AUTONOVEL_API_BASE_URL", "https://api.anthropic.com")

def call_writer(prompt, max_tokens=16000):
    return chat_completion(
        model=WRITER_MODEL,
        prompt=prompt,
        system=CANON_SYSTEM,
        max_tokens=max_tokens,
        temperature=0.2,
        timeout=300,
    )

world = (BASE_DIR / "world.md").read_text(encoding="utf-8")
characters = (BASE_DIR / "characters.md").read_text(encoding="utf-8")
seed = (BASE_DIR / "seed.txt").read_text(encoding="utf-8")

prompt = CANON_PROMPT.format(seed=seed, world=world, characters=characters)

print("Calling writer model...", file=sys.stderr)
result = call_writer(prompt)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
canon_path = BASE_DIR / "canon.md"
canon_path.write_text(result, encoding="utf-8")
print(f"Wrote {canon_path.name}", file=sys.stderr)
print(result)
