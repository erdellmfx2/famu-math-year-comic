#!/usr/bin/env python3
"""Package Week 15 with face-safe lettering and social-release files."""

from __future__ import annotations

import shutil
from pathlib import Path

import finish_week04_comic as package


ROOT = Path(__file__).resolve().parents[1]
WEEK_DIR = ROOT / "art" / "final" / "week-15"
BOARD_DIR = ROOT / "art" / "storyboards" / "week-15"
APPROVED = ROOT / "art" / "final" / "series-endcards" / "approved"


def main() -> None:
    lettering = package.lettering
    lettering.WEEK_DIR = WEEK_DIR
    lettering.BOARD_DIR = BOARD_DIR
    lettering.ARC_TITLE = "WHAT CAN STILL BE CHANGED"
    lettering.END_CARDS = [
        "thank-you-end-card-v1.png",
        "mathematics-invitation-end-card-v1.png",
        "famu-mathematics-attribution-end-card-v1.png",
        "thank-you-end-card-v1.png",
        "mathematics-invitation-end-card-v1.png",
        "famu-mathematics-attribution-end-card-v1.png",
        "thank-you-end-card-v1.png",
    ]
    lettering.SPEAKER_ANCHORS.update({
        (99, 1, 2, "Dr. Brooks"): "left", (99, 1, 3, "Malik"): "right", (99, 1, 4, "Dr. Brooks"): "left", (99, 2, 1, "Student"): "left", (99, 2, 2, "Malik"): "right", (99, 2, 3, "Malik"): "right", (99, 2, 4, "Student"): "left",
        (100, 1, 1, "Celeste"): "left", (100, 1, 4, "Malik"): "right", (100, 2, 1, "Dr. Bennett"): "left", (100, 2, 2, "Dr. Bennett"): "left", (100, 2, 3, "Dr. Bennett"): "left",
        (101, 1, 1, "Dr. Brooks"): "left", (101, 1, 2, "Dr. Brooks"): "left", (101, 2, 1, "Nia"): "left", (101, 2, 2, "Malik"): "right", (101, 2, 3, "Nia"): "left", (101, 2, 4, "Malik"): "right",
        (102, 1, 2, "Simone"): "left", (102, 1, 3, "Malik"): "right", (102, 1, 4, "Simone"): "left", (102, 2, 1, "Simone"): "left", (102, 2, 2, "Malik"): "right", (102, 2, 3, "Simone"): "left",
        (103, 1, 2, "Julian"): "right", (103, 1, 3, "Nia"): "left", (103, 1, 4, "Nia"): "left", (103, 2, 2, "Julian"): "right", (103, 2, 3, "Nia"): "left",
        (104, 1, 2, "Julian"): "right", (104, 1, 3, "Nia"): "left", (104, 1, 4, "Julian"): "right", (104, 2, 1, "Nia"): "left", (104, 2, 2, "Julian"): "right",
        (105, 1, 2, "DJ"): "right", (105, 2, 2, "Nia"): "left", (105, 2, 3, "Malik"): "right",
    })
    for part, episode in enumerate(range(99, 106), start=1):
        episode_dir = WEEK_DIR / f"episode-{episode:02d}"
        sequence = episode_dir / "sequence-v2"
        sequence.mkdir(parents=True, exist_ok=True)
        lettering.make_title(part, sequence / "01-title-card-v1.png")
        for page in (1, 2):
            source = package.newest(list((episode_dir / "unlettered").glob(f"week-15-episode-{episode:02d}-page-{page:02d}-art-v*.png")))
            board = BOARD_DIR / f"week-15-episode-{episode:02d}-page-{page:02d}.md"
            output = episode_dir / f"week-15-episode-{episode:02d}-page-{page:02d}-lettered-v1.png"
            package.letter_page(source, board, output, episode, page)
            shutil.copy2(output, sequence / f"0{page + 1}-comic-page-{page:02d}-v1.png")
        end_card = lettering.END_CARDS[part - 1]
        shutil.copy2(APPROVED / end_card, sequence / f"04-{end_card}")
    print("Finished Week 15 title, lettering, page-mark, and end-card packages.")


if __name__ == "__main__":
    main()
