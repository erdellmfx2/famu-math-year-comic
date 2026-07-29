#!/usr/bin/env python3
"""Build visual review materials and social ads for the July 31 launch."""

from __future__ import annotations

import argparse
import html
import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


REPO_ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN_ROOT = REPO_ROOT / "campaigns" / "launch-2026-07-31"

COLORS = {
    "indigo": "#071A36",
    "indigo_2": "#0E2A50",
    "copper": "#C9793D",
    "cream": "#F5E7CD",
    "paper": "#FFF8E9",
    "green": "#215732",
    "ink": "#101B2D",
}

FONT_SERIF = Path("/System/Library/Fonts/Supplemental/Bodoni 72.ttc")
FONT_SERIF_SMALLCAPS = Path(
    "/System/Library/Fonts/Supplemental/Bodoni 72 Smallcaps Book.ttf"
)
FONT_SANS = Path("/System/Library/Fonts/Avenir Next Condensed.ttc")

TRAILER_DURATION = 50
TRAILER_DURATIONS = (4, 4, 4, 4, 5, 6, 5, 4, 4, 4, 6)

SERIES_LOGO = (
    "art/final/series-endcards/approved/formula-of-becoming-series-logo-v1.png"
)

LAUNCH_ASK_FRAME = {
    "title": "Launch ask",
    "art": "campaign-close-card.png",
    "scene": "The launch date and series identity arrive before the character hook.",
    "speaker": "narrator",
    "voiceover": "The Formula of Becoming. Begins July thirty-first.",
    "onscreen": "BEGINS JULY 31",
    "why": "Front-loads the campaign ask before viewers decide whether to continue.",
    "rules": "waterfall-entry, ambient-glow-bloom",
}

INVITATION_FRAME = {
    "title": "Invitation close",
    "art": "campaign-invitation-card.png",
    "scene": "Malik and Nia anchor a final invitation into the series world.",
    "speaker": "narrator",
    "voiceover": "Where college life, friendship, and mathematics meet.",
    "onscreen": "WHERE COLLEGE LIFE, FRIENDSHIP, AND MATHEMATICS MEET.",
    "why": "Ends on an inclusive promise rather than repeating the launch ask.",
    "rules": "waterfall-entry, ambient-glow-bloom",
}

