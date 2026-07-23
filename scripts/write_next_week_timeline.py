#!/usr/bin/env python3
"""Write approval-ready weekly scripts from the authored v2 season plan."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STORY_DIR = ROOT / "story"
PLAN_PATH = STORY_DIR / "season_plan_v2.json"
MASTER_PATH = STORY_DIR / "master_calendar_2025_2026.json"
APPROVAL_PATH = STORY_DIR / "approval_status.json"
OUT_DIR = STORY_DIR / "timeline-weeks"
STATE_PATH = STORY_DIR / "timeline_writer_state.json"


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def rows_by_week(rows: list[dict]) -> dict[int, list[dict]]:
    grouped: dict[int, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[int(row["week"])].append(row)
    return dict(grouped)


def validate(plan: dict, rows: list[dict]) -> None:
    if len(plan.get("weeks", [])) != 54:
        raise ValueError("The v2 season plan must contain 54 weeks")
    if len(rows) != 374:
        raise ValueError("The v2 master calendar must contain 374 daily episodes")
    planned_beats = [beat for week in plan["weeks"] for beat in week["daily_beats"]]
    row_beats = [row["narrative_beat"] for row in rows]
    if planned_beats != row_beats:
        raise ValueError(
            "The master calendar is stale. Run scripts/build_master_calendar.py first."
        )


def build_week_markdown(
    week: dict,
    rows: list[dict],
    approval: dict,
) -> str:
    start = rows[0]["date"]
    end = rows[-1]["date"]
    approval_text = "approved" if approval.get("script_approved") else "awaiting approval"
    lines = [
        f"# Week {week['week']:02d}: {week['title']}",
        "",
        f"Dates: **{start} to {end}**",
        "",
        f"Script status: **{approval_text}**",
        "",
        "## Weekly Story Turn",
        "",
        week["arc_turn"],
        "",
        "## Academic Spine",
        "",
        week["academic_focus"],
        "",
        "## Event Anchors",
        "",
    ]
    lines.extend(f"- {event}" for event in week["event_anchors"])
    lines.extend(["", "## Daily Episode Plan", ""])

    for row in rows:
        lines.extend(
            [
                f"### Episode {int(row['episode_number']):03d}: {row['day_of_week']}, {row['date']}",
                "",
            ]
        )
        if row.get("fixed_events"):
            lines.extend([f"Calendar: {row['fixed_events']}", ""])
        lines.extend([row["narrative_beat"], ""])

    lines.extend(
        [
            "## Continuity Handoff",
            "",
            week["handoff"],
            "",
            "## Production Gate",
            "",
            "This is a story-approval script. Do not create new storyboards, prompts, panels, or comic pages from it until `story/approval_status.json` records explicit script approval.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_week(week: dict, rows: list[dict], approval: dict) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUT_DIR / f"{week['week']}.md"
    destination.write_text(
        build_week_markdown(week, rows, approval),
        encoding="utf-8",
    )
    return destination


def completed_entry(week: dict, rows: list[dict], destination: Path) -> dict:
    return {
        "week_index": week["week"] - 1,
        "week_number": week["week"],
        "start": rows[0]["date"],
        "end": rows[-1]["date"],
        "file": str(destination.relative_to(ROOT)),
        "script_version": "v2",
    }


def save_state(completed: list[dict], next_week_index: int) -> None:
    state = {
        "script_version": "v2",
        "next_week_index": next_week_index,
        "total_weeks": 54,
        "completed": completed,
    }
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="Rewrite all 54 weekly scripts")
    group.add_argument("--week", type=int, help="Rewrite one numbered week")
    args = parser.parse_args()

    plan = load_json(PLAN_PATH)
    master_rows = load_json(MASTER_PATH)
    approval = load_json(APPROVAL_PATH)
    validate(plan, master_rows)
    grouped = rows_by_week(master_rows)

    if args.all:
        completed = []
        for week in plan["weeks"]:
            destination = write_week(week, grouped[week["week"]], approval)
            completed.append(completed_entry(week, grouped[week["week"]], destination))
        save_state(completed, 54)
        print("WROTE: all 54 v2 weekly scripts")
        return 0

    if args.week is not None:
        if not 1 <= args.week <= 54:
            raise ValueError("--week must be between 1 and 54")
        week = plan["weeks"][args.week - 1]
        destination = write_week(week, grouped[args.week], approval)
        print(f"WROTE: {destination.relative_to(ROOT)}")
        return 0

    existing_state = load_json(STATE_PATH) if STATE_PATH.exists() else {}
    next_index = int(existing_state.get("next_week_index", 0))
    if existing_state.get("script_version") != "v2":
        next_index = 0
    if next_index >= 54:
        print("NOOP: all v2 weekly scripts are complete")
        return 0

    week = plan["weeks"][next_index]
    destination = write_week(week, grouped[week["week"]], approval)
    completed = existing_state.get("completed", []) if next_index else []
    completed.append(completed_entry(week, grouped[week["week"]], destination))
    save_state(completed, next_index + 1)
    print(f"WROTE: {destination.relative_to(ROOT)}")
    print(f"PROGRESS: {next_index + 1}/54 weeks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
