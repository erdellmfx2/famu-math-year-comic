#!/usr/bin/env python3
"""Verify a packaged comic week against the approved lettering continuity lock."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

from PIL import Image, ImageChops


def newest(paths: list[Path]) -> Path:
    if not paths:
        raise FileNotFoundError("Required release image is missing")

    def version(path: Path) -> int:
        match = re.search(r"-v(\d+)\.png$", path.name)
        return int(match.group(1)) if match else 0

    return max(paths, key=version)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_title(title: Path, base: Path, expected_part: int) -> list[str]:
    errors: list[str] = []
    with Image.open(title) as rendered, Image.open(base) as approved:
        if rendered.info.get("part") != str(expected_part):
            errors.append(f"{title}: expected PART {expected_part} metadata")
        if rendered.info.get("growing_leaf_preserved") != "true":
            errors.append(f"{title}: missing growing-leaf preservation metadata")
        if rendered.size != approved.size:
            errors.append(f"{title}: title size differs from approved base")
        else:
            # The renderer may write only below y=1605. Everything above that,
            # including the growing leaf and series title, must remain identical.
            difference = ImageChops.difference(
                rendered.convert("RGB").crop((0, 0, rendered.width, 1580)),
                approved.convert("RGB").crop((0, 0, approved.width, 1580)),
            )
            if difference.getbbox() is not None:
                errors.append(f"{title}: approved growing-leaf title pixels changed")
    return errors


def verify_comic(page: Path) -> list[str]:
    errors: list[str] = []
    with Image.open(page) as image:
        expected = {
            "dialogue_font": "Comic Sans MS Regular",
            "speech_balloon": "organic oval with speaker-directed tail",
            "caption_box": "#FFF4D6 pale cream, no tail",
            "page_mark": "formula-of-becoming-famu-math-page-mark-v1.png",
            "speaker_labels_printed": "false",
            "face_clearance": "dedicated lettering band; no balloon over art",
        }
        for key, value in expected.items():
            if image.info.get(key) != value:
                errors.append(f"{page}: {key} lock is missing or changed")
    return errors


def verify_end_card(card: Path, approved_dir: Path) -> list[str]:
    approved = approved_dir / re.sub(r"^04-", "", card.name)
    if not approved.exists():
        return [f"{card}: closing card is not from the approved set"]
    if digest(card) != digest(approved):
        return [f"{card}: approved closing-card pixels changed"]
    return []


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--week", type=int, required=True)
    parser.add_argument("--first-episode", type=int, required=True)
    parser.add_argument("--count", type=int, default=7)
    args = parser.parse_args()

    repo = args.repo.resolve()
    week_dir = repo / "art" / "final" / f"week-{args.week:02d}"
    approved_dir = repo / "art" / "final" / "series-endcards" / "approved"
    title_base = approved_dir / "formula-of-becoming-series-logo-v1.png"
    errors: list[str] = []

    for day in range(1, args.count + 1):
        episode = args.first_episode + day - 1
        sequence = week_dir / f"episode-{episode:02d}" / "sequence-v2"
        title = newest(list(sequence.glob("01-title-card-v*.png")))
        page_1 = newest(list(sequence.glob("02-comic-page-01-v*.png")))
        page_2 = newest(list(sequence.glob("03-comic-page-02-v*.png")))
        end_cards = list(sequence.glob("04-*-end-card-v*.png"))
        if len(end_cards) != 1:
            errors.append(f"{sequence}: expected exactly one closing card")
        else:
            errors.extend(verify_end_card(end_cards[0], approved_dir))
        errors.extend(verify_title(title, title_base, day))
        errors.extend(verify_comic(page_1))
        errors.extend(verify_comic(page_2))

    if errors:
        print("Release verification failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(
        f"Verified Week {args.week:02d}: {args.count} title cards, "
        f"{args.count * 2} comic pages, and {args.count} approved closing cards."
    )


if __name__ == "__main__":
    main()
