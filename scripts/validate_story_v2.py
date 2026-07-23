#!/usr/bin/env python3
"""Validate v2 story coverage, continuity, fictionalization, and approval gates."""

from __future__ import annotations

import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STORY = ROOT / "story"
PLAN_PATH = STORY / "season_plan_v2.json"
APPROVAL_PATH = STORY / "approval_status.json"
MASTER_PATH = STORY / "master_calendar_2025_2026.json"
WEEK_DIR = STORY / "timeline-weeks"
COMBINED_PATH = STORY / "script-v2-output" / "the-formula-of-becoming-script-v2.md"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def contains_all(text: str, terms: list[str]) -> list[str]:
    lowered = text.lower()
    return [term for term in terms if term.lower() not in lowered]


def active_production_files() -> list[Path]:
    files: list[Path] = []
    roots = [STORY / "timeline-weeks", ROOT / "art", ROOT / "skills"]
    for source_root in roots:
        if not source_root.exists():
            continue
        for path in source_root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".py"}:
                continue
            if "archive" in path.parts:
                continue
            files.append(path)
    files.extend(
        [
            STORY / "season_plan_v2.json",
            STORY / "season_arc_v2.md",
            STORY / "character_bible_v2.md",
            STORY / "master_calendar_2025_2026.md",
            STORY / "master_calendar_sources.md",
        ]
    )
    return sorted(set(files))


def main() -> int:
    errors: list[str] = []
    plan = load_json(PLAN_PATH)
    approval = load_json(APPROVAL_PATH)
    master = load_json(MASTER_PATH)
    weeks = plan.get("weeks", [])

    require(errors, plan.get("setting") == "McCall-Hart University", "Wrong active setting")
    require(errors, len(weeks) == 54, "Season plan must contain 54 weeks")
    require(errors, [week.get("week") for week in weeks] == list(range(1, 55)), "Week numbers are not sequential")
    require(errors, len(master) == 374, "Master calendar must contain 374 daily episodes")
    require(errors, master[0].get("date") == "2025-08-01", "Master calendar start date is wrong")
    require(errors, master[-1].get("date") == "2026-08-09", "Master calendar end date is wrong")

    beats = [beat for week in weeks for beat in week.get("daily_beats", [])]
    require(errors, len(beats) == 374, "Season plan must contain 374 daily beats")
    require(errors, len(set(beats)) == 374, "Daily beats must be unique")
    require(errors, len({week.get("title") for week in weeks}) == 54, "Weekly titles must be unique")
    require(errors, len({week.get("academic_focus") for week in weeks}) == 54, "Weekly academic focuses must be unique")
    require(errors, [row.get("narrative_beat") for row in master] == beats, "Master calendar does not match season plan")

    cursor = date.fromisoformat(plan["date_range"]["start"])
    for week in weeks:
        expected_count = 3 if week["week"] == 54 else 7
        require(errors, len(week["daily_beats"]) == expected_count, f"Week {week['week']} has the wrong daily-beat count")
        week_rows = [row for row in master if int(row["week"]) == week["week"]]
        require(errors, len(week_rows) == expected_count, f"Week {week['week']} has the wrong master-calendar row count")
        if week_rows:
            require(errors, week_rows[0]["date"] == cursor.isoformat(), f"Week {week['week']} starts on the wrong date")
        cursor += timedelta(days=expected_count)

    plan_text = json.dumps(plan, ensure_ascii=False)
    required_story_terms = [
        "Julian",
        "Simone",
        "breakup",
        "Gulf storm",
        "flood",
        "Heron Analytics",
        "fails to advance",
        "does not receive the national fellowship",
        "Delta National Laboratory",
        "football",
        "basketball",
        "softball",
        "baseball",
        "track",
        "band",
        "Calculus I",
        "Calculus II",
        "Calculus III",
        "exclusive relationship",
        "second year",
    ]
    missing_story_terms = contains_all(plan_text, required_story_terms)
    require(errors, not missing_story_terms, "Missing required story coverage: " + ", ".join(missing_story_terms))

    academic_terms = [
        "limits",
        "continuity",
        "derivative",
        "Fundamental Theorem of Calculus",
        "integration by parts",
        "improper integrals",
        "series",
        "Taylor",
        "polar coordinates",
        "vectors",
        "partial derivatives",
        "Lagrange multipliers",
        "double integrals",
        "triple integrals",
        "Green's Theorem",
        "Stokes' Theorem",
        "Divergence Theorem",
    ]
    missing_academic_terms = contains_all(plan_text, academic_terms)
    require(errors, not missing_academic_terms, "Missing syllabus coverage: " + ", ".join(missing_academic_terms))

    require(errors, not approval.get("script_approved"), "Script approval must remain false until the user explicitly approves")
    require(errors, not approval.get("comic_production_allowed"), "Comic production must remain blocked")
    require(errors, approval.get("setting_is_fictional") is True, "Approval file must identify a fictional setting")

    weekly_files = sorted(WEEK_DIR.glob("*.md"), key=lambda path: int(path.stem))
    require(errors, len(weekly_files) == 54, "Expected 54 active weekly script files")
    if weekly_files:
        require(errors, [int(path.stem) for path in weekly_files] == list(range(1, 55)), "Weekly script filenames are incomplete")
    for path in weekly_files:
        text = path.read_text(encoding="utf-8")
        require(errors, "Script status: **awaiting approval**" in text, f"Missing approval status in {path.relative_to(ROOT)}")
        require(errors, "## Production Gate" in text, f"Missing production gate in {path.relative_to(ROOT)}")

    require(errors, COMBINED_PATH.exists(), "Combined v2 approval manuscript is missing")
    if COMBINED_PATH.exists():
        combined = COMBINED_PATH.read_text(encoding="utf-8")
        headings = re.findall(r"^# Week \d{2}:", combined, flags=re.MULTILINE)
        require(errors, len(headings) == 54, "Combined manuscript must contain 54 weekly headings")
        require(errors, "Script status: **AWAITING APPROVAL**" in combined, "Combined manuscript has the wrong approval status")

    forbidden = re.compile(
        r"\b(?:FAMU|Florida A&M|Rattlers?|Bragg Memorial|Al Lawson|Jackson Davis|Coleman Library|Eternal Flame|Moore[-–]Kittles|Tallahassee)\b",
        flags=re.IGNORECASE,
    )
    for path in active_production_files():
        text = path.read_text(encoding="utf-8")
        matches = sorted(set(match.group(0) for match in forbidden.finditer(text)))
        if matches:
            errors.append(
                f"Real-institution reference in active production file {path.relative_to(ROOT)}: "
                + ", ".join(matches)
            )

    require(errors, (STORY / "archive" / "famu-v1" / "timeline-weeks-prose").exists(), "Legacy prose archive is missing")
    require(errors, (ROOT / "art" / "archive" / "famu-v1" / "final").exists(), "Legacy art archive is missing")
    require(errors, not (STORY / "timeline-weeks-prose").exists(), "Legacy prose must not remain in the active story path")

    if errors:
        print("STORY V2 VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("STORY V2 VALIDATION PASSED")
    print("- 54 weeks")
    print("- 374 unique daily beats")
    print("- fall, spring reversal, and summer resolution present")
    print("- Calculus I, II, and III topic progression present")
    print("- sports, family, conference, presentation, and national-lab tracks present")
    print("- active comic production remains blocked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
