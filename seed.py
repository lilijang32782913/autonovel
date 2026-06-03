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

WRITER_MODEL = os.environ.get("AUTONOVEL_WRITER_MODEL", "claude-sonnet-4-6-20250217")
HAS_API_KEY = bool(
  os.environ.get("DEEPSEEK_API_KEY", "")
  or os.environ.get("ANTHROPIC_API_KEY", "")
)


def call_writer(prompt, max_tokens=4000):
    return chat_completion(
        model=WRITER_MODEL,
        prompt=prompt,
        system=(
            "You are a fantasy novelist with deep knowledge of the genre's "
            "best works -- Tolkien, Le Guin, Rothfuss, Wolfe, Jemisin, Peake, "
            "Susanna Clarke, Andrew Peterson, Sofia Samatar. You generate "
            "novel concepts that are SPECIFIC, SURPRISING, and STRUCTURALLY "
            "SOUND. You never propose generic medieval Europe + elves. Each "
            "concept should make a reader think 'I've never seen THAT before.'"
        ),
        max_tokens=max_tokens,
        temperature=1.0,
        timeout=120,
    )


GENERATE_PROMPT = """Generate {count} fantasy novel seed concepts. Each should be
a complete premise you could build a novel from.

For EACH concept, provide:

NUMBER. TITLE (a working title, evocative, not generic)
HOOK: One sentence that would make someone pick up the book. Specific
  and surprising, not "In a world where..."
WORLD: What makes this world different? Not just "there's magic" but
  what specific, unusual thing defines this place? Be concrete --
  salt flats, inverted towers, cities that migrate, a sea that
  remembers, whatever. Make it SENSORY.
MAGIC/COST: What is the core speculative element and what does it
  COST? Per Sanderson's Second Law, limitations > powers. The cost
  should create interesting dilemmas.
TENSION: What's the central conflict? It must be both PERSONAL (one
  character's specific problem) and COSMIC (affects the world).
  These two must be in tension with each other.
THEME: What question does this story explore? Not a message -- a
  genuine question with no easy answer.
WHY IT'S NOT GENERIC: One sentence on what makes this different from
  standard fantasy fare.

Aim for DIVERSITY across the {count} concepts:
  - At least one with a non-human-centric world
  - At least one that's more literary/quiet than epic
  - At least one with an unusual narrative structure idea
  - At least one set outside the typical European-inspired setting
  - Mix of tones: dark, warm, weird, melancholy, whimsical

DO NOT generate:
  - Chosen one prophecies (unless subverted in an interesting way)
  - Dark lord / ultimate evil as the main antagonist
  - Medieval Europe + elves/dwarves/orcs
  - "Academy" or "school for magic" settings
  - Love triangles as the central plot
"""

RIFF_PROMPT = """I have a seed idea for a fantasy novel:

"{idea}"

Generate 5 variations on this concept. Keep what's interesting about
the core idea but push it in different directions. For each variation:

NUMBER. TITLE
HOOK: One sentence.
HOW IT DIFFERS: What did you change from the original seed and why?
WORLD: Concrete, sensory world details.
MAGIC/COST: The speculative element and its cost.
TENSION: Personal + cosmic conflict.
THEME: The question it explores.

Make the variations genuinely different from each other -- don't just
tweak surface details. Change the protagonist, the setting, the tone,
the structure, the thematic focus.
"""

GUIDED_GENERATE_PROMPT = """Generate {count} fantasy novel seed concepts based on the following user brief and constraints.

USER BRIEF AND CONSTRAINTS:
{guidance}

For EACH concept, provide:

NUMBER. TITLE (a working title, evocative, not generic)
HOOK: One sentence that would make someone pick up the book. Specific
  and surprising, not "In a world where..."
WORLD: What makes this world different? Be concrete and sensory.
MAGIC/COST: The core speculative element and what it COSTS.
TENSION: Personal + cosmic conflict in direct tension.
THEME: The question this story explores.
WHY IT'S NOT GENERIC: One sentence.

RULES:
- Follow MUST-HAVE constraints strictly.
- Avoid MUST-AVOID constraints strictly.
- If a constraint conflicts with fantasy conventions, prefer the constraint.
- Keep concepts diverse in structure, tone, and conflict framing.
"""


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
