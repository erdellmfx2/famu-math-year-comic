#!/usr/bin/env python3
"""Render Week 2 with the approved Week 1 title and lettering system."""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
from PIL.PngImagePlugin import PngInfo


ROOT = Path(__file__).resolve().parents[1]
WEEK_DIR = ROOT / "art" / "final" / "week-02"
BOARD_DIR = ROOT / "art" / "storyboards" / "week-02"
APPROVED = ROOT / "art" / "final" / "series-endcards" / "approved"
TITLE_BASE = APPROVED / "formula-of-becoming-series-logo-v1.png"
PAGE_MARK = APPROVED / "formula-of-becoming-famu-math-page-mark-v1.png"

COMIC_FONT = Path("/System/Library/Fonts/Supplemental/Comic Sans MS.ttf")
TITLE_FONT = Path("/System/Library/Fonts/Supplemental/Georgia Bold.ttf")
TITLE_SANS = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")

ARC_TITLE = "THE SHAPE OF AN INVITATION"
OUTPUT_WIDTH = 1024
OUTPUT_HEIGHT = 1820
LETTERING_BAND = 270
END_CARDS = [
    "thank-you-end-card-v1.png",
    "mathematics-invitation-end-card-v1.png",
    "famu-mathematics-attribution-end-card-v1.png",
    "thank-you-end-card-v1.png",
    "mathematics-invitation-end-card-v1.png",
    "famu-mathematics-attribution-end-card-v1.png",
    "thank-you-end-card-v1.png",
]

# Horizontal speaker positions in the accepted v2 art. These keep balloon tails
# attached to the correct character instead of relying on a generic alternation.
SPEAKER_ANCHORS = {
    (8, 1, 1, "Julian"): "right", (8, 1, 1, "Nia"): "left",
    (8, 1, 2, "Julian"): "center",
    (8, 1, 3, "Julian"): "right", (8, 1, 3, "Nia"): "left",
    (8, 1, 4, "Julian"): "left", (8, 1, 4, "Nia"): "right",
    (8, 2, 1, "Nia"): "left", (8, 2, 1, "Julian"): "right",
    (8, 2, 2, "Nia"): "left", (8, 2, 2, "Julian"): "right",
    (8, 2, 3, "Julian"): "right",
    (8, 2, 4, "Julian"): "left", (8, 2, 4, "Nia"): "right",
    (9, 1, 1, "Dr. Bennett"): "center", (9, 1, 2, "Dr. Bennett"): "right",
    (9, 1, 4, "Simone"): "center",
    (9, 2, 1, "Simone"): "left", (9, 2, 1, "Malik"): "right",
    (9, 2, 2, "Simone"): "left", (9, 2, 2, "Malik"): "right",
    (9, 2, 3, "Malik"): "center", (9, 2, 4, "Simone"): "left",
    (10, 1, 2, "Nia"): "right", (10, 1, 2, "Malik"): "left",
    (10, 1, 3, "Nia"): "center",
    (10, 1, 4, "Malik"): "left", (10, 1, 4, "Nia"): "right",
    (10, 2, 1, "Malik"): "left", (10, 2, 1, "Nia"): "right",
    (10, 2, 2, "Dr. Brooks"): "center",
    (10, 2, 3, "Malik"): "left", (10, 2, 3, "Nia"): "right",
    (10, 2, 4, "Nia"): "left", (10, 2, 4, "Malik"): "right",
    (11, 1, 1, "Julian"): "left", (11, 1, 1, "Nia"): "right",
    (11, 1, 2, "Julian"): "left", (11, 1, 2, "Nia"): "right",
    (11, 1, 3, "Julian"): "left", (11, 1, 3, "Nia"): "right",
    (12, 1, 1, "DJ"): "right",
    (12, 1, 2, "DJ"): "right",
    (12, 1, 3, "DJ"): "left",
    (12, 1, 4, "Malik"): "right", (12, 1, 4, "DJ"): "left",
    (12, 2, 1, "DJ"): "right", (12, 2, 1, "Malik"): "left",
    (12, 2, 2, "DJ"): "right", (12, 2, 2, "Malik"): "left",
    (12, 2, 3, "DJ"): "right", (12, 2, 3, "Malik"): "left",
    (12, 2, 4, "DJ"): "right", (12, 2, 4, "Malik"): "left",
    (13, 1, 3, "Julian"): "left", (13, 1, 3, "Nia"): "right",
    (13, 1, 4, "Julian"): "left",
    (13, 2, 1, "Julian"): "left",
    (13, 2, 3, "Nia"): "left", (13, 2, 3, "Julian"): "right",
    (13, 2, 4, "Julian"): "left",
    (14, 1, 1, "Nia"): "left",
    (14, 1, 2, "Malik"): "left",
    (14, 1, 3, "Nia"): "left", (14, 1, 3, "Malik"): "right",
    (14, 1, 4, "Malik"): "left", (14, 1, 4, "Nia"): "right",
    (14, 2, 1, "Malik"): "left", (14, 2, 1, "Nia"): "right",
    (14, 2, 2, "Malik"): "left",
}