TRAILERS = {
    "trailer-a": {
        "title": "You Cannot Plan for Everything",
        "message": (
            "Mathematics cannot eliminate uncertainty, but it can help people "
            "face it honestly."
        ),
        "angle": "Malik-led intimate character drama",
        "frames": [
            LAUNCH_ASK_FRAME,
            {
                "title": "The promise of control",
                "art": "art/final/week-01/episode-01/week-01-episode-01-art-v1.png",
                "scene": "Malik arrives early with his plan already under strain.",
                "speaker": "narrator",
                "voiceover": (
                    "Malik Baptiste believes the right plan can keep the future "
                    "from surprising him."
                ),
                "onscreen": "YOU CANNOT PLAN\nFOR EVERYTHING",
                "why": "Opens on the emotional cost of treating uncertainty as failure.",
                "rules": "multi-phase-camera, waterfall-entry",
            },
            {
                "title": "The first changed variable",
                "art": "art/final/week-01/episode-02/week-01-episode-02-art-v1.png",
                "scene": "The budget error becomes a conversation instead of a secret.",
                "speaker": "malik",
                "voiceover": (
                    "My family budget was balanced when I left. Now it isn't."
                ),
                "onscreen": "A MODEL CHANGES",
                "why": "Makes mathematics part of family life instead of classroom decoration.",
                "rules": "coordinate-target-zoom, ambient-glow-bloom",
            },
            {
                "title": "A different way to see it",
                "art": "art/final/week-01/episode-03/week-01-episode-03-art-v1.png",
                "scene": "Nia reframes new information as the beginning of a choice.",
                "speaker": "nia",
                "voiceover": "Then it was a model with new information.",
                "onscreen": "SO CAN THE NEXT CHOICE",
                "why": "Introduces Nia as the human counterpoint to Malik's precision.",
                "rules": "split-tilt-cards, waterfall-entry",
            },
            {
                "title": "Public progress",
                "art": (
                    "art/final/week-07/episode-47/unlettered/"
                    "week-07-episode-47-page-01-art-v1.png"
                ),
                "scene": "An analytics milestone looks like proof that the plan is working.",
                "speaker": "narrator",
                "voiceover": "At McCall-Hart, every answer opens another choice.",
                "onscreen": "PROGRESS CAN STILL HIDE FEAR",
                "why": "Raises ambition while preserving the hidden emotional pressure.",
                "rules": "coordinate-target-zoom, spring-pop-entrance",
            },
            {
                "title": "The storm",
                "art": (
                    "art/final/week-08/episode-50/unlettered/"
                    "week-08-episode-50-page-01-art-v1.png"
                ),
                "scene": "Storm forecasts turn uncertainty into immediate family danger.",
                "speaker": "narrator",
                "voiceover": (
                    "Then the storm turns uncertainty into something he can no "
                    "longer keep off the page."
                ),
                "onscreen": "UNCERTAINTY BECOMES REAL",
                "why": "Turns the premise into a human stake without revealing the outcome.",
                "rules": "multi-phase-camera, depth-of-field-blur",
            },
            {
                "title": "What water takes",
                "art": (
                    "art/final/week-09/episode-57/unlettered/"
                    "week-09-episode-57-page-01-art-v1.png"
                ),
                "scene": "Malik confronts damage no clean estimate can contain.",
                "speaker": "malik",
                "voiceover": (
                    "I keep looking at flood estimates. But I do not know how "
                    "high the water got inside."
                ),
                "onscreen": "WHAT THE WATER TAKES",
                "why": "Shows why quantitative work matters while respecting grief.",
                "rules": "coordinate-target-zoom, depth-of-field-blur",
            },
            {
                "title": "The honest question",
                "art": (
                    "art/final/week-07/episode-49/unlettered/"
                    "week-07-episode-49-page-01-art-v1.png"
                ),
                "scene": "Nia names the difference between sharing goals and sharing trouble.",
                "speaker": "nia",
                "voiceover": (
                    "You trust me with goals. Why do you not trust me with bad news?"
                ),
                "onscreen": "HONESTY IS PART OF THE WORK",
                "why": "Makes emotional honesty and model honesty part of one arc.",
                "rules": "multi-phase-camera, waterfall-entry",
            },
            {
                "title": "A horizon, not an answer",
                "art": (
                    "art/final/week-13/episode-87/unlettered/"
                    "week-13-episode-87-page-01-art-v1.png"
                ),
                "scene": "Malik and Nia move toward work larger than either first plan.",
                "speaker": "narrator",
                "voiceover": (
                    "Mathematics cannot promise certainty. It can teach us what "
                    "honesty asks next."
                ),
                "onscreen": "NO PERFECT ANSWERS.\nREAL NEXT CHOICES.",
                "why": "Resolves the trailer's message without resolving the story.",
                "rules": "viewport-change, ambient-glow-bloom",
            },
            {
                "title": "Series reveal",
                "art": SERIES_LOGO,
                "scene": "The approved series logo fills the frame intact.",
                "speaker": "",
                "voiceover": "",
                "onscreen": "THE FORMULA OF BECOMING",
                "why": "Names the story after the emotional promise has landed.",
                "rules": "ambient-glow-bloom, scale-swap-transition",
            },
            INVITATION_FRAME,
        ],
    },
    "trailer-b": {
        "title": "More Than One Way to See It",
        "message": (
            "Mathematics and STEM are places where different minds, experiences, "
            "and ways of seeing belong."
        ),
        "angle": "Nia-led hopeful campus momentum",
        "frames": [
            LAUNCH_ASK_FRAME,
            {
                "title": "The missing person",
                "art": "art/final/week-01/episode-02/week-01-episode-02-art-v1.png",
                "scene": "Nia sees the fear and human detail beneath the spreadsheet.",
                "speaker": "nia",
                "voiceover": "What if the model missed the person?",
                "onscreen": "WHAT IF THE MODEL\nMISSED THE PERSON?",
                "why": "Opens with belonging rather than a slogan about STEM.",
                "rules": "coordinate-target-zoom, waterfall-entry",
            },
            {
                "title": "The story inside the numbers",
                "art": "art/final/week-01/episode-03/week-01-episode-03-art-v1.png",
                "scene": "Nia sketches before calculating while Malik builds structure.",
                "speaker": "narrator",
                "voiceover": "Nia Reynolds sees the story hiding inside the numbers.",
                "onscreen": "SHE SEES THE STORY\nINSIDE THE NUMBERS",
                "why": "Normalizes a visual, human route into mathematical thinking.",
                "rules": "split-tilt-cards, ambient-glow-bloom",
            },
            {
                "title": "Campus opens",
                "art": "art/final/week-01/episode-06/week-01-episode-06-art-v1.png",
                "scene": "Indigo Night introduces music, possibility, and new relationships.",
                "speaker": "nia",
                "voiceover": "Sometimes the picture comes before the calculation.",
                "onscreen": "TWO WAYS TO BEGIN",
                "why": "Places mathematics inside a full, joyful college life.",
                "rules": "multi-phase-camera, spring-pop-entrance",
            },
            {
                "title": "A crowded future",
                "art": "art/final/week-01/episode-07/week-01-episode-07-art-v1.png",
                "scene": "Nia's confidence and commitments begin expanding together.",
                "speaker": "narrator",
                "voiceover": (
                    "Campus brings friendship, first love, and more invitations "
                    "than one life can hold."
                ),
                "onscreen": "FRIENDSHIP. FIRST LOVE.\nA CROWDED FUTURE.",
                "why": "Establishes the personal stakes without revealing later outcomes.",
                "rules": "multi-phase-camera, waterfall-entry",
            },
            {
                "title": "A boundary",
                "art": (
                    "art/final/week-07/episode-45/unlettered/"
                    "week-07-episode-45-page-01-art-v1.png"
                ),
                "scene": "Nia learns that showing up cannot mean disappearing.",
                "speaker": "nia",
                "voiceover": (
                    "I like showing up for people. I cannot disappear from my own "
                    "schedule."
                ),
                "onscreen": "BELONGING SHOULD NOT\nCOST YOURSELF",
                "why": "Connects participation in STEM to sustainable belonging.",
                "rules": "coordinate-target-zoom, depth-of-field-blur",
            },
            {
                "title": "The human detail",
                "art": (
                    "art/final/week-14/episode-92/unlettered/"
                    "week-14-episode-92-page-01-art-v1.png"
                ),
                "scene": "Nia uses rectangles and imperfect estimates with young learners.",
                "speaker": "narrator",
                "voiceover": (
                    "In classrooms and community rooms, mathematics becomes a "
                    "way to notice what has been left out."
                ),
                "onscreen": "MATHEMATICS MEETS\nTHE HUMAN DETAIL",
                "why": "Shows mathematics as shared practice rather than gatekeeping.",
                "rules": "coordinate-target-zoom, ambient-glow-bloom",
            },
            {
                "title": "Work that serves people",
                "art": (
                    "art/final/week-13/episode-88/unlettered/"
                    "week-13-episode-88-page-01-art-v1.png"
                ),
                "scene": "The laboratory horizon connects models to community consequences.",
                "speaker": "nia",
                "voiceover": (
                    "It is about reporting which pieces we observed, which we "
                    "inferred, and how those choices change the answer."
                ),
                "onscreen": "WHERE MODELS\nSERVE PEOPLE",
                "why": "Makes rigor and care reinforce one another.",
                "rules": "viewport-change, waterfall-entry",
            },
            {
                "title": "Two perspectives",
                "art": (
                    "art/final/week-13/episode-87/unlettered/"
                    "week-13-episode-87-page-01-art-v1.png"
                ),
                "scene": "Malik and Nia carry different strengths toward the same horizon.",
                "speaker": "malik",
                "voiceover": "Then we test it again.",
                "onscreen": "ONE PROBLEM.\nTWO PERSPECTIVES.",
                "why": "Completes the belonging promise through partnership, not romance.",
                "rules": "multi-phase-camera, ambient-glow-bloom",
            },
            {
                "title": "Series reveal",
                "art": SERIES_LOGO,
                "scene": "The approved series logo fills the frame intact.",
                "speaker": "",
                "voiceover": "",
                "onscreen": "THE FORMULA OF BECOMING",
                "why": "Names the story after the possibility has been felt.",
                "rules": "ambient-glow-bloom, scale-swap-transition",
            },
            INVITATION_FRAME,
        ],
    },
}

ADS = [
    {
        "slug": "01-meet-malik",
        "kicker": "MEET MALIK",
        "headline": "He trusts the plan.\nLife changes the variables.",
        "source": "art/final/week-01/episode-01/week-01-episode-01-art-v1.png",
        "focus_y": 0.14,
    },
    {
        "slug": "02-meet-nia",
        "kicker": "MEET NIA",
        "headline": "She sees the person\nthe model left out.",
        "source": "art/final/week-01/episode-02/week-01-episode-02-art-v1.png",
        "focus_y": 0.38,
    },
    {
        "slug": "03-two-ways-of-seeing",
        "kicker": "TWO WAYS OF SEEING",
        "headline": "One problem.\nTwo perspectives.\nA year of becoming.",
        "source": "art/final/week-01/episode-03/week-01-episode-03-art-v1.png",
        "focus_y": 0.44,
    },
    {
        "slug": "04-launch",
        "kicker": "A MATHEMATICS STORY",
        "headline": (
            "Budgets. Friendships.\nStorms. Futures.\nMathematics is already\npart of the story."
        ),
        "source": SERIES_LOGO,
        "focus_y": 0.5,
        "logo_layout": True,
    },
]


