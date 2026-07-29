#!/usr/bin/env python3
"""Package Week 7 with the approved lettering and social-release system."""

from __future__ import annotations

import shutil
import re
from pathlib import Path

import finish_week04_comic as lettering_package


ROOT = Path(__file__).resolve().parents[1]
WEEK_DIR = ROOT / "art" / "final" / "week-07"
BOARD_DIR = ROOT / "art" / "storyboards" / "week-07"
APPROVED = ROOT / "art" / "final" / "series-endcards" / "approved"


def panel_letters_from_map(board: Path):
    """Read the binding dialogue-first balloon map used by Week 7 boards."""
    source = board.read_text(encoding="utf-8")
    section = source.split("## Balloon Map", 1)[1].split("## Pass-One Art Rules", 1)[0]
    panels = [[] for _ in range(4)]
    for panel, speaker, words in re.findall(
        r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
        section,
        flags=re.MULTILINE,
    ):
        panels[int(panel) - 1].append(
            lettering_package.lettering.Letter(speaker.strip(), words.strip())
        )
    if not all(panels):
        raise ValueError(f"Expected mapped dialogue in every panel of {board.name}")
    return panels


def letter_panel_with_safe_stacked_pair(draw, letters, bounds, episode, page, panel_number):
    """Keep the storm-confrontation exchange in source order without crossed tails."""
    if (episode, page, panel_number) != (49, 2, 1):
        return lettering_package.lettering._week07_original_letter_panel(
            draw, letters, bounds, episode, page, panel_number
        )

    left, top, right, _bottom = bounds
    band_bottom = top + lettering_package.lettering.LETTERING_BAND - 10
    gap = 7
    box_height = (band_bottom - top - gap * 3) // 2
    boxes = [
        (left + 28, top + gap, right - 28, top + gap + box_height),
        (left + 28, top + gap * 2 + box_height, right - 28, band_bottom),
    ]
    for item, box in zip(letters, boxes, strict=True):
        speaker = item.speaker.split(" (", 1)[0]
        side = lettering_package.lettering.speaker_side(
            episode, page, panel_number, speaker, 0
        )
        target_fraction = {"left": 0.27, "center": 0.5, "right": 0.73}[side]
        target_x = left + int((right - left) * target_fraction)
        target_y = top + lettering_package.lettering.LETTERING_BAND + 34
        lettering_package.lettering.draw_speech(draw, item.text, box, (target_x, target_y))


def main() -> None:
    lettering = lettering_package.lettering
    lettering.WEEK_DIR = WEEK_DIR
    lettering.BOARD_DIR = BOARD_DIR
    lettering.ARC_TITLE = "WHAT THE FIRST TEST MEASURES"
    lettering.panel_letters = panel_letters_from_map
    lettering._week07_original_letter_panel = lettering.letter_panel
    lettering.letter_panel = letter_panel_with_safe_stacked_pair
    lettering.END_CARDS = [
        "thank-you-end-card-v1.png",
        "mathematics-invitation-end-card-v1.png",
        "famu-mathematics-attribution-end-card-v1.png",
        "thank-you-end-card-v1.png",
        "mathematics-invitation-end-card-v1.png",
        "famu-mathematics-attribution-end-card-v1.png",
        "thank-you-end-card-v1.png",
    ]

    # The art consistently stages the paired conversations left-to-right.
    lettering.SPEAKER_ANCHORS.update(
        {
            (43, 2, 2, "DJ"): "left",
            (43, 2, 2, "Malik"): "right",
            (44, 2, 1, "Dr. Brooks"): "left",
            (44, 2, 1, "Malik"): "right",
            (44, 2, 2, "Dr. Brooks"): "left",
            (44, 2, 2, "Malik"): "right",
            (44, 2, 4, "Simone"): "left",
            (44, 2, 4, "Malik"): "right",
            (45, 1, 2, "Nia"): "left",
            (45, 1, 2, "Amara"): "right",
            (45, 1, 4, "Nia"): "left",
            (45, 1, 4, "Amara"): "right",
            (46, 1, 3, "Dr. Bennett"): "right",
            (47, 2, 3, "DJ"): "right",
            (47, 2, 3, "Malik"): "left",
            (48, 1, 1, "Nia"): "left",
            (48, 1, 1, "Malik"): "right",
            (48, 1, 2, "Nia"): "left",
            (48, 1, 2, "Malik"): "right",
            (49, 1, 4, "Nia"): "left",
            (49, 1, 4, "Malik"): "right",
            (49, 2, 1, "Nia"): "left",
            (49, 2, 1, "Malik"): "right",
            (49, 2, 2, "Malik"): "right",
            (49, 2, 3, "Nia"): "left",
            (49, 2, 4, "Malik"): "right",
        }
    )

    for part, episode in enumerate(range(43, 50), start=1):
        episode_dir = WEEK_DIR / f"episode-{episode:02d}"
        sequence = episode_dir / "sequence-v2"
        sequence.mkdir(parents=True, exist_ok=True)
        lettering.make_title(part, sequence / "01-title-card-v1.png")
        for page in (1, 2):
            source = lettering_package.newest(
                list(
                    (episode_dir / "unlettered").glob(
                        f"week-07-episode-{episode:02d}-page-{page:02d}-art-v*.png"
                    )
                )
            )
            board = BOARD_DIR / f"week-07-episode-{episode:02d}-page-{page:02d}.md"
            output = episode_dir / f"week-07-episode-{episode:02d}-page-{page:02d}-lettered-v1.png"
            lettering_package.letter_page(source, board, output, episode, page)
            shutil.copy2(output, sequence / f"0{page + 1}-comic-page-{page:02d}-v1.png")
        end_card = lettering.END_CARDS[part - 1]
        shutil.copy2(APPROVED / end_card, sequence / f"04-{end_card}")

    print("Finished Week 7 title, lettering, page-mark, and end-card packages.")


if __name__ == "__main__":
    main()
