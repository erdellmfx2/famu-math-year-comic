#!/usr/bin/env python3
"""Combine all 54 v2 weekly scripts into one approval manuscript."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STORY_DIR = ROOT / "story"
PLAN_PATH = STORY_DIR / "season_plan_v2.json"
APPROVAL_PATH = STORY_DIR / "approval_status.json"
WEEK_DIR = STORY_DIR / "timeline-weeks"
DEFAULT_OUTPUT = STORY_DIR / "script-v2-output" / "the-formula-of-becoming-script-v2.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_week_number(path: Path) -> int:
    match = re.fullmatch(r"(\d+)\.md", path.name)
    if not match:
        raise ValueError(f"Unexpected weekly filename: {path.name}")
    return int(match.group(1))


def load_week_files() -> list[tuple[int, str]]:
    paths = sorted(WEEK_DIR.glob("*.md"), key=extract_week_number)
    numbers = [extract_week_number(path) for path in paths]
    if numbers != list(range(1, 55)):
        raise ValueError("Expected exactly story/timeline-weeks/1.md through 54.md")
    return [
        (extract_week_number(path), path.read_text(encoding="utf-8").strip())
        for path in paths
    ]


def build_document(plan: dict, approval: dict, weeks: list[tuple[int, str]]) -> str:
    status = "APPROVED" if approval.get("script_approved") else "AWAITING APPROVAL"
    lines = [
        "# The Formula of Becoming",
        "",
        "## Season One v2 Approval Script",
        "",
        f"Setting: **{plan['setting']} (fictional)**",
        "",
        f"Story window: **{plan['date_range']['start']} to {plan['date_range']['end']}**",
        "",
        f"Script status: **{status}**",
        "",
        "> This manuscript contains story beats only. It is not approval to create comic art. New storyboards, prompts, panels, and pages remain blocked until `story/approval_status.json` records explicit approval.",
        "",
        "## Review Map",
        "",
        "- Weeks 1-3: Summer Bridge, meeting, and supporting-cast setup",
        "- Weeks 4-19: Fall Calculus I, Nia and Julian, Malik's family crisis, analytics failure, and football success",
        "- Weeks 20-22: Winter consequences and reversal setup",
        "- Weeks 23-39: Spring Calculus II, Malik and Simone, Nia's research challenge, and fellowship loss",
        "- Weeks 40-47: Summer transition, Calculus III, family repair, and national-lab work",
        "- Weeks 48-54: Romantic resolution, public project use, showcase, and year-two close",
        "",
        "## Weekly Contents",
        "",
    ]
    for week in plan["weeks"]:
        lines.append(f"- Week {week['week']:02d}: {week['title']}")

    for _, content in weeks:
        lines.extend(["", "---", "", content])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    plan = load_json(PLAN_PATH)
    approval = load_json(APPROVAL_PATH)
    weeks = load_week_files()
    destination = args.output.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(build_document(plan, approval, weeks), encoding="utf-8")
    print(f"WROTE: {destination.relative_to(ROOT)}")
    print(f"WEEKS: {len(weeks)}")
    print(f"SCRIPT_APPROVED: {bool(approval.get('script_approved'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
