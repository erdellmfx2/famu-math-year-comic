#!/usr/bin/env python3
"""Package Week 14 with face-safe lettering and social-release files."""

from __future__ import annotations

import shutil
from pathlib import Path

import finish_week04_comic as package


ROOT = Path(__file__).resolve().parents[1]
WEEK_DIR = ROOT / "art" / "final" / "week-14"
BOARD_DIR = ROOT / "art" / "storyboards" / "week-14"
APPROVED = ROOT / "art" / "final" / "series-endcards" / "approved"


def main() -> None:
    lettering = package.lettering
    lettering.WEEK_DIR = WEEK_DIR
    lettering.BOARD_DIR = BOARD_DIR
    lettering.ARC_TITLE = "RIEMANN SUMS AND MISSING PIECES"
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
        (92, 1, 1, "Nia"): "left", (92, 1, 2, "Zoe"): "left", (92, 1, 3, "Nia"): "left", (92, 2, 1, "Nia"): "left", (92, 2, 3, "Nia"): "left", (92, 2, 4, "Malik"): "right",
        (93, 1, 2, "Zoe"): "left", (93, 1, 3, "Julian"): "right", (93, 1, 4, "Nia"): "left", (93, 2, 2, "Julian"): "right", (93, 2, 3, "Nia"): "left", (93, 2, 4, "Malik"): "right",
        (94, 1, 1, "Malik"): "left", (94, 1, 2, "Julian"): "right", (94, 1, 3, "Malik"): "left", (94, 1, 4, "Malik"): "left", (94, 2, 1, "Malik"): "left", (94, 2, 2, "Malik"): "left", (94, 2, 3, "Julian"): "right", (94, 2, 4, "Malik"): "left",
        (95, 1, 2, "Coach"): "left", (95, 2, 4, "DJ"): "right",
        (96, 1, 4, "Simone"): "left", (96, 2, 3, "Malik"): "right", (96, 2, 4, "Simone"): "left",
        (97, 1, 2, "Marcus"): "right", (97, 1, 3, "Julian"): "right", (97, 1, 4, "Nia"): "left", (97, 2, 1, "Nia"): "left", (97, 2, 2, "Julian"): "right", (97, 2, 3, "Nia"): "left",
        (98, 1, 1, "Keisha"): "left", (98, 1, 2, "Nia"): "right", (98, 1, 3, "Nia"): "right", (98, 1, 4, "Keisha"): "left", (98, 2, 1, "Nia"): "right", (98, 2, 2, "Nia"): "right", (98, 2, 3, "Keisha"): "left", (98, 2, 4, "Nia"): "right",
    })
    for part, episode in enumerate(range(92, 99), start=1):
        episode_dir = WEEK_DIR / f"episode-{episode:02d}"
        sequence = episode_dir / "sequence-v2"
        sequence.mkdir(parents=True, exist_ok=True)
        lettering.make_title(part, sequence / "01-title-card-v1.png")
        for page in (1, 2):
            source = package.newest(list((episode_dir / "unlettered").glob(f"week-14-episode-{episode:02d}-page-{page:02d}-art-v*.png")))
            board = BOARD_DIR / f"week-14-episode-{episode:02d}-page-{page:02d}.md"
            output = episode_dir / f"week-14-episode-{episode:02d}-page-{page:02d}-lettered-v1.png"
            package.letter_page(source, board, output, episode, page)
            shutil.copy2(output, sequence / f"0{page + 1}-comic-page-{page:02d}-v1.png")
        end_card = lettering.END_CARDS[part - 1]
        shutil.copy2(APPROVED / end_card, sequence / f"04-{end_card}")
    print("Finished Week 14 title, lettering, page-mark, and end-card packages.")


if __name__ == "__main__":
    main()
