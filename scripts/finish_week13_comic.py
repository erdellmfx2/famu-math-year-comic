#!/usr/bin/env python3
"""Package Week 13 with face-safe lettering and social-release files."""

from __future__ import annotations

import shutil
from pathlib import Path

import finish_week04_comic as package


ROOT = Path(__file__).resolve().parents[1]
WEEK_DIR = ROOT / "art" / "final" / "week-13"
BOARD_DIR = ROOT / "art" / "storyboards" / "week-13"
APPROVED = ROOT / "art" / "final" / "series-endcards" / "approved"


def main() -> None:
    lettering = package.lettering
    lettering.WEEK_DIR = WEEK_DIR
    lettering.BOARD_DIR = BOARD_DIR
    lettering.ARC_TITLE = "BEYOND THE CAMPUS MAP"
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
        (85, 1, 2, "Malik"): "right", (85, 1, 3, "Marcel"): "left", (85, 2, 2, "Ms. Alvarez"): "left", (85, 2, 3, "Malik"): "right",
        (86, 1, 1, "Dr. Brooks"): "left", (86, 1, 2, "Amara"): "left", (86, 1, 3, "Nia"): "right", (86, 2, 2, "Nia"): "left", (86, 2, 3, "Nia"): "left",
        (87, 1, 2, "Nia"): "left", (88, 1, 2, "Nia"): "right", (88, 1, 3, "Dr. Vega"): "left", (88, 1, 4, "Dr. Vega"): "left", (88, 2, 1, "Malik"): "right", (88, 2, 2, "Dr. Vega"): "left", (88, 2, 3, "Malik"): "right",
        (89, 1, 1, "Dr. Washington"): "left", (89, 1, 3, "Malik"): "right", (89, 2, 1, "Dr. Washington"): "left", (89, 2, 2, "Dr. Washington"): "left", (89, 2, 3, "Dr. Washington"): "left",
        (90, 1, 1, "Nia"): "left", (90, 1, 2, "Malik"): "right", (90, 1, 3, "Nia"): "left", (90, 1, 4, "Malik"): "right",
        (91, 1, 1, "Julian"): "right", (91, 1, 2, "Nia"): "left", (91, 1, 3, "Julian"): "right", (91, 1, 4, "Nia"): "left", (91, 2, 1, "Julian"): "right", (91, 2, 2, "Julian"): "right", (91, 2, 3, "Nia"): "left", (91, 2, 4, "Julian"): "right",
    })
    for part, episode in enumerate(range(85, 92), start=1):
        episode_dir = WEEK_DIR / f"episode-{episode:02d}"
        sequence = episode_dir / "sequence-v2"
        sequence.mkdir(parents=True, exist_ok=True)
        lettering.make_title(part, sequence / "01-title-card-v1.png")
        for page in (1, 2):
            source = package.newest(list((episode_dir / "unlettered").glob(f"week-13-episode-{episode:02d}-page-{page:02d}-art-v*.png")))
            board = BOARD_DIR / f"week-13-episode-{episode:02d}-page-{page:02d}.md"
            output = episode_dir / f"week-13-episode-{episode:02d}-page-{page:02d}-lettered-v1.png"
            package.letter_page(source, board, output, episode, page)
            shutil.copy2(output, sequence / f"0{page + 1}-comic-page-{page:02d}-v1.png")
        end_card = lettering.END_CARDS[part - 1]
        shutil.copy2(APPROVED / end_card, sequence / f"04-{end_card}")
    print("Finished Week 13 title, lettering, page-mark, and end-card packages.")


if __name__ == "__main__":
    main()
