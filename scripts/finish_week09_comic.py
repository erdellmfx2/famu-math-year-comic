#!/usr/bin/env python3
"""Package Week 9 with face-safe lettering and social-release files."""

from __future__ import annotations

import shutil
from pathlib import Path

import finish_week04_comic as lettering_package


ROOT = Path(__file__).resolve().parents[1]
WEEK_DIR = ROOT / "art" / "final" / "week-09"
BOARD_DIR = ROOT / "art" / "storyboards" / "week-09"
APPROVED = ROOT / "art" / "final" / "series-endcards" / "approved"


def letter_panel_with_safe_dialogue_order(
    draw, letters, bounds, episode, page, panel_number
) -> None:
    """Keep alternating three-line exchanges from crossing balloon tails."""
    lettering = lettering_package.lettering
    target = (episode, page, panel_number)
    alternating_triples = {(58, 2, 4), (60, 2, 4)}
    reversed_pairs = {
        (57, 2, 2), (57, 2, 3),
        (59, 1, 4), (59, 2, 1), (59, 2, 2),
        (60, 1, 3), (60, 1, 4),
        (63, 1, 4),
    }
    if target not in alternating_triples | reversed_pairs:
        return lettering._week09_original_letter_panel(
            draw, letters, bounds, episode, page, panel_number
        )

    left, top, right, _bottom = bounds
    band_bottom = top + lettering.LETTERING_BAND - 10
    gap = 7
    half_width = (right - left - gap * 3) // 2
    half_height = (band_bottom - top - gap * 3) // 2
    left_top = (left + gap, top + gap, left + gap + half_width, top + gap + half_height)
    right_top = (left + gap * 2 + half_width, top + gap, right - gap, top + gap + half_height)
    right_bottom = (left + gap * 2 + half_width, top + gap * 2 + half_height, right - gap, band_bottom)
    boxes = (
        [right_top, left_top, right_bottom]
        if target in alternating_triples
        else [right_top, left_top]
    )

    speech_index = 0
    for item, box in zip(letters, boxes, strict=True):
        if item.kind == "caption":
            lettering.draw_caption(draw, item.text, box)
            continue
        speaker = item.speaker.split(" (", 1)[0]
        side = lettering.speaker_side(episode, page, panel_number, speaker, speech_index)
        target_x = left + int((right - left) * {"left": 0.27, "center": 0.5, "right": 0.73}[side])
        target_y = top + lettering.LETTERING_BAND + 34
        lettering.draw_speech(draw, item.text, box, (target_x, target_y))
        speech_index += 1


def main() -> None:
    lettering = lettering_package.lettering
    lettering.WEEK_DIR = WEEK_DIR
    lettering.BOARD_DIR = BOARD_DIR
    lettering.ARC_TITLE = "WHAT WATER TAKES"
    lettering.END_CARDS = [
        "thank-you-end-card-v1.png",
        "mathematics-invitation-end-card-v1.png",
        "famu-mathematics-attribution-end-card-v1.png",
        "thank-you-end-card-v1.png",
        "mathematics-invitation-end-card-v1.png",
        "famu-mathematics-attribution-end-card-v1.png",
        "thank-you-end-card-v1.png",
    ]
    lettering._week09_original_letter_panel = lettering.letter_panel
    lettering.letter_panel = letter_panel_with_safe_dialogue_order
    lettering.SPEAKER_ANCHORS.update(
        {
            (57, 1, 4, "Marcel"): "left", (57, 1, 4, "Malik"): "right",
            (57, 2, 2, "Celeste"): "left", (57, 2, 2, "Malik"): "right",
            (57, 2, 3, "Celeste"): "left", (57, 2, 3, "Malik"): "right",
            (57, 2, 4, "Marcel"): "left",
            (58, 1, 2, "Micah"): "left", (58, 1, 2, "Malik"): "right",
            (58, 2, 1, "Micah"): "left", (58, 2, 1, "Malik"): "right",
            (58, 2, 2, "Micah"): "left", (58, 2, 2, "Malik"): "right",
            (58, 2, 3, "Micah"): "left",
            (58, 2, 4, "Micah"): "left", (58, 2, 4, "Malik"): "right",
            (59, 1, 1, "Simone"): "left", (59, 1, 1, "Malik"): "right",
            (59, 1, 2, "Simone"): "left", (59, 1, 2, "Malik"): "right",
            (59, 1, 4, "Simone"): "left", (59, 1, 4, "Malik"): "right",
            (59, 2, 1, "Simone"): "left", (59, 2, 1, "Malik"): "right",
            (59, 2, 2, "Simone"): "left", (59, 2, 2, "Malik"): "right",
            (59, 2, 3, "Simone"): "left", (59, 2, 4, "Malik"): "right",
            (60, 1, 3, "Nia"): "left", (60, 1, 3, "Julian"): "right",
            (60, 1, 4, "Nia"): "left", (60, 1, 4, "Julian"): "right",
            (60, 2, 4, "Nia"): "left", (60, 2, 4, "Julian"): "right",
            (62, 1, 2, "Counselor"): "left", (62, 1, 4, "Counselor"): "left",
            (62, 2, 1, "Malik"): "right",
            (63, 1, 3, "Nia"): "left", (63, 1, 3, "Malik"): "center",
            (63, 1, 4, "Julian"): "right", (63, 1, 4, "Malik"): "center",
            (63, 2, 1, "Nia"): "left", (63, 2, 2, "Malik"): "right",
            (63, 2, 3, "Nia"): "left", (63, 2, 3, "Malik"): "right",
            (63, 2, 4, "Malik"): "right",
        }
    )

    for part, episode in enumerate(range(57, 64), start=1):
        episode_dir = WEEK_DIR / f"episode-{episode:02d}"
        sequence = episode_dir / "sequence-v2"
        sequence.mkdir(parents=True, exist_ok=True)
        lettering.make_title(part, sequence / "01-title-card-v1.png")
        for page in (1, 2):
            source = lettering_package.newest(list((episode_dir / "unlettered").glob(f"week-09-episode-{episode:02d}-page-{page:02d}-art-v*.png")))
            board = BOARD_DIR / f"week-09-episode-{episode:02d}-page-{page:02d}.md"
            output = episode_dir / f"week-09-episode-{episode:02d}-page-{page:02d}-lettered-v1.png"
            lettering_package.letter_page(source, board, output, episode, page)
            shutil.copy2(output, sequence / f"0{page + 1}-comic-page-{page:02d}-v1.png")
        end_card = lettering.END_CARDS[part - 1]
        shutil.copy2(APPROVED / end_card, sequence / f"04-{end_card}")
    print("Finished Week 9 title, lettering, page-mark, and end-card packages.")


if __name__ == "__main__":
    main()
