#!/usr/bin/env python3
"""Export one PDF page per approved social-media comic image for a week."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def version_key(path: Path) -> tuple[int, str]:
    """Prefer the newest numbered image version while keeping a stable fallback."""
    match = re.search(r"-v(\d+)\.png$", path.name)
    return (int(match.group(1)) if match else 0, path.name)


def sequence_key(path: Path) -> tuple[int, int, str]:
    """Order release sections first, then prefer the newest version."""
    match = re.match(r"(\d+)-", path.name)
    section = int(match.group(1)) if match else 0
    version, name = version_key(path)
    return (section, version, name)


def episode_key(path: Path) -> tuple[int, str]:
    """Keep episode directories in numerical release order."""
    match = re.search(r"episode-(\d+)$", path.name)
    return (int(match.group(1)) if match else -1, path.name)


def newest_per_section(paths: list[Path]) -> list[Path]:
    """Keep one latest asset for each numbered release section."""
    latest: dict[int, Path] = {}
    for path in sorted(paths, key=sequence_key):
        match = re.match(r"(\d+)-", path.name)
        if match:
            latest[int(match.group(1))] = path
    return [latest[section] for section in sorted(latest)]


def approved_pages(repo_root: Path, week: int) -> list[tuple[Path, bool]]:
    week_dir = repo_root / "art" / "final" / f"week-{week:02d}"
    pages: list[tuple[Path, bool]] = []

    for episode_dir in sorted(week_dir.glob("episode-*"), key=episode_key):
        expanded_sequence_dir = episode_dir / "sequence-v2"
        sequence_dir = (
            expanded_sequence_dir
            if expanded_sequence_dir.is_dir()
            else episode_dir / "sequence"
        )
        if sequence_dir.is_dir():
            title_cards = sorted(
                sequence_dir.glob("01-title-card-v*.png"), key=version_key
            )
            comic_pages = newest_per_section(
                list(sequence_dir.glob("0[2-9]-comic-page*.png"))
            )
            end_cards = sorted(
                sequence_dir.glob("*-end-card-v*.png"), key=sequence_key
            )
            if title_cards and comic_pages and end_cards:
                pages.append((title_cards[-1], False))
                pages.extend((comic_page, True) for comic_page in comic_pages)
                pages.append((end_cards[-1], False))
                continue

        lettered_pages = sorted(
            episode_dir.glob("*-lettered-v*.png"), key=version_key
        )
        if lettered_pages:
            pages.append((lettered_pages[-1], True))

    if not pages:
        raise FileNotFoundError(f"No approved pages found in {week_dir}")
    return pages


def export_pdf(
    pages: list[tuple[Path, bool]],
    output_path: Path,
    page_mark_path: Path,
    week: int,
    add_page_mark: bool,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf = None
    page_mark = ImageReader(str(page_mark_path))

    for page, is_comic_page in pages:
        image = ImageReader(str(page))
        width, height = image.getSize()
        if pdf is None:
            pdf = canvas.Canvas(str(output_path), pagesize=(width, height))
            pdf.setTitle(f"The Formula of Becoming - Week {week:02d}")
            pdf.setAuthor("FAMU Mathematics Department")
            pdf.setSubject("Social-media-size comic pages")
        else:
            pdf.setPageSize((width, height))

        # One PDF page matches one source image at its original pixel dimensions.
        pdf.drawImage(image, 0, 0, width=width, height=height, mask="auto")
        if is_comic_page and add_page_mark:
            mark_size = width * 0.09
            margin = width * 0.015
            pdf.drawImage(
                page_mark,
                width - mark_size - margin,
                margin,
                width=mark_size,
                height=mark_size,
                mask="auto",
            )
        pdf.showPage()

    assert pdf is not None
    pdf.save()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export approved weekly comic images as a social-media PDF."
    )
    parser.add_argument("--week", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--add-page-mark",
        action="store_true",
        help="Overlay the approved page mark on comic pages that do not already include it.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    pages = approved_pages(repo_root, args.week)
    page_mark_path = (
        repo_root
        / "art"
        / "final"
        / "series-endcards"
        / "approved"
        / "formula-of-becoming-famu-math-page-mark-v1.png"
    )
    export_pdf(pages, args.output, page_mark_path, args.week, args.add_page_mark)

    print(f"Created {args.output} with {len(pages)} social-media pages:")
    for index, (page, is_comic_page) in enumerate(pages, start=1):
        suffix = " + page mark" if is_comic_page and args.add_page_mark else ""
        print(f"{index:02d}. {page.relative_to(repo_root)}{suffix}")


if __name__ == "__main__":
    main()
