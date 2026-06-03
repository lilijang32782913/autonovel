#!/usr/bin/env python3
"""
Revision chapter generator. Rewrites a chapter from a specific revision brief.
Usage: python gen_revision.py <chapter_num> <brief_file>
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from deepseek_client import chat_completion
from prompt_config_zh import REVISION_PROMPT, REVISION_SYSTEM

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

WRITER_MODEL = os.environ.get("AUTONOVEL_WRITER_MODEL", "claude-sonnet-4-6")
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
API_BASE = os.environ.get("AUTONOVEL_API_BASE_URL", "https://api.anthropic.com")

def call_writer(prompt, max_tokens=16000):
    return chat_completion(
        model=WRITER_MODEL,
        prompt=prompt,
        system=REVISION_SYSTEM,
        max_tokens=max_tokens,
        temperature=0.8,
        timeout=600,
    )

def main():
    ch_num = int(sys.argv[1])
    brief_file = sys.argv[2]
    
    voice = (BASE_DIR / "voice.md").read_text()
    characters = (BASE_DIR / "characters.md").read_text()
    world = (BASE_DIR / "world.md").read_text()
    brief = Path(brief_file).read_text()
    
    # Load adjacent chapters for continuity
    prev_path = BASE_DIR / "chapters" / f"ch_{ch_num - 1:02d}.md"
    next_path = BASE_DIR / "chapters" / f"ch_{ch_num + 1:02d}.md"
    prev_tail = prev_path.read_text()[-2000:] if prev_path.exists() else "(first chapter)"
    next_head = next_path.read_text()[:1500] if next_path.exists() else "(last chapter)"
    
    # Load old version if exists
    old_path = BASE_DIR / "chapters" / f"ch_{ch_num:02d}.md"
    old_text = old_path.read_text() if old_path.exists() else "(no existing draft)"
    
    prompt = REVISION_PROMPT.format(
        ch_num=ch_num,
        brief=brief,
        voice=voice,
        characters=characters,
        world=world,
        prev_tail=prev_tail,
        next_head=next_head,
        old_text=old_text,
    )

    print(f"Rewriting Chapter {ch_num}...", file=sys.stderr)
    result = call_writer(prompt)
    
    out_path = BASE_DIR / "chapters" / f"ch_{ch_num:02d}.md"
    out_path.write_text(result)
    print(f"Saved to {out_path}", file=sys.stderr)
    print(f"Word count: {len(result.split())}", file=sys.stderr)

if __name__ == "__main__":
    main()
