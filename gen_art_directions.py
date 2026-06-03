#!/usr/bin/env python3
"""
Generate diverse art direction concepts from a novel's visual style.
Called by gen_art.py curate to produce genuinely different variants.
"""
import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv

from deepseek_client import chat_completion
from prompt_config_zh import (
  ART_DIRECTIONS_COVER_PROMPT,
  ART_DIRECTIONS_MAP_PROMPT,
  ART_DIRECTIONS_ORNAMENT_PROMPT,
  ART_DIRECTIONS_SCENE_BREAK_PROMPT,
)

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env", override=True)

WRITER_MODEL = os.environ.get("AUTONOVEL_WRITER_MODEL", "claude-sonnet-4-6")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_BASE = os.environ.get("AUTONOVEL_API_BASE_URL", "https://api.anthropic.com")


def call_claude(prompt, max_tokens=3000):
  return chat_completion(
    model=WRITER_MODEL,
    prompt=prompt,
    max_tokens=max_tokens,
    temperature=0.9,
    timeout=120,
  )


def generate_directions(art_type, style, n=6, world_excerpt=""):
    """Generate N fundamentally different art direction prompts."""

    if art_type == "cover":
        task = ART_DIRECTIONS_COVER_PROMPT.format(
            n=n,
            art_style=style.get("art_style", ""),
            color_palette=style.get("color_palette", ""),
            mood=style.get("mood", ""),
            reference_artists=style.get("reference_artists", ""),
            cover_concept=style.get("cover_concept", ""),
        )

    elif art_type == "ornament":
        task = ART_DIRECTIONS_ORNAMENT_PROMPT.format(
            n=n,
            art_style=style.get("art_style", ""),
            ornament_concept=style.get("ornament_concept", ""),
        )

    elif art_type == "map":
        task = ART_DIRECTIONS_MAP_PROMPT.format(
            n=n,
            art_style=style.get("art_style", ""),
            map_concept=style.get("map_concept", ""),
            world_excerpt=world_excerpt[:2000],
        )

    elif art_type == "scene-break":
      task = ART_DIRECTIONS_SCENE_BREAK_PROMPT.format(
        n=n,
        art_style=style.get("art_style", ""),
        scene_break_concept=style.get("scene_break_concept", ""),
      )

    else:
        raise ValueError(f"Unknown art type: {art_type}")

    result = call_claude(task)
    text = result.strip()
    if text.startswith("```"):
        text = re.sub(r'^```\w*\n?', '', text)
        text = re.sub(r'\n?```$', '', text)

    return json.loads(text)


if __name__ == "__main__":
    import sys
    style_file = BASE_DIR / "art" / "visual_style.json"
    if not style_file.exists():
        print("Run gen_art.py style first")
        sys.exit(1)
    style = json.loads(style_file.read_text())
    
    art_type = sys.argv[1] if len(sys.argv) > 1 else "cover"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    
    world = ""
    if (BASE_DIR / "world.md").exists():
        world = (BASE_DIR / "world.md").read_text()[:3000]
    
    directions = generate_directions(art_type, style, n, world)
    for i, d in enumerate(directions, 1):
        print(f"\n--- Direction {i}: {d['direction'].upper()} ---")
        print(f"  Concept: {d['concept']}")
        print(f"  Medium:  {d['medium']}")
        print(f"  Prompt:  {d['prompt'][:150]}...")
