#!/usr/bin/env python3
"""Package Week 16 with face-safe lettering and social-release files."""

from __future__ import annotations

import shutil
from pathlib import Path

import finish_week04_comic as package


ROOT = Path(__file__).resolve().parents[1]
WEEK_DIR = ROOT / "art" / "final" / "week-16"
BOARD_DIR = ROOT / "art" / "storyboards" / "week-16"
APPROVED = ROOT / "art" / "final" / "series-endcards" / "approved"


def main() -> None:
    lettering = package.lettering
    lettering.WEEK_DIR = WEEK_DIR
    lettering.BOARD_DIR = BOARD_DIR
    lettering.ARC_TITLE = "TWO HONEST LOSSES"
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
        (106, 1, 2, "Julian"): "right", (106, 1, 3, "Nia"): "left", (106, 1, 4, "Julian"): "right", (106, 2, 1, "Nia"): "left", (106, 2, 2, "Julian"): "right", (106, 2, 4, "Nia"): "left",
        (107, 1, 2, "Julian"): "right", (107, 1, 3, "Nia"): "left", (107, 1, 4, "Julian"): "right", (107, 2, 1, "Julian"): "right", (107, 2, 2, "Nia"): "left", (107, 2, 3, "Nia"): "left",
        (108, 2, 3, "Nia"): "right", (108, 2, 4, "Keisha"): "left",
        (109, 1, 3, "Judge"): "left", (109, 2, 1, "Malik"): "right", (109, 2, 2, "Judge"): "left", (109, 2, 3, "Malik"): "right", (109, 2, 4, "Malik"): "right",
        (110, 1, 2, "Malik"): "right", (110, 1, 3, "Simone"): "left", (110, 1, 4, "Simone"): "left", (110, 2, 3, "Simone"): "left", (110, 2, 4, "Simone"): "left",
        (111, 1, 1, "Andre"): "left", (111, 1, 2, "Simone"): "left", (111, 1, 4, "Simone"): "left", (111, 2, 3, "Malik"): "right", (111, 2, 4, "Simone"): "left",
        (112, 1, 1, "Nia"): "left", (112, 1, 2, "Malik"): "right", (112, 1, 3, "Nia"): "left", (112, 1, 4, "Malik"): "right", (112, 2, 1, "Nia"): "left", (112, 2, 2, "Malik"): "right",
    })
    for part, episode in enumerate(range(106, 113), start=1):
        episode_dir = WEEK_DIR / f"episode-{episode:02d}"
        sequence = episode_dir / "sequence-v2"
        sequence.mkdir(parents=True, exist_ok=True)
        lettering.make_title(part, sequence / "01-title-card-v1.png")
        for page in (1, 2):
            source = package.newest(list((episode_dir / "unlettered").glob(f"week-16-episode-{episode:02d}-page-{page:02d}-art-v*.png")))
            board = BOARD_DIR / f"week-16-episode-{episode:02d}-page-{page:02d}.md"
            output = episode_dir / f"week-16-episode-{episode:02d}-page-{page:02d}-lettered-v1.png"
            package.letter_page(source, board, output, episode, page)
            shutil.copy2(output, sequence / f"0{page + 1}-comic-page-{page:02d}-v1.png")
        end_card = lettering.END_CARDS[part - 1]
        shutil.copy2(APPROVED / end_card, sequence / f"04-{end_card}")
    print("Finished Week 16 title, lettering, page-mark, and end-card packages.")


if __name__ == "__main__":
    main()
