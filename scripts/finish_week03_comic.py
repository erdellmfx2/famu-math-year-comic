#!/usr/bin/env python3
"""Render Week 3 with the approved title, lettering, and page-mark system."""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps
from PIL.PngImagePlugin import PngInfo


ROOT = Path(__file__).resolve().parents[1]
WEEK_DIR = ROOT / "art" / "final" / "week-03"
BOARD_DIR = ROOT / "art" / "storyboards" / "week-03"
APPROVED = ROOT / "art" / "final" / "series-endcards" / "approved"
TITLE_BASE = APPROVED / "formula-of-becoming-series-logo-v1.png"
PAGE_MARK = APPROVED / "formula-of-becoming-famu-math-page-mark-v1.png"

COMIC_FONT = Path("/System/Library/Fonts/Supplemental/Comic Sans MS.ttf")
TITLE_FONT = Path("/System/Library/Fonts/Supplemental/Georgia Bold.ttf")
TITLE_SANS = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")

ARC_TITLE = "ROOMS, RULES, AND FIRST IMPRESSIONS"
OUTPUT_WIDTH = 1024
OUTPUT_HEIGHT = 1820
LETTERING_BAND = 190
PANEL_GUTTER = 7
END_CARDS = [
    "thank-you-end-card-v1.png",
    "mathematics-invitation-end-card-v1.png",
    "famu-mathematics-attribution-end-card-v1.png",
    "thank-you-end-card-v1.png",
    "mathematics-invitation-end-card-v1.png",
    "famu-mathematics-attribution-end-card-v1.png",
    "thank-you-end-card-v1.png",
]

DEFAULT_SIDES = {
    "Malik": "left",
    "Nia": "right",
    "DJ": "center",
    "Keisha": "right",
    "Julian": "left",
    "Simone": "left",
    "Tasha": "right",
}

SPEAKER_ANCHORS = {
    (15, 1, 3, "Malik"): "left",
    (15, 1, 3, "DJ"): "right",
    (15, 2, 1, "Malik"): "left",
    (15, 2, 1, "DJ"): "right",
    (15, 2, 2, "Malik"): "left",
    (15, 2, 2, "DJ"): "right",
    (16, 1, 2, "Keisha"): "right",
    (16, 1, 2, "Nia"): "left",
    (16, 1, 3, "Nia"): "left",
    (16, 1, 3, "Keisha"): "right",
    (16, 1, 4, "Nia"): "left",
    (16, 1, 4, "Keisha"): "right",
    (16, 2, 1, "Keisha"): "right",
    (16, 2, 1, "Nia"): "left",
    (16, 2, 4, "Keisha"): "right",
    (16, 2, 4, "Nia"): "left",
    (17, 2, 3, "Malik"): "left",
    (17, 2, 3, "Nia"): "right",
    (17, 2, 4, "Malik"): "left",
    (17, 2, 4, "Nia"): "right",
    (18, 2, 3, "Malik"): "left",
    (18, 2, 3, "Nia"): "right",
    (18, 2, 4, "Malik"): "left",
    (18, 2, 4, "Nia"): "right",
    (19, 2, 2, "Julian"): "left",
    (19, 2, 2, "Nia"): "right",
    (20, 2, 1, "Simone"): "left",
    (20, 2, 1, "Malik"): "right",
    (20, 2, 2, "Simone"): "left",
    (20, 2, 2, "Malik"): "right",
    (20, 2, 3, "Simone"): "left",
    (20, 2, 3, "Malik"): "right",
    (20, 2, 4, "Simone"): "left",
    (20, 2, 4, "Malik"): "right",
    (21, 1, 3, "Malik"): "left",
    (21, 1, 3, "DJ"): "center",
    (21, 1, 3, "Nia"): "right",
    (21, 1, 3, "Keisha"): "right",
    (21, 2, 2, "Julian"): "left",
    (21, 2, 2, "Malik"): "right",
}


