#!/usr/bin/env python3
"""Build the v2 daily story calendar from the authored 54-week season plan.

The v1 builder invented daily activity by rotating short lists. This version does
not generate plot. Every daily narrative beat must already exist in
story/season_plan_v2.json so that arcs can be reviewed before comic production.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STORY_DIR = ROOT / "story"
PLAN_PATH = STORY_DIR / "season_plan_v2.json"
APPROVAL_PATH = STORY_DIR / "approval_status.json"
CSV_PATH = STORY_DIR / "master_calendar_2025_2026.csv"
JSON_PATH = STORY_DIR / "master_calendar_2025_2026.json"
MARKDOWN_PATH = STORY_DIR / "master_calendar_2025_2026.md"
SOURCES_PATH = STORY_DIR / "master_calendar_sources.md"

EXPECTED_WEEKS = 54
EXPECTED_DAYS = 374

# These dates follow the shape of the source calendars but belong to the
# fictional McCall-Hart story calendar. They are not claims about a real school.
FIXED_EVENTS = {
    "2025-08-01": ["Quantitative Summer Bridge begins"],
    "2025-08-18": ["Residence halls open"],
    "2025-08-21": ["Opening Convocation"],
    "2025-08-25": ["Fall classes begin", "Fall add-drop begins"],
    "2025-08-29": ["Fall add-drop ends"],
    "2025-09-01": ["Labor Day - university closed"],
    "2025-11-14": ["Fall course-withdrawal deadline"],
    "2025-11-26": ["Thanksgiving recess begins"],
    "2025-11-27": ["Thanksgiving Day - university closed"],
    "2025-12-05": ["Fall classes end"],
    "2025-12-08": ["Fall final examinations begin"],
    "2025-12-12": ["Fall final examinations end", "Fall commencement"],
    "2025-12-13": ["Residence halls close"],
    "2026-01-01": ["New Year's Day - university closed"],
    "2026-01-04": ["Residence halls reopen"],
    "2026-01-07": ["Spring classes begin", "Spring add-drop begins"],
    "2026-01-13": ["Spring add-drop ends"],
    "2026-01-19": ["Martin Luther King Jr. Day - university closed"],
    "2026-03-16": ["Spring break begins"],
    "2026-03-20": ["Spring break ends"],
    "2026-04-03": ["Spring course-withdrawal deadline"],
    "2026-04-24": ["Last full spring class week ends"],
    "2026-04-27": ["Spring final examinations begin"],
    "2026-05-01": ["Spring final examinations end", "Spring classes end"],
    "2026-05-02": ["Spring commencement"],
    "2026-05-03": ["Residence halls close"],
    "2026-05-11": ["Summer A and full-summer classes begin"],
    "2026-05-25": ["Memorial Day - university closed"],
    "2026-06-19": ["Juneteenth - university closed", "Summer A ends"],
    "2026-06-29": ["Summer B begins"],
    "2026-07-04": ["Independence Day - university closed"],
    "2026-07-31": ["Summer final examinations begin"],
    "2026-08-01": ["Summer classes end"],
    "2026-08-07": ["Summer grades released"],
    "2026-08-09": ["Season one story window ends"],
}


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def parse_iso(value: str) -> date:
    return date.fromisoformat(value)


def validate_plan(plan: dict) -> None:
    weeks = plan.get("weeks")
    if not isinstance(weeks, list) or len(weeks) != EXPECTED_WEEKS:
        raise ValueError(f"Expected {EXPECTED_WEEKS} weeks, found {len(weeks or [])}")

    expected_numbers = list(range(1, EXPECTED_WEEKS + 1))
    actual_numbers = [week.get("week") for week in weeks]
    if actual_numbers != expected_numbers:
        raise ValueError("Week numbers must be sequential from 1 through 54")

    required = {
        "week",
        "title",
        "phase",
        "academic_focus",
        "event_anchors",
        "arc_turn",
        "daily_beats",
        "handoff",
    }
    all_beats: list[str] = []
    for week in weeks:
        missing = sorted(required - set(week))
        if missing:
            raise ValueError(f"Week {week['week']} is missing: {', '.join(missing)}")
        expected_beats = 3 if week["week"] == 54 else 7
        if len(week["daily_beats"]) != expected_beats:
            raise ValueError(
                f"Week {week['week']} requires {expected_beats} daily beats, "
                f"found {len(week['daily_beats'])}"
            )
        all_beats.extend(week["daily_beats"])

    if len(all_beats) != EXPECTED_DAYS:
        raise ValueError(f"Expected {EXPECTED_DAYS} daily beats, found {len(all_beats)}")
    if len(set(all_beats)) != len(all_beats):
        raise ValueError("Daily narrative beats must be unique")


def build_rows(plan: dict) -> list[dict[str, str | int]]:
    start = parse_iso(plan["date_range"]["start"])
    end = parse_iso(plan["date_range"]["end"])
    current = start
    rows: list[dict[str, str | int]] = []
    episode = 1

    for week in plan["weeks"]:
        week_start = current
        for day_index, beat in enumerate(week["daily_beats"], start=1):
            date_text = current.isoformat()
            rows.append(
                {
                    "date": date_text,
                    "day_of_week": current.strftime("%A"),
                    "episode_number": episode,
                    "week": week["week"],
                    "day_in_week": day_index,
                    "phase": week["phase"],
                    "week_title": week["title"],
                    "academic_focus": week["academic_focus"],
                    "fixed_events": " | ".join(FIXED_EVENTS.get(date_text, [])),
                    "weekly_event_anchors": " | ".join(week["event_anchors"]),
                    "arc_turn": week["arc_turn"],
                    "narrative_beat": beat,
                    "continuity_handoff": (
                        week["handoff"] if day_index == len(week["daily_beats"]) else ""
                    ),
                }
            )
            current += timedelta(days=1)
            episode += 1

        expected_week_end = week_start + timedelta(days=len(week["daily_beats"]) - 1)
        if rows[-1]["date"] != expected_week_end.isoformat():
            raise AssertionError(f"Date drift detected in week {week['week']}")

    if rows[-1]["date"] != end.isoformat() or current != end + timedelta(days=1):
        raise ValueError(
            f"Plan dates do not cover {start.isoformat()} through {end.isoformat()}"
        )
    return rows


def write_csv(rows: list[dict[str, str | int]]) -> None:
    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_json(rows: list[dict[str, str | int]]) -> None:
    JSON_PATH.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


def write_markdown(plan: dict, rows: list[dict[str, str | int]]) -> None:
    phase_counts = Counter(str(row["phase"]) for row in rows)
    lines = [
        "# McCall-Hart Story Master Calendar v2",
        "",
        "> Script status: awaiting approval. Comic production remains paused.",
        "",
        f"Date range: **{rows[0]['date']} to {rows[-1]['date']}**",
        "",
        f"Daily episodes: **{len(rows)}**",
        "",
        f"Weekly scripts: **{len(plan['weeks'])}**",
        "",
        "## Phase Counts",
        "",
    ]
    for phase, count in phase_counts.items():
        lines.append(f"- {phase}: {count} days")

    lines.extend(
        [
            "",
            "## Weekly Index",
            "",
            "| Week | Dates | Title | Academic focus | Arc turn | Event anchors |",
            "|---:|---|---|---|---|---|",
        ]
    )
    cursor = parse_iso(plan["date_range"]["start"])
    for week in plan["weeks"]:
        week_end = cursor + timedelta(days=len(week["daily_beats"]) - 1)
        events = "; ".join(week["event_anchors"])
        values = [
            str(week["week"]),
            f"{cursor.isoformat()} to {week_end.isoformat()}",
            week["title"],
            week["academic_focus"],
            week["arc_turn"],
            events,
        ]
        safe = [value.replace("|", "/") for value in values]
        lines.append("| " + " | ".join(safe) + " |")
        cursor = week_end + timedelta(days=1)

    lines.extend(
        [
            "",
            "## Generation Rule",
            "",
            "This calendar is compiled from authored daily beats. The build script may validate and format those beats, but it must not invent replacement plot by rotating generic activity lists.",
        ]
    )
    MARKDOWN_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sources() -> None:
    lines = [
        "# Master Calendar Sources and Fictionalization Rules",
        "",
        "## Authoritative v2 Sources",
        "",
        "- `story/setting_bible_v2.md`",
        "- `story/season_arc_v2.md`",
        "- `story/season_plan_v2.json`",
        "- `story/approval_status.json`",
        "",
        "## Structural Research Sources",
        "",
        "- Saved academic calendars under `research/academic-calendars/`",
        "- Saved Calculus I, II, and III syllabi under `research/course-syllabi/`",
        "- Saved athletics cadence in the v1 master calendar",
        "- Mathematics clubs, conferences, tutoring, and research references under `research/`",
        "",
        "## Boundary",
        "",
        "McCall-Hart University and every story event are fictional. Real source dates and schedules informed plausible rhythm only. Real institution names, opponents, faculty, venues, marks, and policies must not appear as McCall-Hart facts.",
        "",
        "## Calendar Assumptions",
        "",
        "- Story window: 2025-08-01 through 2026-08-09",
        "- Fall classes begin 2025-08-25",
        "- Spring classes begin 2026-01-07",
        "- Full-summer study begins 2026-05-11",
        "- Summer B begins 2026-06-29",
        "- Holiday and examination patterns are fictionalized composites",
    ]
    SOURCES_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    plan = load_json(PLAN_PATH)
    approval = load_json(APPROVAL_PATH)
    validate_plan(plan)
    if approval.get("setting") != plan.get("setting"):
        raise ValueError("Approval status and season plan identify different settings")

    rows = build_rows(plan)
    write_csv(rows)
    write_json(rows)
    write_markdown(plan, rows)
    write_sources()
    print(f"Built {len(rows)} authored daily episodes across {len(plan['weeks'])} weeks")
    print(f"Script approved: {bool(approval.get('script_approved'))}")
    print(f"Comic production allowed: {bool(approval.get('comic_production_allowed'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
