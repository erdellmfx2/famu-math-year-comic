#!/usr/bin/env python3
"""Package Week 8 with face-safe lettering and social-release files."""

from __future__ import annotations

import shutil
from pathlib import Path

import finish_week04_comic as lettering_package


ROOT = Path(__file__).resolve().parents[1]
WEEK_DIR = ROOT / "art" / "final" / "week-08"
BOARD_DIR = ROOT / "art" / "storyboards" / "week-08"
APPROVED = ROOT / "art" / "final" / "series-endcards" / "approved"


def letter_panel_with_safe_dialogue_order(
    draw, letters, bounds, episode, page, panel_number
) -> None:
    """Keep dense alternating dialogue face-safe without crossed balloon tails."""
    lettering = lettering_package.lettering
    target = (episode, page, panel_number)
    special_panels = {
        (50, 2, 4),  # Malik and Nia alternate four times.
        (52, 2, 4),  # Malik and Nia alternate around a quiet thank-you.
        (54, 2, 4),  # Malik and Celeste alternate through the phone call.
        (55, 2, 4),  # Malik, Dr. Brooks, then a closing narration.
    }
    if target not in special_panels:
        return lettering._week08_original_letter_panel(
            draw, letters, bounds, episode, page, panel_number
        )

    left, top, right, _bottom = bounds
    band_bottom = top + lettering.LETTERING_BAND - 10
    gap = 7
    half_width = (right - left - gap * 3) // 2
    half_height = (band_bottom - top - gap * 3) // 2
    left_top = (left + gap, top + gap, left + gap + half_width, top + gap + half_height)
    right_top = (
        left + gap * 2 + half_width,
        top + gap,
        right - gap,
        top + gap + half_height,
    )
    left_bottom = (
        left + gap,
        top + gap * 2 + half_height,
        left + gap + half_width,
        band_bottom,
    )
    right_bottom = (
        left + gap * 2 + half_width,
        top + gap * 2 + half_height,
        right - gap,
        band_bottom,
    )

    if target == (50, 2, 4):
        # Dialogue remains chronological from top to bottom while every tail
        # reaches the speaker's actual side of the panel.
        boxes = [right_top, left_top, right_bottom, left_bottom]
    elif target in {(52, 2, 4), (54, 2, 4)}:
        boxes = [right_top, left_top, (left + gap, top + gap * 2 + half_height, right - gap, band_bottom)]
    elif target == (55, 2, 4):
        boxes = [right_top, left_top, (left + gap, top + gap * 2 + half_height, right - gap, band_bottom)]
    else:
        boxes = [right_top, left_top]

    speech_index = 0
    for item, box in zip(letters, boxes, strict=True):
        if item.kind == "caption":
            lettering.draw_caption(draw, item.text, box)
            continue
        speaker = item.speaker.split(" (", 1)[0]
        side = lettering.speaker_side(
            episode, page, panel_number, speaker, speech_index
        )
        target_fraction = {"left": 0.27, "center": 0.5, "right": 0.73}[side]
        target_x = left + int((right - left) * target_fraction)
        target_y = top + lettering.LETTERING_BAND + 34
        lettering.draw_speech(draw, item.text, box, (target_x, target_y))
        speech_index += 1


def main() -> None:
    lettering = lettering_package.lettering
    lettering.WEEK_DIR = WEEK_DIR
    lettering.BOARD_DIR = BOARD_DIR
    lettering.ARC_TITLE = "NO MODEL FOR THE STORM"
    lettering.END_CARDS = [
        "thank-you-end-card-v1.png",
        "mathematics-invitation-end-card-v1.png",
        "famu-mathematics-attribution-end-card-v1.png",
        "thank-you-end-card-v1.png",
        "mathematics-invitation-end-card-v1.png",
        "famu-mathematics-attribution-end-card-v1.png",
        "thank-you-end-card-v1.png",
    ]
    lettering._week08_original_letter_panel = lettering.letter_panel
    lettering.letter_panel = letter_panel_with_safe_dialogue_order

    # These maps follow the actual left/right staging of the approved art.
    lettering.SPEAKER_ANCHORS.update(
        {
            (50, 2, 1, "Nia"): "left", (50, 2, 1, "Malik"): "right",
            (50, 2, 2, "Nia"): "left", (50, 2, 2, "Malik"): "right",
            (50, 2, 3, "Nia"): "left", (50, 2, 3, "Malik"): "right",
            (50, 2, 4, "Nia"): "left", (50, 2, 4, "Malik"): "right",
            (51, 2, 2, "Simone"): "left", (51, 2, 2, "Malik"): "right",
            (51, 2, 3, "Simone"): "left", (51, 2, 3, "Malik"): "right",
            (52, 1, 2, "Nia"): "left", (52, 1, 2, "Imani"): "right",
            (52, 1, 3, "Nia"): "left", (52, 1, 3, "Imani"): "right",
            (52, 2, 1, "Nia"): "left", (52, 2, 1, "Malik"): "right",
            (52, 2, 4, "Nia"): "left", (52, 2, 4, "Malik"): "right",
            (53, 2, 2, "Nia"): "left", (53, 2, 2, "Julian"): "right",
            (53, 2, 4, "Nia"): "left", (53, 2, 4, "Julian"): "right",
            (54, 2, 4, "Celeste"): "left", (54, 2, 4, "Malik"): "right",
            (55, 2, 4, "Dr. Brooks"): "left", (55, 2, 4, "Malik"): "right",
            (56, 1, 4, "DJ"): "center", (56, 1, 4, "Malik"): "right",
            (56, 2, 3, "Malik"): "left", (56, 2, 3, "Nia"): "right",
        }
    )

    for part, episode in enumerate(range(50, 57), start=1):
        episode_dir = WEEK_DIR / f"episode-{episode:02d}"
        sequence = episode_dir / "sequence-v2"
        sequence.mkdir(parents=True, exist_ok=True)
        lettering.make_title(part, sequence / "01-title-card-v1.png")
        for page in (1, 2):
            source = lettering_package.newest(
                list(
                    (episode_dir / "unlettered").glob(
                        f"week-08-episode-{episode:02d}-page-{page:02d}-art-v*.png"
                    )
                )
            )
            board = BOARD_DIR / f"week-08-episode-{episode:02d}-page-{page:02d}.md"
            output = episode_dir / f"week-08-episode-{episode:02d}-page-{page:02d}-lettered-v1.png"
            lettering_package.letter_page(source, board, output, episode, page)
            shutil.copy2(output, sequence / f"0{page + 1}-comic-page-{page:02d}-v1.png")
        end_card = lettering.END_CARDS[part - 1]
        shutil.copy2(APPROVED / end_card, sequence / f"04-{end_card}")

    print("Finished Week 8 title, lettering, page-mark, and end-card packages.")


if __name__ == "__main__":
    main()