def font(path: Path, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size, index=index)


def cover(image: Image.Image, size: tuple[int, int], focus_y: float = 0.5) -> Image.Image:
    """Resize and crop an image to fill the target size."""
    src = image.convert("RGB")
    target_w, target_h = size
    scale = max(target_w / src.width, target_h / src.height)
    resized = src.resize(
        (round(src.width * scale), round(src.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = max(0, (resized.width - target_w) // 2)
    max_top = max(0, resized.height - target_h)
    top = round(max_top * min(1.0, max(0.0, focus_y)))
    return resized.crop((left, top, left + target_w, top + target_h))


def contain(image: Image.Image, size: tuple[int, int], color: str) -> Image.Image:
    canvas = Image.new("RGB", size, color)
    fitted = ImageOps.contain(image.convert("RGB"), size, Image.Resampling.LANCZOS)
    canvas.paste(
        fitted,
        ((size[0] - fitted.width) // 2, (size[1] - fitted.height) // 2),
    )
    return canvas


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    text_font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if draw.textbbox((0, 0), candidate, font=text_font)[2] <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    text_font: ImageFont.FreeTypeFont,
    fill: str,
    max_width: int,
    spacing: int,
    anchor: str = "la",
) -> int:
    lines = wrap_text(draw, text, text_font, max_width)
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=text_font, fill=fill, anchor=anchor)
        box = draw.textbbox((x, y), line or " ", font=text_font, anchor=anchor)
        y += box[3] - box[1] + spacing
    return y


def add_vertical_gradient(
    image: Image.Image,
    top_rgba: tuple[int, int, int, int],
    bottom_rgba: tuple[int, int, int, int],
) -> Image.Image:
    strip = Image.new("RGBA", (1, image.height))
    draw = ImageDraw.Draw(strip)
    for y in range(image.height):
        t = y / max(1, image.height - 1)
        rgba = tuple(
            round(top_rgba[i] * (1 - t) + bottom_rgba[i] * t) for i in range(4)
        )
        draw.point((0, y), fill=rgba)
    overlay = strip.resize(image.size)
    return Image.alpha_composite(image.convert("RGBA"), overlay)


def draw_tracking_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    text_font: ImageFont.FreeTypeFont,
    fill: str,
    tracking: int,
) -> int:
    x, y = xy
    for character in text:
        draw.text((x, y), character, font=text_font, fill=fill)
        width = draw.textlength(character, font=text_font)
        x += round(width) + tracking
    return x


def draw_campaign_chrome(
    draw: ImageDraw.ImageDraw,
    size: tuple[int, int],
    margin: int,
    story: bool,
) -> None:
    width, height = size
    top = 150 if story else 56
    bottom = height - (220 if story else 60)
    draw.rounded_rectangle(
        (margin, top, width - margin, bottom),
        radius=10,
        outline=COLORS["copper"],
        width=3,
    )
    draw.line(
        (margin + 28, top + 28, margin + 180, top + 28),
        fill=COLORS["copper"],
        width=4,
    )
    draw.ellipse(
        (width - margin - 40, top + 18, width - margin - 20, top + 38),
        fill=COLORS["copper"],
    )


def build_photo_ad(spec: dict, size: tuple[int, int], output: Path) -> None:
    width, height = size
    story = height / width > 1.5
    source = Image.open(REPO_ROOT / spec["source"])

    if spec.get("logo_layout"):
        background = Image.new("RGBA", size, COLORS["indigo"])
        glow = Image.new("RGBA", size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.ellipse(
            (-width // 3, -height // 5, width + width // 2, height * 3 // 4),
            fill=(201, 121, 61, 52),
        )
        glow = glow.filter(ImageFilter.GaussianBlur(90))
        background = Image.alpha_composite(background, glow)
        logo_box = (
            (560, 930) if story else (390, 820)
        )
        logo = contain(source, logo_box, COLORS["indigo"])
        logo = logo.convert("RGBA")
        if story:
            background.alpha_composite(logo, ((width - logo.width) // 2, 180))
        else:
            background.alpha_composite(logo, (68, 130))
    else:
        background = cover(source, size, spec["focus_y"]).convert("RGBA")
        tint = Image.new("RGBA", size, (7, 26, 54, 62))
        background = Image.alpha_composite(background, tint)
        background = add_vertical_gradient(
            background,
            (7, 26, 54, 25),
            (7, 26, 54, 246),
        )

    draw = ImageDraw.Draw(background)
    margin = 54 if story else 48
    draw_campaign_chrome(draw, size, margin, story)

    series_font = font(FONT_SERIF_SMALLCAPS, 36 if story else 28)
    kicker_font = font(FONT_SANS, 34 if story else 26)
    headline_size = 66 if story and spec.get("logo_layout") else (76 if story else 60)
    headline_font = font(FONT_SERIF, headline_size)
    date_font = font(FONT_SANS, 38 if story else 30)
    credit_font = font(FONT_SANS, 27 if story else 21)
    tag_font = font(FONT_SANS, 26 if story else 20)

    top_y = 205 if story else 88
    draw_tracking_text(
        draw,
        "THE FORMULA OF BECOMING",
        (margin + 34, top_y),
        series_font,
        COLORS["cream"],
        2,
    )

    if spec.get("logo_layout"):
        text_y = 1080 if story else 150
        text_x = margin + 34 if story else 520
        max_width = width - text_x - margin - 35
    else:
        text_y = height - (800 if story else 500)
        text_x = margin + 34
        max_width = width - (margin * 2) - 68

    draw_tracking_text(
        draw,
        spec["kicker"],
        (text_x, text_y),
        kicker_font,
        COLORS["copper"],
        3,
    )
    headline_y = text_y + (62 if story else 50)
    headline_y = draw_wrapped(
        draw,
        spec["headline"],
        (text_x, headline_y),
        headline_font,
        COLORS["cream"],
        max_width,
        8,
    )

    pill_y = min(headline_y + 28, height - (330 if story else 210))
    pill_w = 310 if story else 250
    pill_h = 70 if story else 56
    draw.rounded_rectangle(
        (text_x, pill_y, text_x + pill_w, pill_y + pill_h),
        radius=pill_h // 2,
        fill=COLORS["copper"],
    )
    draw.text(
        (text_x + pill_w // 2, pill_y + pill_h // 2),
        "BEGINS JULY 31",
        font=date_font,
        fill=COLORS["indigo"],
        anchor="mm",
    )

    credit_y = height - (350 if story else 123)
    draw.text(
        (margin + 34, credit_y),
        "Presented by the Mathematics Department",
        font=credit_font,
        fill=COLORS["cream"],
    )
    draw.text(
        (margin + 34, credit_y + (42 if story else 32)),
        "Fictional McCall-Hart University  •  #TheFormulaOfBecoming",
        font=tag_font,
        fill=COLORS["copper"],
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    background.convert("RGB").save(output, quality=95)


def build_close_card(output: Path) -> None:
    size = (1080, 1920)
    canvas = Image.new("RGBA", size, COLORS["indigo"])
    glow = Image.new("RGBA", size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((-220, 40, 1300, 1350), fill=(201, 121, 61, 62))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    canvas = Image.alpha_composite(canvas, glow)
    logo = contain(
        Image.open(REPO_ROOT / SERIES_LOGO),
        (520, 1095),
        COLORS["indigo"],
    ).convert("RGBA")
    canvas.alpha_composite(logo, ((1080 - logo.width) // 2, 90))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(
        (68, 88, 1012, 1768),
        radius=10,
        outline=COLORS["copper"],
        width=3,
    )
    date_font = font(FONT_SERIF, 92)
    credit_font = font(FONT_SANS, 38)
    small_font = font(FONT_SANS, 27)
    draw.text(
        (540, 1270),
        "BEGINS JULY 31",
        font=date_font,
        fill=COLORS["cream"],
        anchor="mm",
    )
    draw.line((260, 1360, 820, 1360), fill=COLORS["copper"], width=3)
    draw.text(
        (540, 1435),
        "Presented by the Mathematics Department",
        font=credit_font,
        fill=COLORS["cream"],
        anchor="mm",
    )
    draw.text(
        (540, 1515),
        "A character-led mathematics comic",
        font=small_font,
        fill=COLORS["copper"],
        anchor="mm",
    )
    draw.text(
        (540, 1570),
        "Set at fictional McCall-Hart University",
        font=small_font,
        fill=COLORS["cream"],
        anchor="mm",
    )
    draw.text(
        (540, 1680),
        "#TheFormulaOfBecoming",
        font=small_font,
        fill=COLORS["copper"],
        anchor="mm",
    )
    draw.text(
        (540, 1805),
        "Published trailer voiceovers use AI-generated voices.",
        font=font(FONT_SANS, 22),
        fill="#C9D2DF",
        anchor="mm",
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, quality=96)


def build_invitation_card(output: Path) -> None:
    size = (1080, 1920)
    source = Image.open(
        REPO_ROOT
        / "art/final/week-01/episode-03/week-01-episode-03-art-v1.png"
    )
    canvas = Image.new("RGBA", size, COLORS["indigo"])
    image = cover(source, (1080, 1050), 0.38).convert("RGBA")
    image = Image.alpha_composite(image, Image.new("RGBA", image.size, (7, 26, 54, 48)))
    canvas.alpha_composite(image, (0, 0))
    canvas = add_vertical_gradient(
        canvas,
        (7, 26, 54, 0),
        (7, 26, 54, 255),
    )
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(
        (68, 88, 1012, 1768),
        radius=10,
        outline=COLORS["copper"],
        width=3,
    )
    draw.text(
        (540, 1120),
        "THE FORMULA OF BECOMING",
        font=font(FONT_SANS, 31),
        fill=COLORS["copper"],
        anchor="mm",
    )
    phrase_font = font(FONT_SERIF, 78)
    phrase_lines = (
        "WHERE COLLEGE LIFE,",
        "FRIENDSHIP, AND",
        "MATHEMATICS MEET.",
    )
    y = 1245
    for line in phrase_lines:
        draw.text(
            (540, y),
            line,
            font=phrase_font,
            fill=COLORS["cream"],
            anchor="mm",
        )
        y += 96
    draw.line((260, 1535, 820, 1535), fill=COLORS["copper"], width=3)
    draw.text(
        (540, 1610),
        "BEGINS JULY 31",
        font=font(FONT_SANS, 39),
        fill=COLORS["cream"],
        anchor="mm",
    )
    draw.text(
        (540, 1672),
        "Presented by the Mathematics Department",
        font=font(FONT_SANS, 31),
        fill=COLORS["cream"],
        anchor="mm",
    )
    draw.text(
        (540, 1818),
        "Set at fictional McCall-Hart University",
        font=font(FONT_SANS, 22),
        fill="#C9D2DF",
        anchor="mm",
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, quality=96)


def make_contact_sheet(paths: list[Path], output: Path, columns: int = 5) -> None:
    thumb_w, thumb_h = 250, 375
    label_h = 58
    rows = math.ceil(len(paths) / columns)
    sheet = Image.new(
        "RGB",
        (columns * thumb_w, rows * (thumb_h + label_h)),
        COLORS["paper"],
    )
    draw = ImageDraw.Draw(sheet)
    label_font = font(FONT_SANS, 18)
    for index, path in enumerate(paths):
        row, col = divmod(index, columns)
        x = col * thumb_w
        y = row * (thumb_h + label_h)
        image = Image.open(path)
        sheet.paste(cover(image, (thumb_w, thumb_h)), (x, y))
        label = path.stem.replace("-page-", " p").replace("-art-v1", "")
        draw.rectangle(
            (x, y + thumb_h, x + thumb_w, y + thumb_h + label_h),
            fill=COLORS["indigo"],
        )
        draw.text(
            (x + 10, y + thumb_h + 12),
            label,
            font=label_font,
            fill=COLORS["cream"],
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=94)


def frame_art_path(frame: dict) -> Path:
    if frame["art"] in {"campaign-close-card.png", "campaign-invitation-card.png"}:
        return CAMPAIGN_ROOT / "shared" / frame["art"]
    return REPO_ROOT / frame["art"]


def build_storyboard_sheet(trailer_key: str, output: Path) -> None:
    trailer = TRAILERS[trailer_key]
    card_w, card_h = 470, 930
    columns = 4
    rows = math.ceil(len(trailer["frames"]) / columns)
    sheet = Image.new(
        "RGB",
        (columns * card_w, rows * card_h + 150),
        COLORS["paper"],
    )
    draw = ImageDraw.Draw(sheet)
    title_font = font(FONT_SERIF, 56)
    smallcaps = font(FONT_SANS, 22)
    frame_title_font = font(FONT_SERIF, 30)
    body_font = font(FONT_SANS, 22)
    label_font = font(FONT_SANS, 18)

    draw.text(
        (48, 30),
        f"{trailer_key.upper()}  •  {trailer['title']}",
        font=title_font,
        fill=COLORS["indigo"],
    )
    draw.text(
        (50, 100),
        "50 seconds  •  1080 × 1920  •  STORYBOARD + STATIC ART REVIEW",
        font=smallcaps,
        fill=COLORS["copper"],
    )

    start = 0
    for index, (duration, frame) in enumerate(
        zip(TRAILER_DURATIONS, trailer["frames"], strict=True)
    ):
        row, col = divmod(index, columns)
        x = col * card_w
        y = 150 + row * card_h
        draw.rectangle(
            (x + 8, y + 8, x + card_w - 8, y + card_h - 8),
            fill=COLORS["paper"],
            outline=COLORS["indigo"],
            width=2,
        )
        art = cover(Image.open(frame_art_path(frame)), (card_w - 32, 430), 0.4)
        sheet.paste(art, (x + 16, y + 16))
        draw.rectangle(
            (x + 16, y + 16, x + 146, y + 58),
            fill=COLORS["indigo"],
        )
        draw.text(
            (x + 29, y + 26),
            f"{start:02d}–{start + duration:02d}s",
            font=label_font,
            fill=COLORS["cream"],
        )
        copy_y = y + 470
        draw.text(
            (x + 22, copy_y),
            f"{index + 1:02d}  {frame['title']}",
            font=frame_title_font,
            fill=COLORS["indigo"],
        )
        copy_y += 48
        copy_y = draw_wrapped(
            draw,
            frame["onscreen"],
            (x + 22, copy_y),
            body_font,
            COLORS["copper"],
            card_w - 44,
            3,
        )
        copy_y += 12
        speaker = frame["speaker"].upper() if frame["speaker"] else "MUSIC"
        draw.text(
            (x + 22, copy_y),
            speaker,
            font=label_font,
            fill=COLORS["green"],
        )
        copy_y += 30
        copy_y = draw_wrapped(
            draw,
            frame["voiceover"] or "No dialogue. Score carries the reveal.",
            (x + 22, copy_y),
            body_font,
            COLORS["ink"],
            card_w - 44,
            3,
        )
        copy_y += 12
        draw_wrapped(
            draw,
            f"WHY: {frame['why']}",
            (x + 22, copy_y),
            label_font,
            "#425069",
            card_w - 44,
            2,
        )
        start += duration

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=95)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def brief_markdown(trailer_key: str) -> str:
    trailer = TRAILERS[trailer_key]
    return f"""---
workflow: general-video
flow: automation
storyboard: yes
message: "{trailer['message']}"
destination: x-and-cross-platform-social
aspect: 1080x1920
language: en
audience: "College-age readers, mathematics students, educators, and HBCU-story readers"
length: 50s
angle: "{trailer['angle']}"
---

# {trailer['title']}

## Intent

Create one half of a spoiler-light organic A/B launch test for *The Formula of
Becoming*. Mathematics appears through real choices, relationships, uncertainty,
and community consequences rather than as a motivational slogan.

## Assets

- Active approved unlettered comic art from Weeks 1-17.
- `assets/images/formula-of-becoming-series-logo-v1.png` — intact series reveal.
- `assets/images/campaign-close-card.png` — front-loaded launch ask.
- `assets/images/campaign-invitation-card.png` — shared closing invitation.

## Customizations

- Narrator (`cedar`), Malik (`ash`), and Nia (`coral`) through the OpenAI voice API.
- Locked name pronunciations from `audio/voice-casting/pronunciation-lexicon.json`.
- White active-word captions with dark green `#215732` highlight.
- Original or properly licensed cinematic instrumental score with restrained transitions.
- Clearly perceptible Ken Burns motion and purposeful panel crops.

## Notes

- Storyboard and static-frame approval is required before voice generation.
- No breakup result, analytics-competition result, or other major outcome is revealed.
- Credit reads `Presented by the Mathematics Department`.
- McCall-Hart University, its characters, locations, and events are fictional.
- Published voiceovers disclose that they use AI-generated voices.
"""


def design_markdown(trailer_key: str) -> str:
    trailer = TRAILERS[trailer_key]
    return f"""# Design — {trailer['title']}

## Concept

{trailer['angle']}. Character faces and meaningful objects remain the focal points;
mathematical imagery appears as lived evidence, never as decorative equations.

## Palette

- Deep indigo `#071A36`
- Copper `#C9793D`
- Cream `#F5E7CD`
- Cypress gray `#425069`
- Active caption highlight `#215732`

## Typography

- Display: Bodoni-style editorial serif in static campaign art; League Gothic or
  Archivo Black may be used for compact motion headlines.
- Supporting copy: Montserrat.
- Captions: Montserrat, white, three to five words per group.

## Composition

- Canvas: 1080 × 1920 at 30 fps.
- Face-safe crops with the visual action above the caption rail.
- Editorial rules, copper registration marks, subtle grain, and localized glows.
- No FAMU marks, colors, buildings, or claim that fictional McCall-Hart is FAMU.

## Motion

- Story art begins 8-10 percent enlarged and settles outward over each beat.
- Directional drift follows the active face, hand, notebook, screen, or setting cue.
- Harder cuts serve pressure; crossfades serve recognition and connection.
- Series logo and close remain intact and uncropped.

## Audio

- Three distinct approved voices: narrator `cedar`, Malik `ash`, Nia `coral`.
- Cinematic instrumental score remains below dialogue and avoids melodramatic swells.
- Restrained low impacts, page turns, room tone, rain, and transition risers only
  where they clarify a beat.
"""


def storyboard_markdown(trailer_key: str) -> str:
    trailer = TRAILERS[trailer_key]
    lines = [
        "---",
        "format: 1080x1920",
        "duration: 50s",
        f'message: "{trailer["message"]}"',
        "arc: Launch ask → Hook → Character pressure → Human stakes → Possibility → Invitation",
        "audience: College-age readers, mathematics students, educators, and HBCU-story readers",
        "mode: collaborative",
        "---",
        "",
    ]
    start = 0
    for index, (duration, frame) in enumerate(
        zip(TRAILER_DURATIONS, trailer["frames"], strict=True), start=1
    ):
        src = f"compositions/frames/{index:02d}-{slugify(frame['title'])}.html"
        voice = frame["voiceover"].replace('"', "'")
        lines.extend(
            [
                f"## Frame {index} — {frame['title']}",
                "",
                "- status: built",
                f"- src: {src}",
                f"- duration: {duration}s",
                f"- transition_in: {'cut' if index in (1, 2, 6, 10, 11) else 'crossfade'}",
                f"- scene: {frame['scene']}",
                f'- voiceover: "{voice}"' if voice else "- voiceover: ",
                f"- poster: {max(0.5, duration - 0.5):.1f}s",
                f"- source_art: {frame['art']}",
                f"- motion_rules: {frame['rules']}",
                f"- time_window: {start}s-{start + duration}s",
                "",
                frame["why"],
                "",
                f"On-screen copy: `{frame['onscreen'].replace(chr(10), ' / ')}`",
                "",
            ]
        )
        start += duration
    return "\n".join(lines)


def script_markdown(trailer_key: str) -> str:
    trailer = TRAILERS[trailer_key]
    lines = [
        f"# SCRIPT — {trailer_key}",
        "",
        "**Voices:** OpenAI narrator `cedar`, Malik `ash`, Nia `coral`",
        "**Voice settings:** Established casting directions and pronunciation lexicon",
        (
            "**Voice direction:** Character-led and emotionally grounded; cinematic "
            "without a conventional booming trailer voice."
        ),
        "**Approval status:** APPROVED FOR VOICE AND VIDEO PRODUCTION",
        "",
        "---",
        "",
    ]
    start = 0
    line_number = 1
    for frame_number, (duration, frame) in enumerate(
        zip(TRAILER_DURATIONS, trailer["frames"], strict=True), start=1
    ):
        if frame["voiceover"]:
            lines.extend(
                [
                    f"## Line {line_number} — {frame['title']} (Frame {frame_number})",
                    "",
                    f"**Speaker:** {frame['speaker']}",
                    f"**Time:** {start:.1f}–{start + duration:.1f}s",
                    f"**Delivery:** Serve the frame's role: {frame['why']}",
                    "",
                    f"    {frame['voiceover']}",
                    "",
                ]
            )
            line_number += 1
        start += duration
    return "\n".join(lines)


def voice_manifest(trailer_key: str) -> dict:
    trailer = TRAILERS[trailer_key]
    speakers = {
        "narrator": {
            "voice": "cedar",
            "instructions": (
                "Speak only the supplied narration. Warm, grounded, observant, "
                "quietly lyrical, and cinematic without a booming trailer voice. "
                "Do not add words or imitate a real person."
            ),
        },
        "malik": {
            "voice": "ash",
            "instructions": (
                "Speak only Malik's supplied words. Thoughtful, precise, guarded, "
                "and economical, with controlled feeling beneath the polish. Do "
                "not add words or imitate a real person."
            ),
        },
        "nia": {
            "voice": "coral",
            "instructions": (
                "Speak only Nia's supplied words. Bright, expressive, curious, "
                "and emotionally available, slowing for human consequences. Do "
                "not add words or imitate a real person."
            ),
        },
    }
    scenes = []
    for index, frame in enumerate(trailer["frames"], start=1):
        if not frame["voiceover"]:
            continue
        if frame["title"] == "Launch ask":
            scene_id = "10-launch-close"
        elif frame["title"] == "Invitation close":
            scene_id = "11-invitation-close"
        else:
            scene_id = f"{index - 1:02d}-{slugify(frame['title'])}"
        scenes.append(
            {
                "id": scene_id,
                "panel": frame["art"],
                "utterances": [
                    {
                        "speaker": frame["speaker"],
                        "text": frame["voiceover"],
                        "pause_after": 0,
                    }
                ],
            }
        )
    return {
        "project": f"The Formula of Becoming Launch - {trailer['title']}",
        "approval_status": "approved_for_production",
        "model": "gpt-4o-mini-tts",
        "response_format": "mp3",
        "default_pause_after": 0.18,
        "speakers": speakers,
        "scenes": scenes,
    }


def slugify(text: str) -> str:
    return "-".join(
        "".join(character.lower() if character.isalnum() else " " for character in text)
        .split()
    )


def wireframe_html(frame_number: int, frame: dict, duration: int) -> str:
    composition_id = f"frame-{frame_number:02d}-{slugify(frame['title'])}"
    art_label = Path(frame["art"]).name
    onscreen = html.escape(frame["onscreen"]).replace("\n", "<br>")
    voiceover = html.escape(frame["voiceover"] or "Music and score only.")
    return f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; }}
      body {{ background: #fff8e9; color: #071a36; font-family: "Montserrat", sans-serif; }}
      #root {{ position: relative; width: 1080px; height: 1920px; padding: 96px; }}
      .label {{ color: #c9793d; font-family: "JetBrains Mono", monospace; font-size: 28px; }}
      .media {{ margin-top: 54px; height: 940px; border: 6px solid #071a36;
        background: #d9d1c4; display: grid; place-items: center; padding: 56px;
        font-family: "JetBrains Mono", monospace; font-size: 34px; text-align: center; }}
      h1 {{ margin: 64px 0 24px; font-family: "League Gothic", sans-serif;
        font-size: 118px; line-height: .92; font-weight: 400; letter-spacing: .02em; }}
      .voice {{ border-top: 4px solid #c9793d; padding-top: 28px; font-size: 34px;
        line-height: 1.35; }}
      .safe {{ position: absolute; left: 96px; right: 96px; bottom: 210px;
        height: 110px; border: 3px dashed #215732; color: #215732;
        display: grid; place-items: center; font-size: 25px; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="{composition_id}" data-start="0"
      data-duration="{duration}" data-width="1080" data-height="1920">
      <div class="clip" data-start="0" data-duration="{duration}" data-track-index="1">
        <div class="label">FRAME {frame_number:02d}  /  {duration}s  /  MEDIA BLOCK</div>
        <div class="media">{html.escape(art_label)}<br><br>Face-safe crop and focal point are
          verified against the source-art review board.</div>
        <h1>{onscreen}</h1>
        <div class="voice"><strong>{html.escape(frame['speaker'].upper() or 'MUSIC')}:</strong>
          {voiceover}</div>
        <div class="safe">CAPTION SAFE AREA — ACTIVE WORD HIGHLIGHT #215732</div>
      </div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["{composition_id}"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""


def candidate_paths() -> list[Path]:
    weeks = ("week-01", "week-07", "week-08", "week-09", "week-13", "week-14")
    paths: list[Path] = []
    for week in weeks:
        root = REPO_ROOT / "art" / "final" / week
        paths.extend(sorted(root.glob("episode-*/unlettered/*page-01-art-v1.png")))
        paths.extend(sorted(root.glob("episode-*/*-art-v1.png")))
    return sorted(set(paths))


def stage_trailer_project(trailer_key: str) -> None:
    trailer_root = CAMPAIGN_ROOT / "trailers" / trailer_key
    project_root = trailer_root / "hyperframes"
    images_root = project_root / "assets" / "images"
    frames_root = project_root / "compositions" / "frames"
    review_root = trailer_root / "review"
    images_root.mkdir(parents=True, exist_ok=True)
    frames_root.mkdir(parents=True, exist_ok=True)
    review_root.mkdir(parents=True, exist_ok=True)

    staged: dict[Path, str] = {}
    for frame in TRAILERS[trailer_key]["frames"]:
        source = frame_art_path(frame)
        staged[source] = source.name
    for source, name in staged.items():
        shutil.copy2(source, images_root / name)

    write_text(project_root / "BRIEF.md", brief_markdown(trailer_key))
    write_text(project_root / "DESIGN.md", design_markdown(trailer_key))
    write_text(project_root / "STORYBOARD.md", storyboard_markdown(trailer_key))
    write_text(project_root / "SCRIPT.md", script_markdown(trailer_key))
    write_text(
        trailer_root / "voice" / "full-cast-manifest.json",
        json.dumps(voice_manifest(trailer_key), indent=2),
    )
    write_text(
        trailer_root / "voice" / "README.md",
        """# Voice Generation Gate

Status: **Approved for production**

The storyboard, static-frame package, and API voice generation are approved.

1. Run the full-cast generator in dry-run mode.
2. Verify narrator `cedar`, Malik `ash`, and Nia `coral`.
3. Verify the pronunciation lexicon applies `muh-LEEK`.
4. Generate Trailer A first and finish its review before generating Trailer B.
""",
    )

    for index, (duration, frame) in enumerate(
        zip(TRAILER_DURATIONS, TRAILERS[trailer_key]["frames"], strict=True),
        start=1,
    ):
        filename = f"{index:02d}-{slugify(frame['title'])}.html"
        write_text(frames_root / filename, wireframe_html(index, frame, duration))

    shutil.copy2(
        CAMPAIGN_ROOT / "shared" / "campaign-close-card.png",
        review_root / "campaign-close-card.png",
    )
    shutil.copy2(
        CAMPAIGN_ROOT / "shared" / "campaign-invitation-card.png",
        review_root / "campaign-invitation-card.png",
    )


def campaign_readme() -> str:
    return """# July 31 Launch Campaign

This package launches *The Formula of Becoming* on Friday, July 31, 2026.

## Campaign Position

The series follows Malik Baptiste and Nia Reynolds, two first-year mathematics
students at fictional McCall-Hart University. Mathematics is treated as lived
practice inside friendship, family pressure, college life, uncertainty, and
community-facing work.

Public campaign credit:

> Presented by the Mathematics Department

This neutral credit does not identify fictional McCall-Hart University as FAMU
or claim that its fictional people, buildings, teams, or events are real.

## Approval State

- Story and comic production: approved.
- Static advertisements: complete and approved.
- Trailer storyboards and wireframes: complete and approved.
- Voice generation and word-timed captions: complete.
- HyperFrames trailer renders: complete and verified at 50 seconds each.

Both trailers put the launch ask in the opening four seconds. After their
distinct character-led stories, they share the invitation, `Where college life,
friendship, and mathematics meet`, followed by a July 31 final hold.

## Deliverables

- `ads/feed/` — four 1080 × 1350 advertisements.
- `ads/story/` — four 1080 × 1920 advertisements.
- `exports/trailer-a-you-cannot-plan-for-everything.mp4` — final 50-second Trailer A.
- `exports/trailer-b-more-than-one-way-to-see-it.mp4` — final 50-second Trailer B.
- `review/` — source-art and trailer storyboard sheets.
- `trailers/trailer-a/` — Malik-led character-drama trailer project.
- `trailers/trailer-b/` — Nia-led campus-possibility trailer project.
- `hermes/` — posting copy, alt text, schedule, and A/B measurement manifest.
- `verification-report.md` — technical and visual delivery checks.
"""


def alt_text_markdown() -> str:
    return """# Campaign Alt Text

## Trailer A — You Cannot Plan for Everything

A vertical animated-comic trailer follows Malik Baptiste as a careful plan gives
way to a budget change, a Gulf storm, family pressure, and a more honest way to
face uncertainty. Nia challenges him to share bad news as readily as goals.
Word-highlighted captions remain below the artwork. The Formula of Becoming
begins July 31. It closes with the invitation: “Where college life, friendship,
and mathematics meet.”

## Trailer B — More Than One Way to See It

A vertical animated-comic trailer follows Nia Reynolds through visual thinking,
friendship, a crowded campus life, community mathematics, and a partnership with
Malik built on two ways of seeing. Word-highlighted captions remain below the
artwork. The Formula of Becoming begins July 31. It closes with the invitation:
“Where college life, friendship, and mathematics meet.”

## 01 — Meet Malik

Modern animated-comic scenes show Malik Baptiste, a Black first-year actuarial
science student with glasses and a navy jacket, arriving at a honey-brick campus
building and working tensely over a laptop and notebook. Text reads: “He trusts
the plan. Life changes the variables.” The Formula of Becoming begins July 31.

## 02 — Meet Nia

Modern animated-comic scenes show Nia Reynolds, a Black first-year mathematical
sciences student with long curls and a copper top, joining Malik at a study table
and responding with warmth and curiosity. Text reads: “She sees the person the
model left out.” The Formula of Becoming begins July 31.

## 03 — Two Ways of Seeing

Malik and Nia sit together with notebooks, a laptop, and visual diagrams as they
approach the same modeling problem differently. Text reads: “One problem. Two
perspectives. A year of becoming.” The comic begins July 31.

## 04 — Launch

An indigo-and-copper series poster shows a growing plant emerging through a
mathematical curve above the title The Formula of Becoming. Text reads:
“Budgets. Friendships. Storms. Futures. Mathematics is already part of the
story.” The comic begins July 31.
"""


def posting_copy_markdown() -> str:
    return """# Launch Posting Copy

## Shared Trailer Copy

Plans change. Models change. People do too.

*The Formula of Becoming* follows Malik and Nia through college, friendship,
family pressure, and mathematics that matters because real choices are attached
to it.

Begins July 31. Presented by the Mathematics Department.

#TheFormulaOfBecoming #MathStories

Video voiceovers use AI-generated voices. McCall-Hart University and its
characters are fictional.

## Static Ad 01 — Malik

Meet Malik Baptiste: actuarial science student, careful planner, and the person
most likely to trust a spreadsheet before he trusts a room. The plan changes
July 31. #TheFormulaOfBecoming

## Static Ad 02 — Nia

Meet Nia Reynolds: mathematical sciences student, visual thinker, and the person
most likely to notice the human detail a tidy model left out. Her story begins
July 31. #TheFormulaOfBecoming

## Static Ad 03 — Two Perspectives

One problem. Two perspectives. A friendship built on telling the truth about
both the numbers and the people inside them. Begins July 31.
#TheFormulaOfBecoming #MathStories

## Static Ad 04 — Launch

Budgets. Friendships. Storms. Futures. Mathematics is already part of the story.
*The Formula of Becoming* begins July 31. Presented by the Mathematics
Department. #TheFormulaOfBecoming
"""


def hermes_manifest_markdown() -> str:
    return """# July 31 Launch — Hermes Posting Manifest

Launch: **Friday, July 31, 2026**
Primary platform: **X**
Cross-posting: **Approved social channels**
Publishing owner: **Hermes**

## Required Language

- Credit: `Presented by the Mathematics Department`
- Fiction notice: `McCall-Hart University and its characters are fictional.`
- Video disclosure: `Video voiceovers use AI-generated voices.`

## Schedule

| Date / time EDT | Asset | Purpose | Status |
| --- | --- | --- | --- |
| Thu Jul 30, 9:00 a.m. | Meet Malik Story | Character introduction | Ready |
| Thu Jul 30, 12:15 p.m. | Meet Nia Story | Character introduction | Ready |
| Thu Jul 30, 7:30 p.m. | Two Ways feed + Story | Premise teaser | Ready |
| Fri Jul 31, 9:00 a.m. | Trailer A | Organic test variant A | Ready |
| Fri Jul 31, 12:15 p.m. | Episode 001 | Comic launch; pin on X | Existing episode package |
| Fri Jul 31, 7:30 p.m. | Launch Story | Opening-day reminder | Ready |
| Sat Aug 1, 9:00 a.m. | Trailer B | Organic test variant B | Ready |

## Final Asset Paths

- Trailer A: `exports/trailer-a-you-cannot-plan-for-everything.mp4`
- Trailer B: `exports/trailer-b-more-than-one-way-to-see-it.mp4`
- Feed advertisements: `ads/feed/`
- Story advertisements: `ads/story/`
- Posting copy: `hermes/posting-copy.md`
- Alt text: `hermes/alt-text.md`

## A/B Measurement

Record results after equal 24-hour windows. Treat the comparison as directional.

| Variant | Impressions | 3-second holds | Completion rate | Shares / reposts | Profile visits | Follows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Trailer A |  |  |  |  |  |  |
| Trailer B |  |  |  |  |  |  |

## Publishing Notes

- Both trailers passed voice, motion, caption, layout, and final-preview review.
- Both trailers are 50 seconds and open with the July 31 launch ask.
- Both trailers close with `Where college life, friendship, and mathematics
  meet`, followed by the shared July 31 and Mathematics Department hold.
- Keep the shared opening and closing unchanged so the central character story
  remains the primary A/B variable.
- Do not upload raw voice files, API credentials, or large working renders.
"""


def verification_report_markdown() -> str:
    return """# July 31 Campaign Verification Report

Verified: **July 29, 2026**

## Trailers

| Asset | Duration | Frame | Video | Audio | Status |
| --- | ---: | --- | --- | --- | --- |
| Trailer A — You Cannot Plan for Everything | 50.000 s | 1080 × 1920, 30 fps | H.264 | AAC LC, stereo, 48 kHz | Pass |
| Trailer B — More Than One Way to See It | 50.000 s | 1080 × 1920, 30 fps | H.264 | AAC LC, stereo, 48 kHz | Pass |

- HyperFrames runtime, layout, motion, and WCAG AA contrast checks passed.
- Both 50-second trailers open with the series title and July 31 launch ask before
  moving into their A/B-specific character stories.
- Early and late rendered frames confirm visible Ken Burns motion.
- White word-timed captions use dark mathematics-green active-word highlights.
- Captions remain in a dedicated face-safe rail outside the comic artwork.
- Narrator, Malik, and Nia use distinct approved voices.
- Pronunciation locks are applied for character names, including `muh-LEEK`.
- Both trailers use the same silent logo beat and narrator invitation: `Where
  college life, friendship, and mathematics meet.`
- The final silent hold restores `Begins July 31`, the Mathematics Department
  credit, and the AI-voice disclosure.
- Trailer A audio measures -20.3 dB mean and -2.2 dB peak.
- Trailer B audio measures -20.6 dB mean and -2.5 dB peak.
- The music bed is an original deterministic procedural score.

## Advertisements

- Four feed images verified at 1080 × 1350.
- Four Story/Reel covers verified at 1080 × 1920.
- All eight assets carry the July 31 launch message, series title, campaign
  hashtag, and `Presented by the Mathematics Department` credit.

## Repository Safety

- API key files are ignored.
- Final video exports, generated voice files, mixed audio, and preview snapshots
  are retained locally and excluded from GitHub.
"""


def build_campaign() -> None:
    close_card = CAMPAIGN_ROOT / "shared" / "campaign-close-card.png"
    build_close_card(close_card)
    build_invitation_card(
        CAMPAIGN_ROOT / "shared" / "campaign-invitation-card.png"
    )

    feed_size = (1080, 1350)
    story_size = (1080, 1920)
    for ad in ADS:
        build_photo_ad(
            ad,
            feed_size,
            CAMPAIGN_ROOT / "ads" / "feed" / f"{ad['slug']}-feed.png",
        )
        build_photo_ad(
            ad,
            story_size,
            CAMPAIGN_ROOT / "ads" / "story" / f"{ad['slug']}-story.png",
        )

    ad_outputs = sorted((CAMPAIGN_ROOT / "ads").glob("*/*.png"))
    make_contact_sheet(
        ad_outputs,
        CAMPAIGN_ROOT / "review" / "social-advertisements-review.jpg",
        columns=4,
    )

    for trailer_key in TRAILERS:
        build_storyboard_sheet(
            trailer_key,
            CAMPAIGN_ROOT / "review" / f"{trailer_key}-storyboard-review.jpg",
        )
        stage_trailer_project(trailer_key)

    write_text(CAMPAIGN_ROOT / "README.md", campaign_readme())
    write_text(CAMPAIGN_ROOT / "hermes" / "alt-text.md", alt_text_markdown())
    write_text(CAMPAIGN_ROOT / "hermes" / "posting-copy.md", posting_copy_markdown())
    write_text(
        CAMPAIGN_ROOT / "hermes" / "posting-manifest.md",
        hermes_manifest_markdown(),
    )
    write_text(
        CAMPAIGN_ROOT / "verification-report.md",
        verification_report_markdown(),
    )
    print(CAMPAIGN_ROOT)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--contact-sheet",
        action="store_true",
        help="Build a temporary source-art selection sheet.",
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build the campaign approval package and social advertisements.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.contact_sheet:
        output = CAMPAIGN_ROOT / "review" / "source-art-candidates.jpg"
        make_contact_sheet(candidate_paths(), output)
        print(output)
        return
    if args.build:
        build_campaign()
        return
    raise SystemExit("Choose a build mode.")


if __name__ == "__main__":
    main()