@dataclass(frozen=True)
class Letter:
    speaker: str
    text: str

    @property
    def kind(self) -> str:
        if self.speaker == "Caption":
            return "caption"
        if "(text)" in self.speaker:
            return "message"
        return "speech"


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def panel_letters(board: Path) -> list[list[Letter]]:
    """Extract exact panel text while retaining its semantic box type."""
    source = board.read_text(encoding="utf-8")
    section = source.split("## Panels", 1)[1].split("## Art Rules", 1)[0]
    raw_panels = re.split(r"\n(?=\d+\. )", section.strip())
    output: list[list[Letter]] = []
    for raw in raw_panels:
        matches = re.findall(r"\*\*([^*]+):\*\* `([^`]+)`", raw)
        output.append([Letter(speaker.strip(), words) for speaker, words in matches])
    if len(output) != 4:
        raise ValueError(f"Expected four panels in {board.name}, found {len(output)}")
    return output


def wrap(
    draw: ImageDraw.ImageDraw,
    value: str,
    active_font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    words = value.split()
    lines: list[str] = []
    line = ""
    for word in words:
        trial = f"{line} {word}".strip()
        if not line or draw.textbbox((0, 0), trial, font=active_font)[2] <= max_width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def fit_text(
    draw: ImageDraw.ImageDraw, value: str, max_width: int, max_height: int
) -> tuple[ImageFont.FreeTypeFont, list[str], int]:
    for size in range(27, 13, -1):
        active_font = font(COMIC_FONT, size)
        lines = wrap(draw, value, active_font, max_width)
        line_height = size + 5
        if len(lines) * line_height <= max_height:
            return active_font, lines, line_height
    active_font = font(COMIC_FONT, 13)
    return active_font, wrap(draw, value, active_font, max_width), 18


def draw_centered_lines(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    active_font: ImageFont.FreeTypeFont,
    line_height: int,
    box: tuple[int, int, int, int],
) -> None:
    left, top, right, bottom = box
    y = top + ((bottom - top) - len(lines) * line_height) / 2
    for line in lines:
        bounds = draw.textbbox((0, 0), line, font=active_font)
        text_width = bounds[2] - bounds[0]
        draw.text(
            (left + ((right - left) - text_width) / 2, y),
            line,
            font=active_font,
            fill="#171717",
        )
        y += line_height


def draw_caption(
    draw: ImageDraw.ImageDraw,
    text: str,
    box: tuple[int, int, int, int],
) -> None:
    left, top, right, bottom = box
    draw.rounded_rectangle(
        box, radius=7, fill="#FFF4D6", outline="#171717", width=3
    )
    active_font, lines, line_height = fit_text(
        draw, text, right - left - 28, bottom - top - 20
    )
    draw_centered_lines(draw, lines, active_font, line_height, box)


def draw_message(
    draw: ImageDraw.ImageDraw,
    text: str,
    box: tuple[int, int, int, int],
) -> None:
    left, top, right, bottom = box
    draw.rounded_rectangle(
        box, radius=20, fill="#EAF2F7", outline="#171717", width=3
    )
    active_font, lines, line_height = fit_text(
        draw, text, right - left - 28, bottom - top - 20
    )
    draw_centered_lines(draw, lines, active_font, line_height, box)


def draw_speech(
    draw: ImageDraw.ImageDraw,
    text: str,
    box: tuple[int, int, int, int],
    target: tuple[int, int],
) -> None:
    """Draw a Week 1-style oval balloon with a visible speaker-directed tail."""
    left, top, right, bottom = box
    tail_x = max(left + 30, min(target[0], right - 30))
    tail_base_y = bottom - 8
    target_x, target_y = target
    tail = [
        (tail_x - 18, tail_base_y),
        (tail_x + 18, tail_base_y),
        (target_x, target_y),
    ]
    draw.polygon(tail, fill="#FFFFFF", outline="#171717")
    draw.ellipse(box, fill="#FFFFFF", outline="#171717", width=3)
    active_font, lines, line_height = fit_text(
        draw, text, right - left - 58, bottom - top - 58
    )
    draw_centered_lines(draw, lines, active_font, line_height, box)


def panel_bounds(width: int, height: int, panel_index: int) -> tuple[int, int, int, int]:
    column = panel_index % 2
    row = panel_index // 2
    gutter = max(8, width // 120)
    panel_width = width // 2
    panel_height = height // 2
    left = column * panel_width + gutter
    top = row * panel_height + gutter
    right = (column + 1) * panel_width - gutter
    bottom = (row + 1) * panel_height - gutter
    return left, top, right, bottom


def build_face_clear_canvas(
    source: Image.Image, letters_by_panel: list[list[Letter]]
) -> Image.Image:
    """Reserve a dedicated lettering band so no balloon can cover a face."""
    output = Image.new("RGBA", (OUTPUT_WIDTH, OUTPUT_HEIGHT), "#FFFFFF")
    draw = ImageDraw.Draw(output)
    source_width, source_height = source.size
    source_cell_width = source_width // 2
    source_cell_height = source_height // 2
    output_cell_width = OUTPUT_WIDTH // 2
    output_cell_height = OUTPUT_HEIGHT // 2
    gutter = 7

    for panel_index, _letters in enumerate(letters_by_panel):
        column = panel_index % 2
        row = panel_index // 2
        source_box = (
            column * source_cell_width,
            row * source_cell_height,
            (column + 1) * source_cell_width,
            (row + 1) * source_cell_height,
        )
        panel = source.crop(source_box)
        art_area = (
            output_cell_width - gutter * 2,
            output_cell_height - LETTERING_BAND - gutter * 2,
        )
        panel = ImageOps.contain(panel, art_area, Image.Resampling.LANCZOS)

        cell_left = column * output_cell_width
        cell_top = row * output_cell_height
        cell_right = cell_left + output_cell_width
        cell_bottom = cell_top + output_cell_height
        draw.rectangle(
            (
                cell_left + gutter,
                cell_top + gutter,
                cell_right - gutter,
                cell_top + LETTERING_BAND,
            ),
            fill="#F7F1E3",
        )
        art_x = cell_left + (output_cell_width - panel.width) // 2
        art_y = cell_top + LETTERING_BAND + (
            output_cell_height - LETTERING_BAND - panel.height
        ) // 2
        output.alpha_composite(panel, (art_x, art_y))
        draw.rectangle(
            (
                cell_left + gutter,
                cell_top + gutter,
                cell_right - gutter,
                cell_bottom - gutter,
            ),
            outline="#171717",
            width=3,
        )
        draw.line(
            (
                cell_left + gutter,
                cell_top + LETTERING_BAND,
                cell_right - gutter,
                cell_top + LETTERING_BAND,
            ),
            fill="#171717",
            width=2,
        )
    return output


def letter_panel(
    draw: ImageDraw.ImageDraw,
    letters: list[Letter],
    bounds: tuple[int, int, int, int],
    episode: int,
    page: int,
    panel_number: int,
) -> None:
    if not letters:
        return
    left, top, right, bottom = bounds
    panel_width = right - left
    panel_height = bottom - top
    gap = 8
    count = len(letters)
    all_speech = all(letter.kind == "speech" for letter in letters)

    if count == 1:
        box_width = int(panel_width * 0.86)
        text_length = len(letters[0].text)
        box_height = min(
            int(panel_height * 0.36),
            max(130, min(235, 115 + text_length // 2)),
        )
        boxes = [
            (
                left + (panel_width - box_width) // 2,
                top + 14,
                left + (panel_width + box_width) // 2,
                top + 14 + box_height,
            )
        ]
    elif all_speech:
        box_width = (panel_width - gap * 3) // 2
        box_height = min(
            int(panel_height * (0.22 if count > 2 else 0.25)),
            112 if count > 2 else 175,
        )
        boxes = []
        for index, item in enumerate(letters):
            speaker_name = item.speaker.split(" (", 1)[0]
            side = SPEAKER_ANCHORS.get(
                (episode, page, panel_number, speaker_name),
                "left" if index % 2 == 0 else "right",
            )
            if side == "right":
                x = right - gap - box_width
            elif side == "center":
                x = left + (panel_width - box_width) // 2
            else:
                x = left + gap
            if count == 2:
                y = top + 12 + index * 78
            else:
                y = top + 12 + (index // 2) * (box_height + gap)
            boxes.append((x, y, x + box_width, y + box_height))
    elif count == 2:
        box_width = (panel_width - gap * 3) // 2
        box_height = min(int(panel_height * 0.27), 200)
        boxes = [
            (left + gap, top + 14, left + gap + box_width, top + 14 + box_height),
            (
                left + gap * 2 + box_width,
                top + 14,
                right - gap,
                top + 14 + box_height,
            ),
        ]
    else:
        columns = 2
        rows = (count + 1) // 2
        box_width = (panel_width - gap * 3) // columns
        box_height = min(int(panel_height * 0.20), 155)
        boxes = []
        for index in range(count):
            column = index % 2
            row = index // 2
            x = left + gap + column * (box_width + gap)
            y = top + 12 + row * (box_height + gap)
            boxes.append((x, y, x + box_width, y + box_height))

    speech_index = 0
    speech_total = sum(letter.kind == "speech" for letter in letters)
    for item, box in zip(letters, boxes, strict=True):
        if item.kind == "caption":
            draw_caption(draw, item.text, box)
        elif item.kind == "message":
            draw_message(draw, item.text, box)
        else:
            speaker_name = item.speaker.split(" (", 1)[0]
            side = SPEAKER_ANCHORS.get(
                (episode, page, panel_number, speaker_name),
                "center" if speech_total == 1 else (
                    "left" if speech_index % 2 == 0 else "right"
                ),
            )
            fractions = {"left": 0.28, "center": 0.5, "right": 0.72}
            target_x = left + int(panel_width * fractions[side])
            target_y = top + int(panel_height * (0.40 + 0.05 * (speech_index // 2)))
            draw_speech(draw, item.text, box, (target_x, target_y))
            speech_index += 1


def make_title(part: int, destination: Path) -> None:
    image = Image.open(TITLE_BASE).convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size
    navy = "#061A31"
    copper = "#C77A44"
    cream = "#F4E4C7"

    # Preserve the approved growing-leaf logo and clear only its lower safe area.
    draw.rectangle((45, 1605, width - 45, 1765), fill=navy)
    draw.line((110, 1607, width - 110, 1607), fill=copper, width=2)

    def centered(text: str, y: int, active_font: ImageFont.FreeTypeFont, fill: str) -> None:
        text_box = draw.textbbox((0, 0), text, font=active_font)
        draw.text(
            ((width - (text_box[2] - text_box[0])) / 2, y),
            text,
            font=active_font,
            fill=fill,
        )

    centered(ARC_TITLE, 1625, font(TITLE_FONT, 30), cream)
    centered(f"PART {part}", 1680, font(TITLE_FONT, 29), copper)
    centered("FAMU MATHEMATICS", 1730, font(TITLE_SANS, 15), copper)
    destination.parent.mkdir(parents=True, exist_ok=True)
    metadata = PngInfo()
    metadata.add_text("series_title_base", TITLE_BASE.name)
    metadata.add_text("arc_title", ARC_TITLE)
    metadata.add_text("part", str(part))
    metadata.add_text("growing_leaf_preserved", "true")
    image.save(destination, pnginfo=metadata)


def letter_page(
    source: Path, board: Path, destination: Path, episode: int, page: int
) -> None:
    source_image = Image.open(source).convert("RGBA")
    letters_by_panel = panel_letters(board)
    image = build_face_clear_canvas(source_image, letters_by_panel)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    for panel_index, letters in enumerate(letters_by_panel):
        letter_panel(
            draw,
            letters,
            panel_bounds(width, height, panel_index),
            episode,
            page,
            panel_index + 1,
        )

    mark = Image.open(PAGE_MARK).convert("RGBA")
    mark_size = max(72, int(min(width, height) * 0.085))
    mark.thumbnail((mark_size, mark_size), Image.Resampling.LANCZOS)
    margin = max(14, int(min(width, height) * 0.015))
    image.alpha_composite(mark, (width - mark.width - margin, height - mark.height - margin))
    destination.parent.mkdir(parents=True, exist_ok=True)
    metadata = PngInfo()
    metadata.add_text("dialogue_font", "Comic Sans MS Regular")
    metadata.add_text("speech_balloon", "organic oval with speaker-directed tail")
    metadata.add_text("caption_box", "#FFF4D6 pale cream, no tail")
    metadata.add_text("page_mark", PAGE_MARK.name)
    metadata.add_text("speaker_labels_printed", "false")
    metadata.add_text("face_clearance", "dedicated lettering band; no balloon over art")
    image.convert("RGB").save(destination, pnginfo=metadata)


def main() -> None:
    for day_index, episode in enumerate(range(8, 15), start=1):
        episode_dir = WEEK_DIR / f"episode-{episode:02d}"
        sequence = episode_dir / "sequence-v2"
        sequence.mkdir(parents=True, exist_ok=True)
        make_title(day_index, sequence / "01-title-card-v2.png")
        for page in (1, 2):
            source = (
                episode_dir
                / "unlettered"
                / f"week-02-episode-{episode:02d}-page-{page:02d}-art-v2.png"
            )
            board = BOARD_DIR / f"week-02-episode-{episode:02d}-page-{page:02d}.md"
            finished = (
                episode_dir
                / f"week-02-episode-{episode:02d}-page-{page:02d}-lettered-v3.png"
            )
            letter_page(source, board, finished, episode, page)
            shutil.copy2(
                finished, sequence / f"0{page + 1}-comic-page-{page:02d}-v3.png"
            )
        shutil.copy2(
            APPROVED / END_CARDS[day_index - 1],
            sequence / f"04-{END_CARDS[day_index - 1]}",
        )
    print("Finished Week 2 v3 face-clear release packages with Parts 1-7.")


if __name__ == "__main__":
    main()
