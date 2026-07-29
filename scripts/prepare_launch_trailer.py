#!/usr/bin/env python3

import argparse
import html
import importlib.util
import json
import math
import shutil
import struct
import subprocess
import wave
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN_ROOT = REPO_ROOT / "campaigns" / "launch-2026-07-31"
BUILDER_PATH = REPO_ROOT / "scripts" / "build_launch_campaign.py"
VOICE_GAP = 0.10
RUNTIME = 50
STORY_START = 4.0
LOGO_START = 40.0
INVITATION_START = 44.0


def load_campaign_builder():
    spec = importlib.util.spec_from_file_location("launch_campaign_builder", BUILDER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(command):
    subprocess.run(command, check=True)


def ffprobe_duration(path):
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def process_voice(project_root, trailer_root, manifest):
    source_dir = trailer_root / "voice" / "generated"
    destination_dir = project_root / "assets" / "audio" / "voice"
    destination_dir.mkdir(parents=True, exist_ok=True)
    lines = []

    for scene in manifest["scenes"]:
        utterance = scene["utterances"][0]
        speaker = utterance["speaker"]
        source = source_dir / f"{scene['id']}-001-{speaker}.mp3"
        if not source.exists():
            raise FileNotFoundError(source)
        destination = destination_dir / f"{scene['id']}-{speaker}.wav"
        if scene["id"] == "10-launch-close":
            tempo = 1.18
        elif scene["id"] == "11-invitation-close":
            tempo = 1.10
        else:
            tempo = 1.15
        run(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-i",
                str(source),
                "-filter:a",
                f"atempo={tempo},loudnorm=I=-16:TP=-1.5:LRA=7,aresample=48000",
                "-ac",
                "2",
                str(destination),
            ]
        )
        lines.append(
            {
                "scene": scene["id"],
                "speaker": speaker,
                "text": utterance["text"],
                "file": destination.relative_to(project_root).as_posix(),
                "duration": round(ffprobe_duration(destination), 3),
            }
        )

    cursor = STORY_START + 0.25
    for line in lines:
        if line["scene"] == "10-launch-close":
            line["start"] = 0.20
        elif line["scene"] == "11-invitation-close":
            line["start"] = INVITATION_START + 0.35
        else:
            line["start"] = round(cursor, 3)
            cursor = line["start"] + line["duration"] + VOICE_GAP

    content_end = max(
        line["start"] + line["duration"]
        for line in lines
        if line["scene"] not in {"10-launch-close", "11-invitation-close"}
    )
    launch_end = next(
        line["start"] + line["duration"]
        for line in lines
        if line["scene"] == "10-launch-close"
    )
    invitation_end = next(
        line["start"] + line["duration"]
        for line in lines
        if line["scene"] == "11-invitation-close"
    )
    if launch_end > STORY_START - 0.10:
        raise RuntimeError(f"Launch narration reaches {launch_end:.2f}s and collides with the story")
    if content_end > LOGO_START - 0.15:
        raise RuntimeError(f"Dialogue reaches {content_end:.2f}s and collides with the logo reveal")
    if invitation_end > RUNTIME - 0.15:
        raise RuntimeError(
            f"Invitation narration reaches {invitation_end:.2f}s and exceeds the safe runtime"
        )
    return sorted(lines, key=lambda line: line["start"])