@dataclass(frozen=True)
class Letter:
    speaker: str
    text: str

    @property
    def kind(self) -> str:
        return "caption" if self.speaker == "Caption" else "speech"


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def panel_letters(board: Path) -> list[list[Letter]]:
    source = board.read_text(encoding="utf-8")
    section = source.split("## Panel Plan", 1)[1].split("## Pass-One Art Rules", 1)[0]
    raw_panels = re.split(r"\n(?=### Panel \d+:)", section.strip())
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
    lines: list[str] = []
    line = ""
    for word in value.split():
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
    draw: ImageDraw.ImageDraw,
    value: str,
    max_width: int,
    max_height: int,
    maximum: int = 27,
) -> tuple[ImageFont.FreeTypeFont, list[str], int]:
    for size in range(maximum, 12, -1):
        active_font = font(COMIC_FONT, size)
        lines = wrap(draw, value, active_font, max_width)
        line_height = size + 4
        if len(lines) * line_height <= max_height:
            return active_font, lines, line_height
    active_font = font(COMIC_FONT, 12)
    return active_font, wrap(draw, value, active_font, max_width), 16


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
        draw, text, right - left - 24, bottom - top - 16, maximum=25
    )
    draw_centered_lines(draw, lines, active_font, line_height, box)


def draw_speech(
    draw: ImageDraw.ImageDraw,
    text: str,
    box: tuple[int, int, int, int],
    target: tuple[int, int],
) -> None:
    left, top, right, bottom = box
    tail_x = max(left + 24, min(target[0], right - 24))
    tail = [
        (tail_x - 16, bottom - 7),
        (tail_x + 16, bottom - 7),
        target,
    ]
    draw.polygon(tail, fill="#FFFFFF", outline="#171717")
    draw.ellipse(box, fill="#FFFFFF", outline="#171717", width=3)
    active_font, lines, line_height = fit_text(
        draw, text, right - left - 46, bottom - top - 36, maximum=25
    )
    draw_centered_lines(draw, lines, active_font, line_height, box)


def panel_bounds(panel_index: int) -> tuple[int, int, int, int]:
    cell_height = OUTPUT_HEIGHT // 4
    top = panel_index * cell_height + PANEL_GUTTER
    bottom = (panel_index + 1) * cell_height - PANEL_GUTTER
    return PANEL_GUTTER, top, OUTPUT_WIDTH - PANEL_GUTTER, bottom


def build_face_clear_canvas(source: Image.Image) -> Image.Image:
    output = Image.new("RGBA", (OUTPUT_WIDTH, OUTPUT_HEIGHT), "#FFFFFF")
    draw = ImageDraw.Draw(output)
    source_width, source_height = source.size
    source_cell_height = source_height // 4
    output_cell_height = OUTPUT_HEIGHT // 4

    for panel_index in range(4):
        source_top = panel_index * source_cell_height
        source_bottom = (
            source_height if panel_index == 3 else (panel_index + 1) * source_cell_height
        )
        original_band = int(source_cell_height * 0.14)
        panel = source.crop(
            (0, source_top + original_band, source_width, source_bottom)
        )
        art_area = (
            OUTPUT_WIDTH - PANEL_GUTTER * 2,
            output_cell_height - LETTERING_BAND - PANEL_GUTTER * 2,
        )
        panel = ImageOps.contain(panel, art_area, Image.Resampling.LANCZOS)

        cell_top = panel_index * output_cell_height
        cell_bottom = cell_top + output_cell_height
        draw.rectangle(
            (
                PANEL_GUTTER,
                cell_top + PANEL_GUTTER,
                OUTPUT_WIDTH - PANEL_GUTTER,
                cell_top + LETTERING_BAND,
            ),
            fill="#F7F1E3",
        )
        art_x = (OUTPUT_WIDTH - panel.width) // 2
        art_y = cell_top + LETTERING_BAND + (
            output_cell_height - LETTERING_BAND - panel.height
        ) // 2
        output.alpha_composite(panel, (art_x, art_y))
        draw.rectangle(
            (
                PANEL_GUTTER,
                cell_top + PANEL_GUTTER,
                OUTPUT_WIDTH - PANEL_GUTTER,
                cell_bottom - PANEL_GUTTER,
            ),
            outline="#171717",
            width=3,
        )
        draw.line(
            (
                PANEL_GUTTER,
                cell_top + LETTERING_BAND,
                OUTPUT_WIDTH - PANEL_GUTTER,
                cell_top + LETTERING_BAND,
            ),
            fill="#171717",
            width=2,
        )
    return output


