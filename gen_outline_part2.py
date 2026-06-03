#!/usr/bin/env python3
"""Generate remaining chapters + foreshadowing ledger."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from deepseek_client import chat_completion
from prompt_config_zh import OUTLINE_CONT_PROMPT, OUTLINE_CONT_SYSTEM

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

WRITER_MODEL = os.environ.get("AUTONOVEL_WRITER_MODEL", "claude-sonnet-4-6")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
API_BASE = os.environ.get("AUTONOVEL_API_BASE_URL", "https://api.anthropic.com")

def call_writer(prompt, max_tokens=16000):
    return chat_completion(
        model=WRITER_MODEL,
        prompt=prompt,
        system=OUTLINE_CONT_SYSTEM,
        max_tokens=max_tokens,
        temperature=0.5,
        timeout=600,
    )

part1_path = BASE_DIR / "outline_output.md"
part1 = part1_path.read_text(encoding="utf-8") if part1_path.exists() else ""
mystery = (BASE_DIR / "MYSTERY.md").read_text(encoding="utf-8")

prompt = OUTLINE_CONT_PROMPT.format(part1=part1, mystery=mystery)

print("Calling writer model...", file=sys.stderr)
result = call_writer(prompt)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
outline_path = BASE_DIR / "outline.md"
combined = part1.rstrip() + "\n\n" + result.lstrip() if part1.strip() else result
outline_path.write_text(combined, encoding="utf-8")
print(f"Wrote {outline_path.name}", file=sys.stderr)
print(result)