def build_original_score(destination, trailer_key, duration=RUNTIME, sample_rate=48000):
    destination.parent.mkdir(parents=True, exist_ok=True)
    frame_count = duration * sample_rate
    audio = bytearray()
    phase_shift = 0.04 if trailer_key == "trailer-a" else 0.08

    for frame in range(frame_count):
        t = frame / sample_rate
        fade = min(1.0, t / 1.8, (duration - t) / 1.6)
        if t < 18:
            chord = (55.0, 82.41, 110.0)
        elif t < 31:
            chord = (48.99, 73.42, 98.0)
        elif t < LOGO_START:
            chord = (65.41, 98.0, 130.81)
        else:
            chord = (73.42, 110.0, 146.83)

        drift = 0.0
        for index, frequency in enumerate(chord):
            drift += math.sin(2 * math.pi * frequency * t + index * 0.7) / (index + 2)
        drift *= 0.10

        pulse_phase = t % 2.0
        pulse = 0.0
        if pulse_phase < 0.32:
            pulse = (
                math.sin(2 * math.pi * 46 * pulse_phase)
                * math.exp(-10 * pulse_phase)
                * 0.16
            )

        reveal = 0.0
        if 38.0 <= t <= INVITATION_START:
            reveal_envelope = math.sin(math.pi * (t - 38.0) / 6.0)
            reveal = (
                math.sin(2 * math.pi * 293.66 * t)
                + 0.6 * math.sin(2 * math.pi * 440.0 * t)
            ) * reveal_envelope * 0.035

        left = max(-1.0, min(1.0, (drift + pulse + reveal) * fade))
        right_drift = sum(
            math.sin(2 * math.pi * frequency * (t + phase_shift) + index * 0.7)
            / (index + 2)
            for index, frequency in enumerate(chord)
        ) * 0.10
        right = max(-1.0, min(1.0, (right_drift + pulse + reveal) * fade))
        audio.extend(struct.pack("<hh", int(left * 32767), int(right * 32767)))

    with wave.open(str(destination), "wb") as output:
        output.setnchannels(2)
        output.setsampwidth(2)
        output.setframerate(sample_rate)
        output.writeframes(audio)


def stage_sfx(project_root):
    source_root = Path("/Users/erdellmaurice-famu/.agents/skills/media-use/audio/assets/sfx")
    destination = project_root / "assets" / "audio" / "sfx"
    destination.mkdir(parents=True, exist_ok=True)
    for filename in ("impact-bass-1.mp3", "riser.mp3", "whoosh-cinematic.mp3", "chime.mp3"):
        shutil.copy2(source_root / filename, destination / filename)


def prepare_audio(trailer_key):
    project_root = CAMPAIGN_ROOT / "trailers" / trailer_key / "hyperframes"
    trailer_root = CAMPAIGN_ROOT / "trailers" / trailer_key
    manifest = json.loads((trailer_root / "voice" / "full-cast-manifest.json").read_text())
    lines = process_voice(project_root, trailer_root, manifest)
    build_original_score(
        project_root / "assets" / "audio" / "original-cinematic-score.wav",
        trailer_key,
    )
    stage_sfx(project_root)
    plan = {
        "trailer": trailer_key,
        "duration": RUNTIME,
        "score": "assets/audio/original-cinematic-score.wav",
        "lines": lines,
    }
    destination = project_root / "assets" / "audio" / "timing-plan.json"
    destination.write_text(f"{json.dumps(plan, indent=2)}\n")
    print(destination)


def group_words(lines, max_words=4):
    groups = []
    for line in lines:
        current = []
        for word in line["words"]:
            current.append(word)
            sentence_break = word["text"].endswith((".", "?", "!"))
            if len(current) >= max_words or sentence_break:
                groups.append(
                    {
                        "speaker": line["speaker"],
                        "start": current[0]["start"],
                        "end": current[-1]["end"],
                        "words": current,
                    }
                )
                current = []
        if current:
            groups.append(
                {
                    "speaker": line["speaker"],
                    "start": current[0]["start"],
                    "end": current[-1]["end"],
                    "words": current,
                }
            )
    return groups


def asset_filename(frame):
    if frame["art"] in {"campaign-close-card.png", "campaign-invitation-card.png"}:
        return frame["art"]
    return Path(frame["art"]).name


def headline_text(frame):
    return frame["onscreen"]