def speaker_side(
    episode: int, page: int, panel_number: int, speaker: str, index: int
) -> str:
    return SPEAKER_ANCHORS.get(
        (episode, page, panel_number, speaker),
        DEFAULT_SIDES.get(speaker, "left" if index % 2 == 0 else "right"),
    )


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
    left, top, right, _bottom = bounds
    band_bottom = top + LETTERING_BAND - 10
    gap = 7
    count = len(letters)

    if count == 1:
        boxes = [(left + 28, top + 10, right - 28, band_bottom)]
    elif count == 2:
        box_width = (right - left - gap * 3) // 2
        boxes = [
            (left + gap, top + 9, left + gap + box_width, band_bottom),
            (left + gap * 2 + box_width, top + 9, right - gap, band_bottom),
        ]
    else:
        rows = 2
        columns = (count + 1) // rows
        box_width = (right - left - gap * (columns + 1)) // columns
        box_height = (band_bottom - top - gap * 3) // rows
        boxes = []
        for index in range(count):
            row = index // columns
            column = index % columns
            x = left + gap + column * (box_width + gap)
            y = top + gap + row * (box_height + gap)
            boxes.append((x, y, x + box_width, y + box_height))

    speech_index = 0
    for item, box in zip(letters, boxes, strict=True):
        if item.kind == "caption":
            draw_caption(draw, item.text, box)
            continue
        speaker = item.speaker.split(" (", 1)[0]
        side = speaker_side(episode, page, panel_number, speaker, speech_index)
        target_fraction = {"left": 0.27, "center": 0.5, "right": 0.73}[side]
        target_x = left + int((right - left) * target_fraction)
        target_y = top + LETTERING_BAND + 34
        draw_speech(draw, item.text, box, (target_x, target_y))
        speech_index += 1


def make_title(part: int, destination: Path) -> None:
    image = Image.open(TITLE_BASE).convert("RGB")
    draw = ImageDraw.Draw(image)
    width, _height = image.size
    navy = "#061A31"
    copper = "#C77A44"
    cream = "#F4E4C7"

    draw.rectangle((45, 1605, width - 45, 1765), fill=navy)
    draw.line((90, 1607, width - 90, 1607), fill=copper, width=2)

    def centered(
        text: str, y: int, active_font: ImageFont.FreeTypeFont, fill: str
    ) -> None:
        text_box = draw.textbbox((0, 0), text, font=active_font)
        draw.text(
            ((width - (text_box[2] - text_box[0])) / 2, y),
            text,
            font=active_font,
            fill=fill,
        )

    centered(ARC_TITLE, 1626, font(TITLE_FONT, 23), cream)
    centered(f"PART {part}", 1681, font(TITLE_FONT, 29), copper)
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
    image = build_face_clear_canvas(source_image)
    draw = ImageDraw.Draw(image)
    for panel_index, letters in enumerate(letters_by_panel):
        letter_panel(
            draw,
            letters,
            panel_bounds(panel_index),
            episode,
            page,
            panel_index + 1,
        )

    mark = Image.open(PAGE_MARK).convert("RGBA")
    mark_size = max(72, int(min(OUTPUT_WIDTH, OUTPUT_HEIGHT) * 0.085))
    mark.thumbnail((mark_size, mark_size), Image.Resampling.LANCZOS)
    margin = max(14, int(min(OUTPUT_WIDTH, OUTPUT_HEIGHT) * 0.015))
    image.alpha_composite(
        mark,
        (OUTPUT_WIDTH - mark.width - margin, OUTPUT_HEIGHT - mark.height - margin),
    )
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
    for day_index, episode in enumerate(range(15, 22), start=1):
        episode_dir = WEEK_DIR / f"episode-{episode:02d}"
        sequence = episode_dir / "sequence-v2"
        sequence.mkdir(parents=True, exist_ok=True)
        make_title(day_index, sequence / "01-title-card-v1.png")
        for page in (1, 2):
            source = (
                episode_dir
                / "unlettered"
                / f"week-03-episode-{episode:02d}-page-{page:02d}-art-v1.png"
            )
            board = BOARD_DIR / f"week-03-episode-{episode:02d}-page-{page:02d}.md"
            finished = (
                episode_dir
                / f"week-03-episode-{episode:02d}-page-{page:02d}-lettered-v1.png"
            )
            letter_page(source, board, finished, episode, page)
            shutil.copy2(
                finished, sequence / f"0{page + 1}-comic-page-{page:02d}-v1.png"
            )
        end_card = END_CARDS[day_index - 1]
        shutil.copy2(APPROVED / end_card, sequence / f"04-{end_card}")
    print("Finished Week 3 face-clear release packages with Parts 1-7.")


if __name__ == "__main__":
    main()
