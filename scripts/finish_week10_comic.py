#!/usr/bin/env python3
"""Package Week 10 with face-safe lettering and social-release files."""

from __future__ import annotations

import shutil
from pathlib import Path

import finish_week04_comic as package


ROOT = Path(__file__).resolve().parents[1]
WEEK_DIR = ROOT / "art" / "final" / "week-10"
BOARD_DIR = ROOT / "art" / "storyboards" / "week-10"
APPROVED = ROOT / "art" / "final" / "series-endcards" / "approved"


def safe_dialogue_order(draw, letters, bounds, episode, page, panel_number) -> None:
    """Keep right-to-left exchanges in the visual reading order of their speakers."""
    lettering = package.lettering
    target = (episode, page, panel_number)
    reverse_pairs = {(64, 1, 3), (65, 1, 2), (65, 1, 4), (66, 1, 1), (69, 1, 3)}
    triple_with_caption = {(70, 2, 4)}
    if target not in reverse_pairs | triple_with_caption:
        return lettering._week10_original_letter_panel(draw, letters, bounds, episode, page, panel_number)

    left, top, right, _bottom = bounds
    band_bottom = top + lettering.LETTERING_BAND - 10
    gap = 7
    half_width = (right - left - gap * 3) // 2
    left_top = (left + gap, top + gap, left + gap + half_width, band_bottom)
    right_top = (left + gap * 2 + half_width, top + gap, right - gap, band_bottom)

    if target in reverse_pairs:
        boxes = [right_top, left_top]
    else:
        half_height = (band_bottom - top - gap * 3) // 2
        left_top = (left + gap, top + gap, left + gap + half_width, top + gap + half_height)
        right_top = (left + gap * 2 + half_width, top + gap, right - gap, top + gap + half_height)
        caption_box = (left + gap, top + gap * 2 + half_height, right - gap, band_bottom)
        boxes = [right_top, left_top, caption_box]

    speech_index = 0
    for item, box in zip(letters, boxes, strict=True):
        if item.kind == "caption":
            lettering.draw_caption(draw, item.text, box)
            continue
        speaker = item.speaker.split(" (", 1)[0]
        side = lettering.speaker_side(episode, page, panel_number, speaker, speech_index)
        target_x = left + int((right - left) * {"left": 0.27, "center": 0.5, "right": 0.73}[side])
        lettering.draw_speech(draw, item.text, box, (target_x, top + lettering.LETTERING_BAND + 34))
        speech_index += 1


def main() -> None:
    lettering = package.lettering
    lettering.WEEK_DIR = WEEK_DIR
    lettering.BOARD_DIR = BOARD_DIR
    lettering.ARC_TITLE = "THE COST OF LOOKING FINE"
    lettering.END_CARDS = [
        "thank-you-end-card-v1.png",
        "mathematics-invitation-end-card-v1.png",
        "famu-mathematics-attribution-end-card-v1.png",
        "thank-you-end-card-v1.png",
        "mathematics-invitation-end-card-v1.png",
        "famu-mathematics-attribution-end-card-v1.png",
        "thank-you-end-card-v1.png",
    ]
    lettering._week10_original_letter_panel = lettering.letter_panel
    lettering.letter_panel = safe_dialogue_order
    lettering.SPEAKER_ANCHORS.update({
        (64, 1, 2, "Ms. Alvarez"): "left", (64, 1, 3, "Malik"): "right", (64, 1, 3, "Ms. Alvarez"): "left",
        (64, 2, 3, "Ms. Alvarez"): "left", (64, 2, 4, "Ms. Alvarez"): "left",
        (65, 1, 1, "Simone"): "left", (65, 1, 2, "Malik"): "right", (65, 1, 2, "Simone"): "left",
        (65, 1, 3, "Andre"): "left", (65, 1, 4, "Malik"): "right", (65, 1, 4, "Simone"): "left",
        (65, 2, 1, "Simone"): "left", (65, 2, 3, "Simone"): "left", (65, 2, 4, "Malik"): "right",
        (66, 1, 1, "Nia"): "left", (66, 1, 1, "Julian"): "right", (66, 1, 3, "Nia"): "left",
        (67, 1, 4, "Malik"): "right", (67, 2, 2, "Nia"): "left", (67, 2, 3, "Malik"): "right",
        (68, 1, 3, "Nia"): "left", (69, 1, 1, "Malik"): "right", (69, 1, 2, "Malik"): "right",
        (69, 1, 3, "Malik"): "right", (69, 1, 3, "Nia"): "left", (69, 1, 4, "Nia"): "left",
        (69, 2, 1, "Malik"): "right", (69, 2, 2, "Nia"): "left", (69, 2, 4, "Nia"): "left", (69, 2, 4, "Malik"): "right",
        (70, 1, 2, "Dr. Brooks"): "left", (70, 1, 3, "Malik"): "right",
        (70, 2, 1, "Malik"): "right", (70, 2, 2, "Dr. Bennett"): "left", (70, 2, 3, "Simone"): "left",
        (70, 2, 4, "Malik"): "right", (70, 2, 4, "Simone"): "left",
    })

    for part, episode in enumerate(range(64, 71), start=1):
        episode_dir = WEEK_DIR / f"episode-{episode:02d}"
        sequence = episode_dir / "sequence-v2"
        sequence.mkdir(parents=True, exist_ok=True)
        lettering.make_title(part, sequence / "01-title-card-v1.png")
        for page in (1, 2):
            source = package.newest(list((episode_dir / "unlettered").glob(f"week-10-episode-{episode:02d}-page-{page:02d}-art-v*.png")))
            board = BOARD_DIR / f"week-10-episode-{episode:02d}-page-{page:02d}.md"
            output = episode_dir / f"week-10-episode-{episode:02d}-page-{page:02d}-lettered-v1.png"
            package.letter_page(source, board, output, episode, page)
            shutil.copy2(output, sequence / f"0{page + 1}-comic-page-{page:02d}-v1.png")
        end_card = lettering.END_CARDS[part - 1]
        shutil.copy2(APPROVED / end_card, sequence / f"04-{end_card}")
    print("Finished Week 10 title, lettering, page-mark, and end-card packages.")


if __name__ == "__main__":
    main()
