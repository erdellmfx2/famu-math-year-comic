#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKGROUNDS_DIR = REPO_ROOT / "art" / "final" / "backgrounds"
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


def send_status(message: str, channel: str | None, target: str | None, dry_run: bool) -> None:
    print(message, flush=True)
    if dry_run or not channel or not target:
        return
    cmd = [
        "openclaw",
        "message",
        "send",
        "--channel",
        channel,
        "--target",
        target,
        "--message",
        message,
    ]
    try:
        run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"[warn] status message failed: {exc.stderr.strip() or exc.stdout.strip()}", file=sys.stderr, flush=True)


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
    parser = argparse.ArgumentParser(description="Generate remaining FAMU venue background assets with cooldowns and retries.")
    parser.add_argument("--channel", default="telegram", help="Channel for short status messages (default: telegram)")
    parser.add_argument("--target", default="8642570479", help="Chat target for short status messages")
    parser.add_argument("--cooldown", type=int, default=COOLDOWN_SECONDS, help="Seconds to wait between images and retries")
    parser.add_argument("--dry-run", action="store_true", help="Show what would run without generating or sending messages")
    args = parser.parse_args()

    BACKGROUNDS_DIR.mkdir(parents=True, exist_ok=True)
    todo = remaining_specs()
    print(f"Remaining venue images: {len(todo)}", flush=True)
    for spec in todo:
        print(f" - {spec['slug']} -> {spec['filename']}", flush=True)

    if not todo:
        send_status("Venue asset batch: nothing remaining to generate.", args.channel, args.target, args.dry_run)
        return 0

    send_status(f"Venue asset batch starting. Remaining images: {len(todo)}.", args.channel, args.target, args.dry_run)

    for index, spec in enumerate(todo, start=1):
        slug = spec["slug"]
        output_path = BACKGROUNDS_DIR / spec["filename"]

        if output_path.exists():
            send_status(f"[{index}/{len(todo)}] Skipping {slug}; already exists.", args.channel, args.target, args.dry_run)
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
                send_status(f"[{index}/{len(todo)}] Completed {slug}: {spec['filename']}", args.channel, args.target, args.dry_run)
                break

            send_status(f"[{index}/{len(todo)}] Error on {slug} attempt {attempt}/{MAX_ATTEMPTS}.", args.channel, args.target, args.dry_run)
            if attempt < MAX_ATTEMPTS:
                time.sleep(args.cooldown)

        if not success:
            send_status(f"[{index}/{len(todo)}] Failed {slug} after {MAX_ATTEMPTS} attempts. Moving on.", args.channel, args.target, args.dry_run)
            print(f"[error] {slug}: {last_detail}", file=sys.stderr, flush=True)

        if index < len(todo):
            time.sleep(args.cooldown)

    send_status("Venue asset batch finished.", args.channel, args.target, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
