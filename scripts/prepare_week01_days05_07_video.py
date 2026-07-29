#!/usr/bin/env python3
"""Prepare exact-prose full-cast manifests for Week 1 Days 5-7."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROSE = ROOT / "story" / "timeline-weeks-prose-v2" / "prose_1.md"

SPEAKERS = {
    "narrator": {
        "voice": "cedar",
        "instructions": (
            "Speak only supplied narration in a warm, grounded, observant, quietly "
            "lyrical documentary delivery. Be clear, restrained, and unhurried. "
            "Quicken slightly for campus montage. Do not perform character dialogue "
            "or add words."
        ),
    },
    "malik": {
        "voice": "ash",
        "instructions": (
            "Speak only Malik's supplied words. He is precise, guarded, economical, "
            "and quietly warm when trust appears. Use a measured medium-low delivery "
            "and dry humor without adding words."
        ),
    },
    "nia": {
        "voice": "coral",
        "instructions": (
            "Speak only Nia's supplied words. She is bright, expressive, curious, "
            "and playful, with a lively conversational pace. Slow slightly for human "
            "consequences. Do not add words."
        ),
    },
    "julian": {
        "voice": "verse",
        "instructions": (
            "Speak only Julian's supplied words. He is warm, smooth, and publicly "
            "confident, with a musician's sense of timing. Keep him welcoming rather "
            "than smug or seductive. Do not add words."
        ),
    },
}


def u(speaker: str, text: str) -> dict[str, str]:
    return {"speaker": speaker, "text": text}


DAY_CONFIG = {
    5: {
        "title": "The Campus Has a Memory",
        "heading": "Tuesday, August 5: The Campus Has a Memory",
        "message": "A campus becomes meaningful when people learn how to move through it together.",
        "scenes": [
            {
                "id": "01-tour",
                "panel": "page-01-panels-01-02",
                "utterances": [
                    u("narrator", "The campus tour began at Jubilee Library, moved through the glass-walled North Star Learning Commons, and ended beneath the live oaks along Cypress Walk."),
                    u("narrator", "Nia photographed everything: the copper-framed windows of Eliza Moss Hall, the old reading room inside Jubilee, the wall of whiteboards at North Star, even a campus cat sleeping under a bench as though it had tenure."),
                ],
            },
            {
                "id": "02-map",
                "panel": "page-01-panels-03-04",
                "utterances": [
                    u("narrator", "Malik photographed the map."),
                    u("nia", "You know they give us that online,"),
                    u("narrator", "Nia said."),
                    u("malik", "Phones lose signal."),
                    u("nia", "Paper maps exist."),
                    u("malik", "Paper gets wet."),
                    u("nia", "Do you prepare for joy like this too?"),
                    u("narrator", "He considered it."),
                    u("malik", "I have not had to."),
                ],
            },
            {
                "id": "03-bell",
                "panel": "page-02-panels-01-02",
                "utterances": [
                    u("narrator", "Their guide led them to Founders' Bell, greened with age and suspended beneath a limestone arch. It had once called students to assembly, she explained. Now it rang at Opening Convocation and commencement, marking the entrance and exit of a McCall-Hart education."),
                    u("narrator", "Nia looked up at it."),
                    u("nia", "Imagine hearing that on your last day here."),
                    u("narrator", "Malik looked down Cypress Walk, where indigo banners shifted in the humid breeze. Four years seemed both enormous and dangerously brief."),
                ],
            },
            {
                "id": "04-steps",
                "panel": "page-02-panels-03-04",
                "utterances": [
                    u("malik", "We have to make it to the first day first,"),
                    u("narrator", "he said."),
                    u("nia", "You really refuse to skip steps."),
                    u("malik", "Steps exist for a reason."),
                    u("nia", "So do leaps."),
                    u("narrator", "He glanced at her."),
                    u("malik", "Leaps are just steps with poor documentation."),
                    u("narrator", "Nia laughed so hard the tour guide turned around."),
                ],
            },
        ],
    },
    6: {
        "title": "Indigo Night",
        "heading": "Wednesday, August 6: Indigo Night",
        "message": "Belonging begins when students risk choosing what might become part of them.",
        "scenes": [
            {
                "id": "01-festival",
                "panel": "page-01-panels-01-02",
                "utterances": [
                    u("narrator", "Indigo Night transformed Hart Student Union into a festival of music, food, club tables, and first-year students trying out possible versions of themselves."),
                    u("narrator", "Nia moved through it like a spark in dry grass. She signed an interest card for the Association for Women in Mathematics, took a flyer from Math Circle, promised to visit campus radio, and nearly volunteered for a service event before Malik removed the pen from her hand."),
                    u("malik", "You cannot join the whole university tonight."),
                    u("nia", "Watch me."),
                    u("malik", "I am watching. It is concerning."),
                ],
            },
            {
                "id": "02-saxophone",
                "panel": "page-01-panels-03-04",
                "utterances": [
                    u("narrator", "Across the terrace, an alto saxophone climbed above the crowd. A small group from the Marching Herons was performing beside the radio booth. The saxophonist played with his eyes half closed, then opened them at the exact moment Nia stepped closer."),
                    u("narrator", "After the set, he introduced himself as Julian Cross, second-year media arts student, campus radio host, and, according to him,"),
                    u("julian", "occasional rescuer of boring events."),
                    u("nia", "This event was not boring,"),
                    u("narrator", "Nia said."),
                    u("julian", "Then I can take the night off."),
                    u("narrator", "His confidence should have been irritating. Somehow, it was not."),
                ],
            },
            {
                "id": "03-invitation",
                "panel": "page-02-panel-01",
                "utterances": [
                    u("narrator", "Julian told her about a radio showcase on Friday and invited her to stop by. Nia said yes with the speed she used for nearly every interesting opportunity."),
                ],
            },
            {
                "id": "04-analytics",
                "panel": "page-02-panels-02-03",
                "utterances": [
                    u("narrator", "At another table, Malik found a sign for the Heron Analytics Challenge. Fourth-down decisions. Player performance. Ticket demand. Real datasets, competitive teams, regional presentations."),
                    u("narrator", "He read every line twice before writing his name."),
                    u("narrator", "When he and Nia met again near the Copper Cup Cafe, they both had news."),
                    u("nia", "I got invited to the radio showcase,"),
                    u("narrator", "Nia said."),
                    u("malik", "I signed up for an analytics information session."),
                    u("nia", "Look at us choosing things."),
                    u("malik", "You chose six things."),
                    u("nia", "Seven, technically."),
                ],
            },
            {
                "id": "05-unnamed",
                "panel": "page-02-panel-04",
                "utterances": [
                    u("narrator", "He shook his head, but his attention drifted to Julian across the room. Julian saw Nia and lifted two fingers in a casual salute. She smiled back."),
                    u("narrator", "Malik did not yet have a name for the small drop inside his chest. He treated it like a number too minor to enter."),
                ],
            },
        ],
    },
    7: {
        "title": "Accountability",
        "heading": "Thursday, August 7: Accountability",
        "message": "Accountability is the choice to make assumptions, schedules, and feelings visible.",
        "scenes": [
            {
                "id": "01-presentation",
                "panel": "page-01-panels-01-04",
                "utterances": [
                    u("narrator", "Their final Bridge presentation returned to the budget model Malik had repaired, expanded into a scenario for a first-year student managing books, meals, transportation, and emergencies."),
                    u("narrator", "Malik explained the spreadsheet logic. Nia told the story of what happened when one assumption changed. They showed the original error, the revised categories, and a sensitivity table that made visible how quickly a small surprise could become a larger problem."),
                    u("nia", "A budget is not a promise that nothing will go wrong,"),
                    u("narrator", "Nia told the room."),
                    u("nia", "It is a way to notice change early enough to make choices."),
                    u("narrator", "Malik advanced the slide."),
                    u("malik", "And a model should show what it assumes, so the person using it knows when the answer no longer applies."),
                    u("narrator", "Dr. Brooks smiled from the back row."),
                ],
            },
            {
                "id": "02-bell",
                "panel": "page-02-panels-01-02",
                "utterances": [
                    u("narrator", "Afterward, Malik and Nia carried their laptops to the Founders' Bell. The campus was copper in the late sun, and somewhere near the union a drumline practiced the same eight measures until they became part of the air."),
                    u("nia", "We work well together,"),
                    u("narrator", "Nia said."),
                    u("malik", "After arguing."),
                    u("nia", "During arguing. The arguing is part of the system."),
                    u("malik", "That sounds unhealthy."),
                    u("nia", "Only because you hate being challenged by someone delightful."),
                ],
            },
            {
                "id": "03-pact",
                "panel": "page-02-panel-03",
                "utterances": [
                    u("narrator", "Malik leaned against the limestone arch."),
                    u("malik", "We should keep each other on schedule when classes start. Weekly check-in. Assignments, deadlines, major commitments."),
                    u("narrator", "Nia held out her hand."),
                    u("nia", "Accountability partners. Academic honesty, honest schedules, and emergency snack intervention."),
                    u("malik", "Define emergency."),
                    u("nia", "If you have to ask, you are already in one."),
                    u("narrator", "He shook her hand."),
                ],
            },
            {
                "id": "04-two-plans",
                "panel": "page-02-panel-04",
                "utterances": [
                    u("narrator", "Then Nia mentioned that Julian had sent her the details for Friday's showcase."),
                    u("nia", "I think he might actually be asking me out,"),
                    u("narrator", "she said, trying and failing to sound casual."),
                    u("narrator", "Malik released her hand and adjusted the strap of his laptop bag."),
                    u("malik", "You should go,"),
                    u("narrator", "he said. His voice was kind, steady, and almost completely convincing."),
                    u("malik", "You wanted to see the radio station."),
                    u("narrator", "Nia studied him for half a second, then smiled."),
                    u("nia", "I did."),
                    u("narrator", "They walked away from the bell together, carrying two kinds of plans into the next week: the ones they had said aloud and the ones they had not yet admitted, even to themselves."),
                ],
            },
        ],
    },
}


def normalize(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", value.lower().replace("’", "'"))


def section(source: str, heading: str) -> str:
    marker = f"## {heading}\n\n"
    start = source.index(marker) + len(marker)
    next_heading = source.find("\n## ", start)
    return source[start:] if next_heading == -1 else source[start:next_heading]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    source = PROSE.read_text(encoding="utf-8")
    report = {}

    for day, config in DAY_CONFIG.items():
        video_dir = ROOT / "video" / f"week-01-day-{day:02d}"
        manifest = {
            "project": f"The Formula of Becoming - Week 1 Day {day} - Full Cast",
            "model": "gpt-4o-mini-tts",
            "response_format": "mp3",
            "default_pause_after": 0.18,
            "speakers": {
                speaker: SPEAKERS[speaker]
                for speaker in sorted(
                    {utterance["speaker"] for scene in config["scenes"] for utterance in scene["utterances"]}
                )
            },
            "scenes": config["scenes"],
        }
        write_text(
            video_dir / "full-cast-manifest.json",
            json.dumps(manifest, indent=2, ensure_ascii=True),
        )

        source_section = section(source, config["heading"])
        performed = " ".join(
            utterance["text"]
            for scene in config["scenes"]
            for utterance in scene["utterances"]
        )
        source_words = normalize(source_section)
        performed_words = normalize(performed)
        exact = source_words == performed_words
        report[str(day)] = {
            "heading": config["heading"],
            "source_words": len(source_words),
            "manifest_words": len(performed_words),
            "exact_normalized_match": exact,
        }
        if not exact:
            for index, (left, right) in enumerate(zip(source_words, performed_words)):
                if left != right:
                    raise ValueError(
                        f"Day {day} source mismatch at word {index + 1}: {left!r} != {right!r}"
                    )
            raise ValueError(
                f"Day {day} source length mismatch: {len(source_words)} != {len(performed_words)}"
            )

        write_text(
            video_dir / "BRIEF.md",
            f"""---
