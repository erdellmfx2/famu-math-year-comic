#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKGROUNDS_DIR = REPO_ROOT / "art" / "final" / "backgrounds"
LOG_DIR = REPO_ROOT / "logs"
LOG_PATH = LOG_DIR / "venue_background_generation.log"
COOLDOWN_SECONDS = 180
MAX_ATTEMPTS = 2

VENUE_SPECS = [
    {
        "slug": "al_lawson_center",
        "filename": "al_lawson_center_wide_establishing.png",
        "prompt": "Modern animated comic style background plate of the Al Lawson Center at Florida A&M University, wide indoor basketball arena establishing view, polished hardwood court, modern collegiate seating bowl, bright indoor sports lighting, FAMU green and orange accents, energetic but clean atmosphere, readable environment, semi-cartoon linework, polished digital illustration, no text, no watermark, G-rated, social-media comic friendly.",
    },
    {
        "slug": "bragg_memorial_stadium",
        "filename": "bragg_memorial_stadium_wide_establishing.png",
        "prompt": "Modern animated comic style background plate of Ken Riley Field at Bragg Memorial Stadium at Florida A&M University, wide interior field establishing view from the lower stands, broad collegiate seating bowl, vivid green football field, FAMU green and orange atmosphere, warm Florida late afternoon light, HBCU game-day energy, clean semi-cartoon linework, readable composition, polished digital illustration, youth-friendly inspirational comic tone, no text, no watermark.",
    },
    {
        "slug": "coleman_library",
        "filename": "coleman_library_exterior_establishing.png",
        "prompt": "Modern animated comic style background plate of Samuel H. Coleman Memorial Library at Florida A&M University, exterior establishing view of the main library building, academic anchor campus architecture, welcoming front approach, a few students entering or exiting in the distance, warm Florida daylight, library seriousness with student life warmth, clean semi-cartoon linework, readable composition, polished digital illustration, youth-friendly inspirational comic tone, no text, no watermark.",
    },
    {
        "slug": "famu_eternal_flame",
        "filename": "famu_eternal_flame_establishing.png",
        "prompt": "Modern animated comic style background plate of the Florida A&M University Eternal Flame campus landmark, wide establishing shot with surrounding campus context, symbolic and inspirational atmosphere, warm academic pride, golden hour light with a visible eternal flame glow, clean semi-cartoon linework, readable social-media comic composition, polished digital illustration, grounded but iconic, no text, no watermark.",
    },
    {
        "slug": "jackson_davis_hall",
        "filename": "famu_jackson_davis_hall_establishing.png",
        "prompt": "Modern animated comic style background plate of Jackson Davis Hall at Florida A&M University, exterior campus establishing shot, warm Florida light, welcoming academic building atmosphere, green and orange identity accents, clean semi-cartoon linework, polished digital illustration, youth-friendly inspirational comic tone, no text, no watermark.",
    },
    {
        "slug": "jschool",
        "filename": "jschool_exterior_establishing.png",
        "prompt": "Modern animated comic style background plate of the School of Journalism & Graphic Communication at Florida A&M University, exterior establishing shot, modern communication-school energy, student media and creative campus atmosphere, welcoming walkway and entry composition, warm Florida daylight, clean semi-cartoon linework, polished digital illustration, readable social-media comic background, no text, no watermark.",
    },
    {
        "slug": "learning_commons",
        "filename": "famu_learning_commons_interior.png",
        "prompt": "Modern animated comic style background plate of a Florida A&M learning commons interior, student study atmosphere, collaborative tables, warm academic lighting, green and orange identity accents, clean semi-cartoon linework, readable environment, polished digital illustration, youth-friendly inspirational comic tone, no text, no watermark.",
    },
    {
        "slug": "moore_kittles_field",
        "filename": "moore_kittles_field_wide_establishing.png",
        "prompt": "Modern animated comic style background plate of Moore-Kittles Field at Florida A&M University, wide college baseball field establishing view, intimate bleachers, dugout and backstop feel, sunny Florida daylight, green field with orange and green identity touches, warm community atmosphere, clean semi-cartoon linework, readable composition, polished digital illustration, no text, no watermark.",
    },
    {
        "slug": "sbi",
        "filename": "sbi_exterior_establishing.png",
        "prompt": "Modern animated comic style background plate of the School of Business and Industry at Florida A&M University, exterior establishing shot, polished and ambitious campus architecture, professional entry walkway, warm Florida daylight, leadership and career-prep energy, clean semi-cartoon linework, readable composition, polished digital illustration, youth-friendly inspirational comic tone, no text, no watermark.",
    },
    {
        "slug": "top_cafe",
        "filename": "famu_top_cafe_interior.png",
        "prompt": "Modern animated comic style background plate of a Florida A&M campus cafe interior, student life warmth, dining and conversation setting, green and orange atmosphere, clean semi-cartoon linework, readable environment, polished digital illustration, no text, no watermark.",
    },
]


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=check)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def log(message: str) -> None:
    print(message, flush=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"{now_iso()} {message}\n")


