#!/usr/bin/env python3
"""Package Week 6 with the approved lettering and social-release system."""

from __future__ import annotations

import shutil
from pathlib import Path

import finish_week04_comic as lettering_package


ROOT = Path(__file__).resolve().parents[1]
WEEK_DIR = ROOT / "art" / "final" / "week-06"
BOARD_DIR = ROOT / "art" / "storyboards" / "week-06"
APPROVED = ROOT / "art" / "final" / "series-endcards" / "approved"


def main() -> None:
    lettering = lettering_package.lettering
    lettering.WEEK_DIR = WEEK_DIR
    lettering.BOARD_DIR = BOARD_DIR
    lettering.ARC_TITLE = "CONTINUITY UNDER PRESSURE"
    lettering.END_CARDS = [
        "thank-you-end-card-v1.png",
        "mathematics-invitation-end-card-v1.png",
        "famu-mathematics-attribution-end-card-v1.png",
        "thank-you-end-card-v1.png",
        "mathematics-invitation-end-card-v1.png",
        "famu-mathematics-attribution-end-card-v1.png",
        "thank-you-end-card-v1.png",
    ]

    # The art stages the two-person conversations in reverse of the default anchors.
    lettering.SPEAKER_ANCHORS.update(
        {
            (38, 2, 1, "Julian"): "left",
            (38, 2, 1, "Nia"): "right",
            (38, 2, 2, "Julian"): "left",
            (38, 2, 2, "Nia"): "right",
            (39, 1, 2, "Keisha"): "left",
            (39, 1, 2, "Nia"): "right",
            (39, 2, 2, "Nia"): "left",
            (39, 2, 2, "Keisha"): "right",
            (41, 2, 2, "Andre"): "left",
            (41, 2, 2, "Malik"): "right",
            (42, 1, 1, "Nia"): "left",
            (42, 1, 1, "Julian"): "right",
            (42, 2, 1, "Julian"): "left",
            (42, 2, 1, "Nia"): "right",
            (42, 2, 3, "Julian"): "left",
            (42, 2, 3, "Nia"): "right",
        }
    )

    for part, episode in enumerate(range(36, 43), start=1):
        episode_dir = WEEK_DIR / f"episode-{episode:02d}"
        sequence = episode_dir / "sequence-v2"
        sequence.mkdir(parents=True, exist_ok=True)
        lettering.make_title(part, sequence / "01-title-card-v1.png")
        for page in (1, 2):
            source = lettering_package.newest(
                list(
                    (episode_dir / "unlettered").glob(
                        f"week-06-episode-{episode:02d}-page-{page:02d}-art-v*.png"
                    )
                )
            )
            board = BOARD_DIR / f"week-06-episode-{episode:02d}-page-{page:02d}.md"
            output = episode_dir / f"week-06-episode-{episode:02d}-page-{page:02d}-lettered-v1.png"
            lettering_package.letter_page(source, board, output, episode, page)
            shutil.copy2(output, sequence / f"0{page + 1}-comic-page-{page:02d}-v1.png")
        end_card = lettering.END_CARDS[part - 1]
        shutil.copy2(APPROVED / end_card, sequence / f"04-{end_card}")

    print("Finished Week 6 title, lettering, page-mark, and end-card packages.")


if __name__ == "__main__":
    main()
