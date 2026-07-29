#!/usr/bin/env python3
"""Package Week 12 with face-safe lettering and social-release files."""

from __future__ import annotations

import shutil
from pathlib import Path

import finish_week04_comic as package


ROOT = Path(__file__).resolve().parents[1]
WEEK_DIR = ROOT / "art" / "final" / "week-12"
BOARD_DIR = ROOT / "art" / "storyboards" / "week-12"
APPROVED = ROOT / "art" / "final" / "series-endcards" / "approved"


def main() -> None:
    lettering = package.lettering
    lettering.WEEK_DIR = WEEK_DIR
    lettering.BOARD_DIR = BOARD_DIR
    lettering.ARC_TITLE = "THE MAXIMUM IS NOT THE MEANING"
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
        (78, 1, 1, "Dr. Price"): "left", (78, 1, 2, "Student"): "left", (78, 1, 3, "Dr. Price"): "left", (78, 2, 1, "Dr. Price"): "left", (78, 2, 2, "Nia"): "right", (78, 2, 3, "Dr. Price"): "left", (78, 2, 4, "Malik"): "right",
        (79, 1, 1, "Dr. Brooks"): "left", (79, 1, 2, "Nia"): "left", (79, 1, 3, "Malik"): "right", (79, 2, 1, "Keisha"): "left", (79, 2, 2, "Nia"): "right", (79, 2, 3, "Nia"): "right", (79, 2, 4, "Nia"): "right",
        (80, 1, 1, "Malik"): "right", (80, 1, 2, "Simone"): "left", (80, 1, 3, "Malik"): "right", (80, 1, 4, "Simone"): "left", (80, 2, 1, "Simone"): "left", (80, 2, 2, "Malik"): "right", (80, 2, 3, "Malik"): "right",
        (81, 1, 1, "Julian"): "right", (81, 1, 2, "Julian"): "right", (81, 1, 3, "Nia"): "left", (81, 2, 1, "Nia"): "left", (81, 2, 2, "Julian"): "right", (81, 2, 3, "Nia"): "left",
        (82, 1, 1, "Julian"): "right", (82, 1, 2, "Nia"): "left", (82, 1, 3, "Julian"): "right", (82, 2, 1, "Nia"): "left", (82, 2, 2, "Nia"): "left", (82, 2, 3, "Julian"): "right",
        (83, 1, 1, "Andre"): "left", (83, 1, 2, "Dr. Bennett"): "left", (83, 1, 3, "Malik"): "right", (83, 1, 4, "Simone"): "left", (83, 2, 1, "Malik"): "right",
        (84, 1, 2, "Nia"): "left", (84, 1, 3, "Malik"): "right", (84, 1, 4, "Nia"): "left", (84, 2, 1, "Nia"): "left", (84, 2, 2, "Malik"): "right", (84, 2, 3, "Nia"): "left",
    })
    for part, episode in enumerate(range(78, 85), start=1):
        episode_dir = WEEK_DIR / f"episode-{episode:02d}"
        sequence = episode_dir / "sequence-v2"
        sequence.mkdir(parents=True, exist_ok=True)
        lettering.make_title(part, sequence / "01-title-card-v1.png")
        for page in (1, 2):
            source = package.newest(list((episode_dir / "unlettered").glob(f"week-12-episode-{episode:02d}-page-{page:02d}-art-v*.png")))
            board = BOARD_DIR / f"week-12-episode-{episode:02d}-page-{page:02d}.md"
            output = episode_dir / f"week-12-episode-{episode:02d}-page-{page:02d}-lettered-v1.png"
            package.letter_page(source, board, output, episode, page)
            shutil.copy2(output, sequence / f"0{page + 1}-comic-page-{page:02d}-v1.png")
        end_card = lettering.END_CARDS[part - 1]
        shutil.copy2(APPROVED / end_card, sequence / f"04-{end_card}")
    print("Finished Week 12 title, lettering, page-mark, and end-card packages.")


if __name__ == "__main__":
    main()
