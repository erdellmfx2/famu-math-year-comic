#!/usr/bin/env python3
"""Package Week 4 with the established lettering and social-release system."""

from __future__ import annotations

import shutil
from pathlib import Path

import finish_week03_comic as lettering


ROOT = Path(__file__).resolve().parents[1]
WEEK_DIR = ROOT / "art" / "final" / "week-04"
BOARD_DIR = ROOT / "art" / "storyboards" / "week-04"
APPROVED = ROOT / "art" / "final" / "series-endcards" / "approved"


def newest(paths: list[Path]) -> Path:
    """Choose the latest accepted non-destructive art version."""
    if not paths:
        raise FileNotFoundError("Missing unlettered comic page")

    def version(path: Path) -> int:
        stem = path.stem
        marker = stem.rsplit("-v", 1)
        return int(marker[1]) if len(marker) == 2 and marker[1].isdigit() else 0

    return max(paths, key=version)


def restore_silent_panel(
    canvas: "lettering.Image.Image", source: "lettering.Image.Image", panel_index: int
) -> None:
    """Keep intentional silent beats as full-width art instead of empty text bands."""
    source_cell_height = source.height // 4
    output_cell_height = lettering.OUTPUT_HEIGHT // 4
    source_top = panel_index * source_cell_height
    source_bottom = source.height if panel_index == 3 else (panel_index + 1) * source_cell_height
    source_panel = source.crop((0, source_top, source.width, source_bottom))
    destination_size = (
        lettering.OUTPUT_WIDTH - lettering.PANEL_GUTTER * 2,
        output_cell_height - lettering.PANEL_GUTTER * 2,
    )
    panel = lettering.ImageOps.fit(
        source_panel, destination_size, method=lettering.Image.Resampling.LANCZOS
    )
    x = lettering.PANEL_GUTTER
    y = panel_index * output_cell_height + lettering.PANEL_GUTTER
    canvas.alpha_composite(panel, (x, y))
    lettering.ImageDraw.Draw(canvas).rectangle(
        (x, y, x + panel.width, y + panel.height), outline="#171717", width=3
    )


def letter_page(
    source: Path, board: Path, destination: Path, episode: int, page: int
) -> None:
    """Apply dialogue maps while preserving explicitly silent visual beats."""
    source_image = lettering.Image.open(source).convert("RGBA")
    letters_by_panel = lettering.panel_letters(board)
    image = lettering.build_face_clear_canvas(source_image)
    for panel_index, letters in enumerate(letters_by_panel):
        if not letters:
            restore_silent_panel(image, source_image, panel_index)

    draw = lettering.ImageDraw.Draw(image)
    for panel_index, letters in enumerate(letters_by_panel):
        lettering.letter_panel(
            draw,
            letters,
            lettering.panel_bounds(panel_index),
            episode,
            page,
            panel_index + 1,
        )

    mark = lettering.Image.open(lettering.PAGE_MARK).convert("RGBA")
    mark_size = max(72, int(min(lettering.OUTPUT_WIDTH, lettering.OUTPUT_HEIGHT) * 0.085))
    mark.thumbnail((mark_size, mark_size), lettering.Image.Resampling.LANCZOS)
    margin = max(14, int(min(lettering.OUTPUT_WIDTH, lettering.OUTPUT_HEIGHT) * 0.015))
    image.alpha_composite(
        mark,
        (lettering.OUTPUT_WIDTH - mark.width - margin, lettering.OUTPUT_HEIGHT - mark.height - margin),
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    metadata = lettering.PngInfo()
    metadata.add_text("dialogue_font", "Comic Sans MS Regular")
    metadata.add_text("speech_balloon", "organic oval with speaker-directed tail")
    metadata.add_text("caption_box", "#FFF4D6 pale cream, no tail")
    metadata.add_text("page_mark", lettering.PAGE_MARK.name)
    metadata.add_text("speaker_labels_printed", "false")
    metadata.add_text("face_clearance", "dedicated lettering band; no balloon over art")
    image.convert("RGB").save(destination, pnginfo=metadata)


def main() -> None:
    lettering.WEEK_DIR = WEEK_DIR
    lettering.BOARD_DIR = BOARD_DIR
    lettering.ARC_TITLE = "THE FIRST LIMIT"
    lettering.END_CARDS = [
        "thank-you-end-card-v1.png",
        "mathematics-invitation-end-card-v1.png",
        "famu-mathematics-attribution-end-card-v1.png",
        "thank-you-end-card-v1.png",
        "mathematics-invitation-end-card-v1.png",
        "famu-mathematics-attribution-end-card-v1.png",
        "thank-you-end-card-v1.png",
    ]

    for part, episode in enumerate(range(22, 29), start=1):
        episode_dir = WEEK_DIR / f"episode-{episode:02d}"
        sequence = episode_dir / "sequence-v2"
        sequence.mkdir(parents=True, exist_ok=True)
        lettering.make_title(part, sequence / "01-title-card-v1.png")

        for page in (1, 2):
            source = newest(
                list(
                    (episode_dir / "unlettered").glob(
                        f"week-04-episode-{episode:02d}-page-{page:02d}-art-v*.png"
                    )
                )
            )
            board = BOARD_DIR / f"week-04-episode-{episode:02d}-page-{page:02d}.md"
            output = episode_dir / f"week-04-episode-{episode:02d}-page-{page:02d}-lettered-v1.png"
            letter_page(source, board, output, episode, page)
            shutil.copy2(output, sequence / f"0{page + 1}-comic-page-{page:02d}-v1.png")

        end_card = lettering.END_CARDS[part - 1]
        shutil.copy2(APPROVED / end_card, sequence / f"04-{end_card}")

    print("Finished Week 4 title, lettering, page-mark, and end-card packages.")


if __name__ == "__main__":
    main()