def is_done(spec: dict[str, str]) -> bool:
    return (BACKGROUNDS_DIR / spec["filename"]).exists()


def generate(spec: dict[str, str], dry_run: bool) -> tuple[bool, str]:
    output_path = BACKGROUNDS_DIR / spec["filename"]
    if dry_run:
        return True, f"[dry-run] would generate {output_path.name}"

    cmd = [
        "openclaw",
        "infer",
        "image",
        "generate",
        "--model",
        "openai/gpt-image-2",
        "--size",
        "1536x1024",
        "--count",
        "1",
        "--prompt",
        spec["prompt"],
        "--output",
        str(output_path),
        "--json",
    ]
    try:
        result = run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip() or str(exc)
        return False, detail

    stdout = result.stdout.strip()
    if stdout:
        try:
            payload = json.loads(stdout.splitlines()[-1])
            model = payload.get("model") or "unknown-model"
            return True, f"generated with {model}"
        except json.JSONDecodeError:
            pass
    return True, "generated"


def remaining_specs() -> list[dict[str, str]]:
    return [spec for spec in VENUE_SPECS if not is_done(spec)]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate remaining FAMU venue background assets with cooldowns, retries, and local logging.")
    parser.add_argument("--cooldown", type=int, default=COOLDOWN_SECONDS, help="Seconds to wait between images and retries")
    parser.add_argument("--dry-run", action="store_true", help="Show what would run without generating")
    args = parser.parse_args()

    BACKGROUNDS_DIR.mkdir(parents=True, exist_ok=True)
    todo = remaining_specs()
    log(f"Remaining venue images: {len(todo)}")
    for spec in todo:
        log(f" - {spec['slug']} -> {spec['filename']}")

    if not todo:
        log("Venue asset batch: nothing remaining to generate.")
        return 0

    log(f"Venue asset batch starting. Remaining images: {len(todo)}.")

    for index, spec in enumerate(todo, start=1):
        slug = spec["slug"]
        output_path = BACKGROUNDS_DIR / spec["filename"]

        if output_path.exists():
            log(f"[{index}/{len(todo)}] Skipping {slug}; already exists.")
            if index < len(todo):
                time.sleep(args.cooldown)
            continue

        success = False
        last_detail = ""
        for attempt in range(1, MAX_ATTEMPTS + 1):
            ok, detail = generate(spec, dry_run=args.dry_run)
            last_detail = detail
            if ok:
                success = True
                log(f"[{index}/{len(todo)}] Completed {slug}: {spec['filename']} ({detail})")
                break

            log(f"[{index}/{len(todo)}] Error on {slug} attempt {attempt}/{MAX_ATTEMPTS}: {detail}")
            if attempt < MAX_ATTEMPTS:
                time.sleep(args.cooldown)

        if not success:
            log(f"[{index}/{len(todo)}] Failed {slug} after {MAX_ATTEMPTS} attempts. Moving on.")
            print(f"[error] {slug}: {last_detail}", file=sys.stderr, flush=True)

        if index < len(todo):
            time.sleep(args.cooldown)

    log("Venue asset batch finished.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
