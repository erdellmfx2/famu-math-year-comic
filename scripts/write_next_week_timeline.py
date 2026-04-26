#!/usr/bin/env python3
"""Write one 7-day timeline slice from master_calendar_2025_2026.csv per run.

Outputs markdown files under story/timeline-weeks/ and advances state in
story/timeline_writer_state.json.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "story" / "master_calendar_2025_2026.csv"
OUT_DIR = ROOT / "story" / "timeline-weeks"
STATE_PATH = ROOT / "story" / "timeline_writer_state.json"


@dataclass
class WeekSlice:
    index: int
    rows: list[dict]


def load_rows() -> list[dict]:
    if not MASTER.exists():
        raise FileNotFoundError(f"Missing master calendar: {MASTER}")
    with MASTER.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_state(total_weeks: int) -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {
        "next_week_index": 0,
        "total_weeks": total_weeks,
        "completed": [],
    }


def chunk_weeks(rows: list[dict]) -> list[WeekSlice]:
    weeks = []
    for i in range(0, len(rows), 7):
        idx = i // 7
        weeks.append(WeekSlice(index=idx, rows=rows[i : i + 7]))
    return weeks


def build_week_markdown(week: WeekSlice) -> str:
    start = week.rows[0]["date"]
    end = week.rows[-1]["date"]
    title = f"# Timeline Week {week.index + 1:03d} ({start} to {end})"

    lines = [title, "", "## Weekly Highlights", ""]
    high = [r for r in week.rows if r.get("priority_score") in ("high", "peak")]
    if high:
        for r in high:
            trigger = r.get("sports_events") or r.get("syllabus_events") or r.get("fixed_events") or "High-pressure day"
            lines.append(f"- **{r['date']}** ({r['priority_score']}): {trigger}")
    else:
        lines.append("- Steady week with no major peak-pressure overlaps.")

    lines += ["", "## Daily Beat Plan", ""]
    for r in week.rows:
        lines += [
            f"### {r['date']} ({r.get('academic_phase', 'n/a')})",
            f"- Fixed events: {r.get('fixed_events') or '—'}",
            f"- Syllabus events: {r.get('syllabus_events') or '—'}",
            f"- Sports/events: {r.get('sports_events') or '—'}",
            f"- Malik activity: {r.get('character_activity_malik') or '—'}",
            f"- Nia activity: {r.get('character_activity_nia') or '—'}",
            f"- Professor touchpoint: {r.get('professor_touchpoint') or '—'}",
            f"- Comic scene hint: {r.get('comic_scene_hint') or '—'}",
            "",
        ]

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    rows = load_rows()
    weeks = chunk_weeks(rows)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    state = load_state(total_weeks=len(weeks))
    next_idx = int(state.get("next_week_index", 0))

    if next_idx >= len(weeks):
        print("NOOP: timeline complete")
        return 0

    week = weeks[next_idx]
    start = week.rows[0]["date"]
    end = week.rows[-1]["date"]
    week_number = week.index + 1
    out_name = f"{week_number}.md"
    out_path = OUT_DIR / out_name

    out_path.write_text(build_week_markdown(week), encoding="utf-8")

    completed = state.get("completed", [])
    completed.append(
        {
            "week_index": week.index,
            "week_number": week_number,
            "start": start,
            "end": end,
            "file": str(out_path.relative_to(ROOT)),
        }
    )
    state["completed"] = completed
    state["next_week_index"] = week.index + 1
    state["total_weeks"] = len(weeks)
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")

    print(f"WROTE: {out_path.relative_to(ROOT)}")
    print(f"PROGRESS: {state['next_week_index']}/{state['total_weeks']} weeks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
