#!/usr/bin/env python3
"""Build a post-approval production plan for recurring McCall-Hart locations.

This helper never calls an image model. It records which background plates are
still needed and carries the project's approval state into the plan so a later
production tool cannot mistake planning for authorization.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
APPROVAL_PATH = REPO_ROOT / "story" / "approval_status.json"
VENUES_DIR = REPO_ROOT / "art" / "assets" / "venues"
PLAN_PATH = VENUES_DIR / "venue_background_generation_plan.json"

STYLE_SUFFIX = (
    "Editorial coming-of-age comic background plate, grounded Southern campus "
    "architecture, indigo, copper, and cream accents, expressive ink linework, "
    "warm natural light, readable composition, no people in the foreground, no "
    "logos, no legible text, no watermark."
)

VENUE_SPECS = [
    {
        "slug": "eliza_moss_hall",
        "display_name": "Eliza Moss Hall",
        "filename": "eliza_moss_hall_exterior.png",
        "scene": "Historic mathematics and science building with brick arches, tall windows, copper-toned doors, and mature live oaks.",
    },
    {
        "slug": "jubilee_library",
        "display_name": "Jubilee Library",
        "filename": "jubilee_library_exterior.png",
        "scene": "Grand but welcoming library with cream stone, broad steps, shaded study terraces, and an indigo banner without lettering.",
    },
    {
        "slug": "north_star_learning_commons",
        "display_name": "North Star Learning Commons",
        "filename": "north_star_learning_commons_interior.png",
        "scene": "Collaborative study hall with whiteboards, long tables, tutoring alcoves, copper fixtures, and late-afternoon window light.",
    },
    {
        "slug": "hart_student_union",
        "display_name": "Hart Student Union",
        "filename": "hart_student_union_exterior.png",
        "scene": "Lively student-union plaza with covered walkways, a low fountain, event-board shapes without readable text, and cypress trees.",
    },
    {
        "slug": "copper_cup_cafe",
        "display_name": "Copper Cup Cafe",
        "filename": "copper_cup_cafe_interior.png",
        "scene": "Warm campus cafe with copper pendant lights, indigo tile, small tables, a service counter, and room for dialogue scenes.",
    },
    {
        "slug": "founders_bell_cypress_walk",
        "display_name": "Founders' Bell and Cypress Walk",
        "filename": "founders_bell_cypress_walk.png",
        "scene": "Ceremonial bronze bell in a brick arch at the end of a long cypress-lined pedestrian walk during golden hour.",
    },
    {
        "slug": "henry_boyd_stadium",
        "display_name": "Henry Boyd Stadium",
        "filename": "henry_boyd_stadium_wide.png",
        "scene": "Wide college football stadium interior with a vivid field, indigo end zones without lettering, copper rail details, and game-night lights.",
    },
    {
        "slug": "ruth_ellis_fieldhouse",
        "display_name": "Ruth Ellis Fieldhouse",
        "filename": "ruth_ellis_fieldhouse_wide.png",
        "scene": "Intimate basketball arena with polished hardwood, indigo seating, copper trim, and clear open space for crowd overlays.",
    },
    {
        "slug": "meridian_diamond",
        "display_name": "Meridian Diamond",
        "filename": "meridian_diamond_wide.png",
        "scene": "College baseball park with a brick backstop, shaded dugouts, compact bleachers, and bright spring sunlight.",
    },
    {
        "slug": "magnolia_field",
        "display_name": "Magnolia Field",
        "filename": "magnolia_field_wide.png",
        "scene": "College softball field framed by magnolias, with cream dugouts, indigo fencing, and a welcoming community-game atmosphere.",
    },
    {
        "slug": "bellwether_media_house",
        "display_name": "Bellwether Media House",
        "filename": "bellwether_media_house_exterior.png",
        "scene": "Restored brick media building with glass studio additions, production cases near the entry, and a creative student-newsroom character.",
    },
    {
        "slug": "porter_center_for_enterprise",
        "display_name": "Porter Center for Enterprise",
        "filename": "porter_center_for_enterprise_exterior.png",
        "scene": "Modern entrepreneurship center with copper fins, shaded presentation terraces, and a polished competition-day atmosphere.",
    },
    {
        "slug": "delta_national_laboratory",
        "display_name": "Delta National Laboratory",
        "filename": "delta_national_laboratory_computing_gallery.png",
        "scene": "Fictional national-laboratory visitor computing gallery with glass walls, blue-white equipment light, secure doors, and no government seals.",
    },
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_approval() -> dict:
    return json.loads(APPROVAL_PATH.read_text(encoding="utf-8"))


def build_plan() -> dict:
    approval = load_approval()
    generation_allowed = bool(
        approval.get("script_approved")
        and approval.get("comic_production_allowed")
    )
    assets = []
    for spec in VENUE_SPECS:
        destination = VENUES_DIR / spec["filename"]
        assets.append(
            {
                "slug": spec["slug"],
                "display_name": spec["display_name"],
                "filename": spec["filename"],
                "path": str(destination.relative_to(REPO_ROOT)),
                "status": "complete" if destination.exists() else "planned",
                "prompt": f'{spec["scene"]} {STYLE_SUFFIX}',
            }
        )

    complete = [asset for asset in assets if asset["status"] == "complete"]
    planned = [asset for asset in assets if asset["status"] == "planned"]
    return {
        "updated_at": now_iso(),
        "setting": approval.get("setting"),
        "script_version": approval.get("script_version"),
        "script_approved": bool(approval.get("script_approved")),
        "comic_production_allowed": generation_allowed,
        "hold_reason": None if generation_allowed else approval.get("approval_note"),
        "complete_count": len(complete),
        "planned_count": len(planned),
        "assets": assets,
        "next_after_approval": planned[0] if generation_allowed and planned else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write a planning-only inventory for McCall-Hart venue backgrounds."
    )
    parser.add_argument("--json", action="store_true", help="Also print the plan")
    args = parser.parse_args()

    VENUES_DIR.mkdir(parents=True, exist_ok=True)
    plan = build_plan()
    PLAN_PATH.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")

    state = "OPEN" if plan["comic_production_allowed"] else "ON HOLD"
    print(
        f"Venue plan refreshed: {plan['complete_count']} complete, "
        f"{plan['planned_count']} planned. Production gate: {state}."
    )
    if args.json:
        print(json.dumps(plan, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
