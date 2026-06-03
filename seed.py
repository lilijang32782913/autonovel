#!/usr/bin/env python3
"""
seed.py -- Generate fantasy novel seed concepts.

Usage:
  uv run python seed.py              # Generate 10 concepts, pick one
  uv run python seed.py --count=5    # Generate 5 concepts
  uv run python seed.py --riff "magic costs memories"  # Riff on an idea
  uv run python seed.py --brief-file seed_brief.md --must-have "sentient ocean"
"""

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

from deepseek_client import chat_completion

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

from prompt_config_zh import (
    SEED_GENERATE_PROMPT,
    SEED_GUIDED_PROMPT,
    SEED_RIFF_PROMPT,
    SEED_SYSTEM,
)
WRITER_MODEL = os.environ.get("AUTONOVEL_WRITER_MODEL", "claude-sonnet-4-6-20250217")
HAS_API_KEY = bool(
  os.environ.get("DEEPSEEK_API_KEY", "")
  or os.environ.get("ANTHROPIC_API_KEY", "")
)


def call_writer(prompt, max_tokens=4000):
    return chat_completion(
        model=WRITER_MODEL,
        prompt=prompt,
        system=SEED_SYSTEM,
        max_tokens=max_tokens,
        temperature=1.0,
        timeout=120,
    )


GENERATE_PROMPT = SEED_GENERATE_PROMPT

RIFF_PROMPT = SEED_RIFF_PROMPT

GUIDED_GENERATE_PROMPT = SEED_GUIDED_PROMPT


def read_brief(path_str: str | None) -> str:
  if not path_str:
    return ""

  path = Path(path_str)
  if not path.is_absolute():
    path = BASE_DIR / path
  if not path.exists():
    print(f"WARN: brief file not found: {path}", file=sys.stderr)
    return ""
  return path.read_text(encoding="utf-8", errors="replace").strip()


def build_guidance(args) -> str:
  lines = []
  brief = read_brief(args.brief_file)

  if args.project:
    lines.append(f"PROJECT GOAL: {args.project}")

  if brief:
    lines.append("\nUSER BRIEF:\n" + brief)

  if args.protagonist:
    lines.append("PROTAGONIST REQUIREMENTS:")
    for item in args.protagonist:
      lines.append(f"- {item}")

  if args.setting:
    lines.append("SETTING REQUIREMENTS:")
    for item in args.setting:
      lines.append(f"- {item}")

  if args.magic_cost:
    lines.append("MAGIC/COST REQUIREMENTS:")
    for item in args.magic_cost:
      lines.append(f"- {item}")

  if args.tone:
    lines.append("TONE REQUIREMENTS:")
    for item in args.tone:
      lines.append(f"- {item}")

  if args.must_have:
    lines.append("MUST-HAVE ELEMENTS:")
    for item in args.must_have:
      lines.append(f"- {item}")

  if args.must_avoid:
    lines.append("MUST-AVOID ELEMENTS:")
    for item in args.must_avoid:
      lines.append(f"- {item}")

  return "\n".join(lines).strip()


def derive_seed_title(text: str) -> str:
  for line in text.splitlines():
    s = line.strip()
    if not s:
      continue
    # Example: "1. THE LAST SKETCH OF THE SEA-WRIGHT"
    m = re.match(r"^\d+\.\s+(.+)$", s)
    if m:
      return m.group(1).strip()
  return "seed"


def save_result_file(result: str) -> Path:
  title = derive_seed_title(result)
  digest = hashlib.sha1(result.encode("utf-8", errors="ignore")).hexdigest()[:8]
  stem = re.sub(r"[^a-zA-Z0-9_-]+", "-", title.lower()).strip("-")[:50] or "seed"
  out = BASE_DIR / f"seed_suggestions_{stem}_{digest}.md"
  out.write_text(result, encoding="utf-8")
  return out


def main():
    parser = argparse.ArgumentParser(description="Generate novel seed concepts")
    parser.add_argument("--count", type=int, default=10,
                        help="Number of concepts to generate (default: 10)")
    parser.add_argument("--riff", type=str, default=None,
                        help="Riff on an existing idea")
    parser.add_argument("--project", type=str, default=None,
                        help="High-level project goal for guided generation")
    parser.add_argument("--brief-file", type=str, default=None,
                        help="Path to text/markdown brief with detailed requirements")
    parser.add_argument("--must-have", action="append", default=[],
                        help="Must-have element (repeatable)")
    parser.add_argument("--must-avoid", action="append", default=[],
                        help="Must-avoid element (repeatable)")
    parser.add_argument("--tone", action="append", default=[],
                        help="Tone requirement (repeatable)")
    parser.add_argument("--setting", action="append", default=[],
                        help="Setting requirement (repeatable)")
    parser.add_argument("--protagonist", action="append", default=[],
                        help="Protagonist requirement (repeatable)")
    parser.add_argument("--magic-cost", action="append", default=[],
                        help="Magic/cost requirement (repeatable)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only print final prompt, do not call model")
    parser.add_argument("--save-output", action="store_true",
                        help="Save generated suggestions into a markdown file")
    args = parser.parse_args()

    guidance = build_guidance(args)

    if args.riff:
        print(f"Riffing on: {args.riff}\n")
        prompt = RIFF_PROMPT.format(idea=args.riff)
        if guidance:
            prompt += "\n\nADDITIONAL REQUIREMENTS:\n" + guidance
    elif guidance:
        print(f"Generating {args.count} guided seed concepts...\n")
        prompt = GUIDED_GENERATE_PROMPT.format(count=args.count, guidance=guidance)
    else:
        print(f"Generating {args.count} seed concepts...\n")
        prompt = GENERATE_PROMPT.format(count=args.count)

    if args.dry_run:
        print("[DRY RUN] Final prompt:\n")
        print(prompt)
        return

    if not HAS_API_KEY:
        print("ERROR: Set DEEPSEEK_API_KEY (or ANTHROPIC_API_KEY) in .env first")
        sys.exit(1)

    result = call_writer(prompt, max_tokens=8000)
    print(result)

    if args.save_output:
        out_path = save_result_file(result)
        print(f"\nSaved suggestions to: {out_path}")

    print("\n" + "=" * 60)
    print("To pick a seed, copy the concept you like into seed.txt:")
    print("  edit seed.txt")
    print("Or remix several concepts into your own seed.")
    print("Then proceed to Step 2 in WORKFLOW.md.")


if __name__ == "__main__":
    main()