workflow: general-video
flow: automation
storyboard: no
message: "{config['message']}"
destination: social-media
aspect: 9:16
language: English
audience: "McCall-Hart comic readers and the FAMU Mathematics Department"
---

# Week 1 Day {day} Video Brief

Create a vertical, captioned, full-cast motion-comic video for "{config['title']}." Begin
with the approved title card, perform the complete approved prose section exactly, use
the two approved unlettered comic pages as the visual source, and end on the approved
message card.

Use perceptible 8 to 10 percent Ken Burns zoom-outs and a word-highlight caption rail
with `#215732` as the active-word color. Preserve the established Week 1 voice cast.
Do not add music, sound effects, stock imagery, or extra story text.

AI-generated voices must be disclosed in publication notes.
""",
        )
        write_text(
            video_dir / "DESIGN.md",
            f"""# Design: Week 1 Day {day}

- Delivery: 1080 by 1920, 30 fps, captioned portrait social video.
- Cards: preserve the approved title and closing cards intact over deep indigo.
- Story art: use the approved unlettered pages; show one panel at a time over a
  softly blurred copy of the same page.
- Motion: every story visual begins near 110% scale and settles continuously toward
  100% with a small one-way drift.
- Captions: white Montserrat on a dark indigo rail; only the spoken word receives
  a `#215732` backing pill.
- Audio: no music or effects; use the accepted full-cast voices and pronunciation locks.
""",
        )
        write_text(
            video_dir / "resource-ledger.md",
            f"""# Week 1 Day {day} Video Resource Ledger

## Allocation

- Weekly allocation remaining at start: not exposed to the workspace
- Production cap: no more than 50 percentage points of weekly allocation

## OpenAI Generation Log

| Stage | Calls | Words | Status |
| --- | ---: | ---: | --- |
| Full-cast TTS | {sum(len(scene['utterances']) for scene in config['scenes'])} | {len(performed_words)} | Pending |
| Word-level transcription | {len(config['scenes'])} | {len(performed_words)} | Pending |

## Local Production Log

| Stage | Status |
| --- | --- |
| Exact source audit | Complete |
| Scene audio assembly | Pending |
| HyperFrames authoring | Pending |
| Final render and QA | Pending |

The OpenAI weekly-allocation percentage is not available through the repository,
API key, or local scripts. This ledger records calls and source volume for
reconciliation against the account allocation meter.
""",
        )

    write_text(
        ROOT / "video" / "week-01-days-05-07-source-audit.json",
        json.dumps(report, indent=2),
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