def build_composition(trailer_key):
    builder = load_campaign_builder()
    trailer = builder.TRAILERS[trailer_key]
    project_root = CAMPAIGN_ROOT / "trailers" / trailer_key / "hyperframes"
    timing = json.loads(
        (project_root / "assets" / "audio" / "word-timings.json").read_text()
    )
    plan = json.loads((project_root / "assets" / "audio" / "timing-plan.json").read_text())
    invitation_line = next(
        line for line in plan["lines"] if line["scene"] == "11-invitation-close"
    )
    invitation_end = invitation_line["start"] + invitation_line["duration"]
    groups = group_words(timing["lines"])

    scene_markup = []
    scene_script = []
    cursor = 0
    for index, (frame, duration) in enumerate(
        zip(trailer["frames"], builder.TRAILER_DURATIONS, strict=True),
        start=1,
    ):
        start = cursor
        cursor += duration
        scene_id = f"scene-{index:02d}"
        image_id = f"{scene_id}-image"
        body_id = f"{scene_id}-body"
        if frame["title"] == "Launch ask":
            card_class = " scene-card scene-open"
        elif frame["title"] == "Series reveal":
            card_class = " scene-card scene-logo"
        elif frame["title"] == "Invitation close":
            card_class = " scene-card scene-invitation"
        else:
            card_class = ""
        object_position = "center center"
        is_card = bool(card_class)
        drift_x = 0 if is_card else (-22 if index % 2 else 22)
        drift_y = 0 if is_card else (-12 if index % 3 == 0 else 8)
        if frame["title"] == "Series reveal":
            start_scale, end_scale = 0.94, 0.90
        elif is_card:
            start_scale, end_scale = 0.98, 0.94
        else:
            start_scale, end_scale = 1.13, 1.025
        scene_markup.append(
            f"""
      <section id="{scene_id}" class="clip scene{card_class}" data-start="{start}" data-duration="{duration}" data-track-index="1">
        <div id="{body_id}" class="scene-body">
          <div class="image-stage" data-layout-allow-overflow="true">
            <img id="{image_id}" src="assets/images/{html.escape(asset_filename(frame))}" alt="">
            <div class="image-vignette"></div>
          </div>
          <div class="scene-copy">
            <div class="scene-number">{index:02d} / 11</div>
            <div class="scene-headline">{html.escape(headline_text(frame))}</div>
          </div>
          <div class="registration-mark" aria-hidden="true"></div>
        </div>
      </section>"""
        )
        scene_script.append(
            f"""
      tl.fromTo("#{body_id}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.22, ease: "power2.out" }}, {start});
      tl.fromTo("#{image_id}", {{ scale: {start_scale}, x: {-drift_x}, y: {-drift_y} }},
        {{ scale: {end_scale}, x: {drift_x}, y: {drift_y}, duration: {duration}, ease: "none" }}, {start});
      tl.to("#{body_id}", {{ opacity: 0, duration: 0.18, ease: "power2.in" }}, {start + duration - 0.18});
      tl.set("#{body_id}", {{ opacity: 0 }}, {start + duration});"""
        )

    caption_markup = []
    caption_script = []
    for group_index, group in enumerate(groups):
        group_id = f"caption-group-{group_index:02d}"
        words = []
        for word_index, word in enumerate(group["words"]):
            word_id = f"{group_id}-word-{word_index:02d}"
            words.append(f'<span id="{word_id}">{html.escape(word["text"])}</span>')
            caption_script.append(
                f"""
      tl.set("#{word_id}", {{ color: "#ffffff", backgroundColor: "#215732", scale: 1 }}, {word["start"]});
      tl.set("#{word_id}", {{ color: "#ffffff", backgroundColor: "transparent", scale: 1 }}, {word["end"]});"""
            )
        caption_markup.append(
            f"""
          <div id="{group_id}" class="caption-group">
            <div class="speaker-label">{html.escape(group["speaker"].upper())}</div>
            <div class="caption-words">{' '.join(words)}</div>
          </div>"""
        )
        caption_script.append(
            f"""
      tl.set("#{group_id}", {{ visibility: "visible", opacity: 0, y: 16 }}, {group["start"]});
      tl.to("#{group_id}", {{ opacity: 1, y: 0, duration: 0.16, ease: "power2.out" }}, {group["start"]});
      tl.to("#{group_id}", {{ opacity: 0, y: -8, duration: 0.12, ease: "power2.in" }}, {max(group["end"] - 0.12, group["start"] + 0.18)});
      tl.set("#{group_id}", {{ opacity: 0, visibility: "hidden" }}, {group["end"]});"""
        )

    voice_audio = []
    for index, line in enumerate(plan["lines"]):
        voice_audio.append(
            f"""
      <audio id="voice-{index:02d}" src="{html.escape(line["file"])}" data-start="{line["start"]}" data-duration="{line["duration"]}" data-track-index="11" data-volume="1"></audio>"""
        )

    title = html.escape(trailer["title"])
    composition_id = f"formula-launch-{trailer_key}"
    document = f"""<!DOCTYPE html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1080, height=1920">
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #071a36; }}
      body {{ color: #f5e7cd; font-family: "Montserrat", sans-serif; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; }}
      .scene {{ position: absolute; inset: 0; overflow: hidden; background: #071a36; }}
      .scene-body {{ position: absolute; inset: 0; overflow: hidden; background: #071a36; opacity: 0; }}
      .image-stage {{ position: absolute; inset: 0 0 330px; overflow: hidden; background: #071a36; }}
      .image-stage img {{ width: 100%; height: 100%; object-fit: cover; object-position: center; display: block; transform-origin: center; }}
      .scene-card .image-stage {{ inset: 0; display: grid; place-items: center; }}
      .scene-card .image-stage img {{ width: auto; height: 100%; max-width: 100%; object-fit: contain; }}
      .scene-card .image-vignette {{ display: none; }}
      .scene-open .image-stage, .scene-invitation .image-stage {{ inset: 0 0 360px; }}
      .image-vignette {{ position: absolute; inset: 0; background:
        linear-gradient(180deg, rgba(7,26,54,.62) 0%, transparent 22%, transparent 66%, rgba(7,26,54,.94) 100%),
        linear-gradient(90deg, rgba(7,26,54,.28), transparent 30%, transparent 70%, rgba(7,26,54,.28)); }}
      .scene-copy {{ position: absolute; left: 58px; right: 58px; top: 72px; z-index: 3; }}
      .scene-number {{ color: #f0a05b; font-size: 22px; font-weight: 800; letter-spacing: .18em; }}
      .scene-headline {{ margin-top: 18px; max-width: 820px; white-space: pre-line; font-size: 72px; line-height: .94;
        font-weight: 900; letter-spacing: -.035em; text-transform: uppercase; text-shadow: 0 3px 24px rgba(7,26,54,.9); }}
      .scene-card .scene-copy {{ display: none; }}
      .registration-mark {{ position: absolute; right: 38px; top: 40px; width: 28px; height: 28px;
        border-top: 3px solid #c9793d; border-right: 3px solid #c9793d; z-index: 4; }}
      #caption-rail {{ position: absolute; left: 0; right: 0; bottom: 0; height: 360px; z-index: 20;
        display: flex; align-items: center; justify-content: center; padding: 38px 58px 64px;
        background: linear-gradient(180deg, rgba(7,26,54,.72), #071a36 24%); border-top: 3px solid rgba(201,121,61,.78); }}
      .caption-group {{ position: absolute; left: 58px; right: 58px; top: 54px; min-height: 210px;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        visibility: hidden; opacity: 0; text-align: center; }}
      .speaker-label {{ margin-bottom: 12px; color: #f0a05b; font-size: 21px; line-height: 1; font-weight: 900; letter-spacing: .18em; }}
      .caption-words {{ max-width: 940px; color: white; font-size: 61px; line-height: 1.08; font-weight: 850;
        letter-spacing: -.025em; text-wrap: balance; text-shadow: 0 3px 18px rgba(0,0,0,.7); }}
      .caption-words span {{ display: inline-block; padding: .02em .08em; border-radius: .14em;
        background: transparent; transform-origin: center bottom; }}
      #close-disclosure {{ position: absolute; left: 58px; right: 58px; bottom: 24px; z-index: 26;
        visibility: hidden; opacity: 0; color: #c9d1dc; font-size: 19px; line-height: 1.1;
        font-weight: 750; letter-spacing: .065em; text-align: center; text-transform: uppercase;
        text-shadow: 0 3px 18px rgba(0,0,0,.7); }}
      #final-cta {{ position: absolute; left: 58px; right: 58px; top: 68px; z-index: 26;
        visibility: hidden; opacity: 0; text-align: center; text-transform: uppercase; }}
      #final-cta strong {{ display: block; color: #fff8ea; font-size: 54px; line-height: 1;
        font-weight: 900; letter-spacing: .035em; text-shadow: 0 3px 18px rgba(0,0,0,.7); }}
      #final-cta span {{ display: block; margin-top: 24px; color: #f0a05b; font-size: 21px;
        line-height: 1.15; font-weight: 850; letter-spacing: .09em; }}
      .series-tag {{ position: absolute; left: 58px; right: 58px; bottom: 28px; z-index: 25;
        color: #c9d1dc; font-size: 18px; font-weight: 700; letter-spacing: .08em; text-align: center; text-transform: uppercase; }}
      .grain {{ position: absolute; inset: 0; z-index: 30; opacity: .055;
        background-image: repeating-linear-gradient(0deg, transparent 0, transparent 3px, rgba(255,255,255,.18) 4px); }}
    </style>
  </head>
  <body>
    <main id="root" data-composition-id="{composition_id}" data-start="0" data-duration="{RUNTIME}" data-width="1080" data-height="1920">
      {''.join(scene_markup)}
      <section id="caption-rail" class="clip" data-start="0" data-duration="{RUNTIME}" data-track-index="20" data-layout-allow-caption-zone="true">
        {''.join(caption_markup)}
        <div id="final-cta"><strong>Begins July 31</strong><span>Presented by the Mathematics Department</span></div>
        <div id="close-disclosure">Video voiceovers use AI-generated voices.</div>
        <div class="series-tag">The Formula of Becoming | Presented by the Mathematics Department</div>
      </section>
      <div id="grain" class="clip grain" data-start="0" data-duration="{RUNTIME}" data-track-index="30" data-layout-allow-overflow="true"></div>
      <audio id="score" src="assets/audio/original-cinematic-score.wav" data-start="0" data-duration="{RUNTIME}" data-track-index="10" data-volume="0.24"></audio>
      {''.join(voice_audio)}
      <audio id="impact-open" src="assets/audio/sfx/impact-bass-1.mp3" data-start="0" data-duration="1.5" data-track-index="12" data-volume="0.22"></audio>
      <audio id="story-whoosh" src="assets/audio/sfx/whoosh-cinematic.mp3" data-start="3.8" data-duration="1.2" data-track-index="13" data-volume="0.14"></audio>
      <audio id="reveal-riser" src="assets/audio/sfx/riser.mp3" data-start="38.2" data-duration="1.6" data-track-index="14" data-volume="0.18"></audio>
      <audio id="logo-whoosh" src="assets/audio/sfx/whoosh-cinematic.mp3" data-start="39.8" data-duration="1.2" data-track-index="15" data-volume="0.16"></audio>
      <audio id="close-chime" src="assets/audio/sfx/chime.mp3" data-start="44" data-duration="1.5" data-track-index="16" data-volume="0.16"></audio>
    </main>
    <script>
      window.__timelines = window.__timelines || {{}};
      var tl = gsap.timeline({{ paused: true }});
      {''.join(scene_script)}
      tl.to("#caption-rail", {{ opacity: 0, duration: 0.2, ease: "power2.in" }}, 39.8);
      tl.set("#caption-rail", {{ opacity: 0 }}, 40);
      tl.set("#caption-rail", {{ opacity: 0 }}, 44);
      tl.to("#caption-rail", {{ opacity: 1, duration: 0.2, ease: "power2.out" }}, 44);
      {''.join(caption_script)}
      tl.to(".series-tag", {{ opacity: 0, duration: 0.15, ease: "power2.in" }}, 44);
      tl.set("#close-disclosure", {{ visibility: "visible", opacity: 0, y: 6 }}, 44.12);
      tl.to("#close-disclosure", {{ opacity: 1, y: 0, duration: 0.18, ease: "power2.out" }}, 44.12);
      tl.set("#final-cta", {{ visibility: "visible", opacity: 0, y: 8 }}, {invitation_end + 0.08:.2f});
      tl.to("#final-cta", {{ opacity: 1, y: 0, duration: 0.22, ease: "power2.out" }}, {invitation_end + 0.08:.2f});
      window.__timelines["{composition_id}"] = tl;
    </script>
  </body>
</html>
"""
    (project_root / "index.html").write_text(document)
    (project_root / "caption-overrides.json").write_text("[]\n")
    storyboard = project_root / "STORYBOARD.md"
    storyboard.write_text(storyboard.read_text().replace("- status: built", "- status: animated"))
    audio_meta = {
        "duration": RUNTIME,
        "score": plan["score"],
        "score_provenance": "Original deterministic procedural instrumental generated for this campaign.",
        "voice_model": "gpt-4o-mini-tts",
        "word_timing_model": timing["model"],
        "lines": plan["lines"],
        "captions": "assets/audio/word-timings.json",
    }
    (project_root / "audio_meta.json").write_text(f"{json.dumps(audio_meta, indent=2)}\n")
    print(project_root / "index.html")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("trailer", choices=("trailer-a", "trailer-b"))
    parser.add_argument("--prepare-audio", action="store_true")
    parser.add_argument("--compose", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.prepare_audio and not args.compose:
        raise SystemExit("Choose --prepare-audio or --compose")
    if args.prepare_audio:
        prepare_audio(args.trailer)
    if args.compose:
        build_composition(args.trailer)


if __name__ == "__main__":
    main()
