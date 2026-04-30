#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKGROUNDS_DIR = REPO_ROOT / "art" / "final" / "backgrounds"
LOG_DIR = REPO_ROOT / "logs"
LOG_PATH = LOG_DIR / "venue_background_generation.log"
PLAN_PATH = LOG_DIR / "venue_background_generation_plan.json"

VENUE_SPECS = [
    {
        "slug": "al_lawson_center",
        "filename": "al_lawson_center_wide_establishing.png",
        "prompt": "Modern animated comic style background plate of the Al Lawson Center at Florida A&M University, wide indoor basketball arena establishing view, polished hardwood court, modern collegiate seating bowl, bright indoor sports lighting, FAMU green and orange accents, energetic but clean atmosphere, readable environment, semi-cartoon linework, polished digital illustration, no text, no watermark, G-rated, social-media comic friendly.",
    },
    {
        "slug": "bragg_memorial_stadium",
        "filename": "bragg_memorial_stadium_wide_establishing.png",
        "prompt": "Modern animated comic style background plate of Ken Riley Field at Bragg Memorial Stadium at Florida A&M University, wide interior field establishing view from the lower stands, broad collegiate seating bowl, vivid green football field, FAMU green and orange atmosphere, warm Florida late afternoon light, HBCU game-day energy, clean semi-cartoon linework, readable composition, polished digital illustration, youth-friendly inspirational comic tone, no text, no watermark.",
    },
    {
        "slug": "coleman_library",
        "filename": "coleman_library_exterior_establishing.png",
        "prompt": "Modern animated comic style background plate of Samuel H. Coleman Memorial Library at Florida A&M University, exterior establishing view of the main library building, academic anchor campus architecture, welcoming front approach, a few students entering or exiting in the distance, warm Florida daylight, library seriousness with student life warmth, clean semi-cartoon linework, readable composition, polished digital illustration, youth-friendly inspirational comic tone, no text, no watermark.",
    },
    {
        "slug": "famu_eternal_flame",
        "filename": "famu_eternal_flame_establishing.png",
        "prompt": "Modern animated comic style background plate of the Florida A&M University Eternal Flame campus landmark, wide establishing shot with surrounding campus context, symbolic and inspirational atmosphere, warm academic pride, golden hour light with a visible eternal flame glow, clean semi-cartoon linework, readable social-media comic composition, polished digital illustration, grounded but iconic, no text, no watermark.",
    },
    {
        "slug": "jackson_davis_hall",
        "filename": "famu_jackson_davis_hall_establishing.png",
        "prompt": "Modern animated comic style background plate of Jackson Davis Hall at Florida A&M University, exterior campus establishing shot, warm Florida light, welcoming academic building atmosphere, green and orange identity accents, clean semi-cartoon linework, polished digital illustration, youth-friendly inspirational comic tone, no text, no watermark.",
    },
    {
        "slug": "jschool",
        "filename": "jschool_exterior_establishing.png",
        "prompt": "Modern animated comic style background plate of the School of Journalism & Graphic Communication at Florida A&M University, exterior establishing shot, modern communication-school energy, student media and creative campus atmosphere, welcoming walkway and entry composition, warm Florida daylight, clean semi-cartoon linework, polished digital illustration, readable social-media comic background, no text, no watermark.",
    },
    {
        "slug": "learning_commons",
        "filename": "famu_learning_commons_interior.png",
        "prompt": "Modern animated comic style background plate of a Florida A&M learning commons interior, student study atmosphere, collaborative tables, warm academic lighting, green and orange identity accents, clean semi-cartoon linework, readable environment, polished digital illustration, youth-friendly inspirational comic tone, no text, no watermark.",
    },
    {
        "slug": "moore_kittles_field",
        "filename": "moore_kittles_field_wide_establishing.png",
        "prompt": "Modern animated comic style background plate of Moore-Kittles Field at Florida A&M University, wide college baseball field establishing view, intimate bleachers, dugout and backstop feel, sunny Florida daylight, green field with orange and green identity touches, warm community atmosphere, clean semi-cartoon linework, readable composition, polished digital illustration, no text, no watermark.",
    },
    {
        "slug": "sbi",
        "filename": "sbi_exterior_establishing.png",
        "prompt": "Modern animated comic style background plate of the School of Business and Industry at Florida A&M University, exterior establishing shot, polished and ambitious campus architecture, professional entry walkway, warm Florida daylight, leadership and career-prep energy, clean semi-cartoon linework, readable composition, polished digital illustration, youth-friendly inspirational comic tone, no text, no watermark.",
    },
    {
        "slug": "top_cafe",
        "filename": "famu_top_cafe_interior.png",
        "prompt": "Modern animated comic style background plate of a Florida A&M campus cafe interior, student life warmth, dining and conversation setting, green and orange atmosphere, clean semi-cartoon linework, readable environment, polished digital illustration, no text, no watermark.",
    },
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def log(message: str) -> None:
    print(message, flush=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"{now_iso()} {message}\n")


def asset_exists(spec: dict[str, str]) -> bool:
    return (BACKGROUNDS_DIR / spec["filename"]).exists()


def build_plan() -> dict:
    completed = []
    remaining = []
    for spec in VENUE_SPECS:
        entry = {
            "slug": spec["slug"],
            "filename": spec["filename"],
            "path": str(BACKGROUNDS_DIR / spec["filename"]),
            "prompt": spec["prompt"],
        }
        if asset_exists(spec):
            completed.append(entry)
        else:
            remaining.append(entry)

    return {
        "updated_at": now_iso(),
        "completed_count": len(completed),
        "remaining_count": len(remaining),
        "completed": completed,
        "remaining": remaining,
        "next": remaining[0] if remaining else None,
    }


def save_plan(plan: dict) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    PLAN_PATH.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a local plan/log for remaining FAMU venue backgrounds.")
    parser.add_argument("--json", action="store_true", help="Print the plan JSON to stdout")
    args = parser.parse_args()

    BACKGROUNDS_DIR.mkdir(parents=True, exist_ok=True)
    plan = build_plan()
    save_plan(plan)

    log(f"Venue asset plan refreshed. Completed: {plan['completed_count']} | Remaining: {plan['remaining_count']}")
    if plan["next"]:
        log(f"Next missing venue asset: {plan['next']['slug']} -> {plan['next']['filename']}")
    else:
        log("No remaining venue assets.")

    if args.json:
        print(json.dumps(plan, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
