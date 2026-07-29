#!/usr/bin/env python3
"""Package Week 17 with face-safe lettering and social-release files."""

from __future__ import annotations

import shutil
from pathlib import Path

import finish_week04_comic as package


ROOT = Path(__file__).resolve().parents[1]
WEEK_DIR = ROOT / "art" / "final" / "week-17"
BOARD_DIR = ROOT / "art" / "storyboards" / "week-17"
APPROVED = ROOT / "art" / "final" / "series-endcards" / "approved"


def main() -> None:
    lettering = package.lettering
    lettering.WEEK_DIR = WEEK_DIR
    lettering.BOARD_DIR = BOARD_DIR
    lettering.ARC_TITLE = "THE CATCH AND THE QUIET AFTER"
    lettering.END_CARDS = [
        "thank-you-end-card-v1.png", "mathematics-invitation-end-card-v1.png",
        "famu-mathematics-attribution-end-card-v1.png", "thank-you-end-card-v1.png",
        "mathematics-invitation-end-card-v1.png", "famu-mathematics-attribution-end-card-v1.png",
        "thank-you-end-card-v1.png",
    ]
    lettering.SPEAKER_ANCHORS.update({
        (113, 1, 1, "Nia"): "left", (113, 1, 2, "Julian"): "right", (113, 1, 3, "Nia"): "left", (113, 2, 1, "Nia"): "right", (113, 2, 2, "Nia"): "right", (113, 2, 3, "Keisha"): "left", (113, 2, 4, "Nia"): "right",
        (114, 1, 3, "Malik"): "right", (114, 1, 4, "Simone"): "left", (114, 2, 1, "Malik"): "right", (114, 2, 2, "Simone"): "left",
        (116, 1, 2, "DJ"): "right", (116, 1, 3, "DJ"): "right", (116, 1, 4, "Mother"): "left", (116, 2, 1, "DJ"): "right", (116, 2, 2, "Mother"): "left", (116, 2, 3, "Mother"): "left", (116, 2, 4, "Malik"): "left",
        (117, 2, 1, "Nia"): "left", (117, 2, 2, "Julian"): "right", (117, 2, 3, "Julian"): "right",
        (118, 1, 2, "Marcel"): "left", (118, 1, 3, "Malik"): "right", (118, 2, 1, "Celeste"): "left", (118, 2, 2, "Malik"): "right", (118, 2, 3, "Malik"): "right",
        (119, 1, 1, "Nia"): "left", (119, 1, 2, "Malik"): "right", (119, 1, 3, "Nia"): "left", (119, 2, 1, "Nia"): "left", (119, 2, 2, "Malik"): "right",
    })
    for part, episode in enumerate(range(113, 120), start=1):
        episode_dir = WEEK_DIR / f"episode-{episode:02d}"
        sequence = episode_dir / "sequence-v2"
        sequence.mkdir(parents=True, exist_ok=True)
        lettering.make_title(part, sequence / "01-title-card-v1.png")
        for page in (1, 2):
            source = package.newest(list((episode_dir / "unlettered").glob(f"week-17-episode-{episode:02d}-page-{page:02d}-art-v*.png")))
            board = BOARD_DIR / f"week-17-episode-{episode:02d}-page-{page:02d}.md"
            output = episode_dir / f"week-17-episode-{episode:02d}-page-{page:02d}-lettered-v1.png"
            package.letter_page(source, board, output, episode, page)
            shutil.copy2(output, sequence / f"0{page + 1}-comic-page-{page:02d}-v1.png")
        end_card = lettering.END_CARDS[part - 1]
        shutil.copy2(APPROVED / end_card, sequence / f"04-{end_card}")
    print("Finished Week 17 title, lettering, page-mark, and end-card packages.")


if __name__ == "__main__":
    main()
