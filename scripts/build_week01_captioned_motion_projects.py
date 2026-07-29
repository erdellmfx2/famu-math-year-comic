#!/usr/bin/env python3
"""Build local HyperFrames projects from approved Week 1 audio and comic assets."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TITLE_SECONDS = 5.0
END_SECONDS = 7.0


def duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nk=1:nw=1", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def panels(specification: str) -> list[tuple[int, int]]:
    page_text, panel_text = specification.split("-panels-") if "-panels-" in specification else specification.split("-panel-")
    page = int(page_text.split("-")[-1])
    values = panel_text.split("-")
    if len(values) == 1:
        return [(page, int(values[0]))]
    first, last = int(values[0]), int(values[-1])
    return [(page, panel) for panel in range(first, last + 1)]


def copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def visual_markup(visuals: list[dict]) -> str:
    lines = []
    for index, visual in enumerate(visuals, start=1):
        page = "page-one" if visual["page"] == 1 else "page-two"
        panel = f"panel-{visual['panel']}"
        lines.extend([
            f'      <div id="visual-{index}" class="clip scene" data-start="{visual["start"]:.3f}" data-duration="{visual["duration"]:.3f}" data-track-index="{index + 1}">',
            f'        <div class="story-blur {page} {panel}" data-layout-ignore></div>',
            f'        <div class="story-card {page} {panel}" data-layout-allow-overflow></div>',
            '        <div class="story-vignette" data-layout-ignore></div>',
            '      </div>',
        ])
    return "\n".join(lines)


def audio_markup(scenes: list[dict]) -> str:
    return "\n".join(
        f'      <audio id="audio-{scene["id"]}" class="clip" data-start="{scene["audio_start"]:.3f}" data-duration="{scene["duration"]:.3f}" data-track-index="{100 + index}" src="assets/audio/{scene["id"]}.mp3" data-volume="1"></audio>'
        for index, scene in enumerate(scenes)
    )


def animation_markup(visuals: list[dict]) -> str:
    rows = [
        '      const tl = gsap.timeline({ paused: true });',
        '      const enter = (selector, start) => tl.fromTo(selector, { opacity: 0 }, { opacity: 1, duration: 0.55, ease: "power2.inOut" }, start);',
        '      const move = (selector, start, duration, from, to) => tl.fromTo(selector, from, { ...to, duration, ease: "sine.inOut" }, start);',
        '      tl.fromTo("#title-card", { opacity: 0 }, { opacity: 1, duration: 0.7, ease: "power2.out" }, 0.2);',
    ]
    drifts = [(16, 10, -3, -2), (-14, 9, 3, -2), (12, -9, -2, 2), (-10, 8, 2, -2)]
    for index, visual in enumerate(visuals, start=1):
        x1, y1, x2, y2 = drifts[(index - 1) % len(drifts)]
        rows.append(f'      enter("#visual-{index}", {visual["start"]:.3f});')
        rows.append(
            f'      move("#visual-{index} .story-card", {visual["start"] + 0.05:.3f}, {max(0.3, visual["duration"] - 0.1):.3f}, {{ scale: 1.10, x: {x1}, y: {y1} }}, {{ scale: 1, x: {x2}, y: {y2} }});'
        )
    rows.extend([
        '      enter("#message-card", MESSAGE_START);',
        '      tl.to("#message-card .final-indigo", { opacity: 1, duration: 0.75, ease: "power2.in" }, MESSAGE_START + 5.25);',
        '      groups.forEach((group, groupIndex) => {',
        '        const groupSelector = `#caption-group-${groupIndex}`;',
        '        tl.set(groupSelector, { opacity: 1, visibility: "visible", y: 0 }, group.show);',
        '        group.words.forEach((word, wordIndex) => {',
        '          const wordSelector = `#caption-word-${groupIndex}-${wordIndex}`;',
        '          tl.set(wordSelector, { backgroundColor: "#215732", boxShadow: "0 0 0 3px rgba(255,255,255,0.24)", scale: 1.055 }, word.start);',
        '          tl.set(wordSelector, { backgroundColor: "rgba(33,87,50,0)", boxShadow: "0 0 0 0 rgba(255,255,255,0)", scale: 1 }, word.end);',
        '        });',
        '        tl.set(groupSelector, { opacity: 0, visibility: "hidden" }, group.hide);',
        '      });',
        '      tl.seek(0);',
        '      window.__timelines[COMPOSITION_ID] = tl;',
    ])
    return "\n".join(rows)


def html(day: int, total: float, message_start: float, visuals: list[dict], scenes: list[dict]) -> str:
    composition = f"week-01-day-{day:02d}"
    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <script src="assets/captions-data.js"></script>
    <style>
      :root {{ --indigo:#07172e; --green:#215732; --white:#fff; }}
      * {{ box-sizing:border-box; margin:0; padding:0; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:var(--indigo); }}
      #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; isolation:isolate; }}
      .scene {{ position:absolute; inset:0; overflow:hidden; background:var(--indigo); opacity:0; }}
      .card-image {{ position:absolute; inset:0; width:100%; height:100%; object-fit:contain; }}
      .story-blur {{ position:absolute; inset:-120px; background-repeat:no-repeat; background-size:auto 400%; filter:blur(34px) saturate(.82) brightness(.62); transform:scale(1.16); }}
      .story-card {{ position:absolute; left:0; top:675px; width:1080px; height:570px; background-repeat:no-repeat; background-size:100% 400%; box-shadow:0 0 0 3px rgba(241,226,195,.92),0 28px 72px rgba(7,23,46,.62); will-change:transform; }}
      .page-one {{ background-image:url("assets/comic-page-01.png"); }} .page-two {{ background-image:url("assets/comic-page-02.png"); }}
      .panel-1 {{ background-position:center 0%; }} .panel-2 {{ background-position:center 33.333%; }} .panel-3 {{ background-position:center 66.667%; }} .panel-4 {{ background-position:center 100%; }}
      .story-vignette {{ position:absolute; inset:0; background:linear-gradient(180deg,rgba(7,23,46,.28),transparent 28%,transparent 72%,rgba(7,23,46,.34)),radial-gradient(circle at center,transparent 30%,rgba(7,23,46,.22) 100%); pointer-events:none; }}
      .final-indigo {{ position:absolute; inset:0; background:var(--indigo); opacity:0; pointer-events:none; }}
      #caption-layer {{ position:absolute; left:54px; right:54px; bottom:235px; height:230px; z-index:100; display:flex; align-items:center; justify-content:center; pointer-events:none; }}
      .caption-group {{ position:absolute; left:0; right:0; min-height:92px; display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:2px 4px; padding:16px 22px; border:2px solid rgba(255,255,255,.16); border-radius:22px; background:rgba(7,23,46,.82); box-shadow:0 14px 44px rgba(0,0,0,.38); color:var(--white); font-family:Montserrat,sans-serif; font-size:58px; font-weight:800; line-height:1.12; letter-spacing:-1px; text-align:center; text-shadow:0 2px 7px rgba(0,0,0,.92); opacity:0; visibility:hidden; }}
      .caption-word {{ display:inline-block; padding:4px 8px 6px; border-radius:10px; color:var(--white); background:rgba(33,87,50,0); transform-origin:center; will-change:transform,background-color,box-shadow; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="{composition}" data-start="0" data-duration="{total:.3f}" data-width="1080" data-height="1920">
      <div id="title-card" class="clip scene" data-start="0" data-duration="5" data-track-index="1"><img class="card-image" src="assets/title-card.png" alt="" data-layout-allow-overflow /></div>
{visual_markup(visuals)}
      <div id="message-card" class="clip scene" data-start="{message_start:.3f}" data-duration="7" data-track-index="90"><img class="card-image" src="assets/message-card.png" alt="" data-layout-allow-overflow /><div class="final-indigo" data-layout-ignore></div></div>
{audio_markup(scenes)}
      <div id="caption-layer" data-layout-allow-overlap></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const COMPOSITION_ID = "{composition}";
      const MESSAGE_START = {message_start:.3f};
      const groups = window.CAPTION_GROUPS || [];
      const captionLayer = document.getElementById("caption-layer");
      groups.forEach((group, groupIndex) => {{
        const groupElement = document.createElement("div"); groupElement.id = `caption-group-${{groupIndex}}`; groupElement.className = "caption-group"; groupElement.setAttribute("data-layout-allow-overlap", "");
        group.words.forEach((word, wordIndex) => {{ const element = document.createElement("span"); element.id = `caption-word-${{groupIndex}}-${{wordIndex}}`; element.className = "caption-word"; element.textContent = word.text; groupElement.appendChild(element); }});
        captionLayer.appendChild(groupElement);
      }});
{animation_markup(visuals)}
    </script>
  </body>
</html>
'''


def main() -> None:
    for day in (5, 6, 7):
        directory = ROOT / "video" / f"week-01-day-{day:02d}"
        manifest = json.loads((directory / "full-cast-manifest.json").read_text())
        scenes = []
        cursor = TITLE_SECONDS
        visuals = []
        for scene in manifest["scenes"]:
            track = directory / "audio-full-cast" / "scenes" / f"{scene['id']}.mp3"
            scene_duration = duration(track)
            scenes.append({"id": scene["id"], "audio_start": round(cursor, 3), "duration": round(scene_duration, 3)})
            panel_list = panels(scene["panel"])
            visual_duration = scene_duration / len(panel_list)
            for panel_index, (page, panel) in enumerate(panel_list):
                visuals.append({"page": page, "panel": panel, "start": round(cursor - 0.55 + panel_index * visual_duration, 3), "duration": round(visual_duration + 0.55, 3)})
            cursor += scene_duration
        message_start = cursor
        total = message_start + END_SECONDS
        (directory / "caption-timing-manifest.json").write_text(json.dumps({"scenes": [{"id": item["id"], "audio_start": item["audio_start"]} for item in scenes]}, indent=2) + "\n")
        sequence = ROOT / "art" / "final" / "week-01" / f"episode-{day:02d}" / "sequence-v2"
        project = directory / "hyperframes"
        assets = project / "assets"
        copy(sequence / "01-title-card-v1.png", assets / "title-card.png")
        end_card = next(sequence.glob("04-*-end-card-v1.png"))
        copy(end_card, assets / "message-card.png")
        copy(ROOT / "art" / "final" / "week-01" / f"episode-{day:02d}" / f"week-01-episode-{day:02d}-art-v1.png", assets / "comic-page-01.png")
        copy(ROOT / "art" / "final" / "week-01" / f"episode-{day:02d}" / f"week-01-episode-{day:02d}-page-02-art-v1.png", assets / "comic-page-02.png")
        copy(ROOT / "video" / "week-01-day-04" / "hyperframes" / "assets" / "gsap.min.js", assets / "gsap.min.js")
        (assets / "captions-data.js").write_text("window.CAPTION_GROUPS = [];\n")
        for scene in scenes:
            copy(directory / "audio-full-cast" / "scenes" / f"{scene['id']}.mp3", assets / "audio" / f"{scene['id']}.mp3")
        (project / "index.html").write_text(html(day, total, message_start, visuals, scenes))
        (project / "hyperframes.json").write_text('{"media":{"autoProxy":true}}\n')
        (project / "package.json").write_text(json.dumps({"name": f"week-01-day-{day:02d}-hyperframes", "private": True, "type": "module", "scripts": {"check": "npx --yes hyperframes@0.7.76 check", "render": "npx --yes hyperframes@0.7.76 render"}}, indent=2) + "\n")
        (project / "caption-overrides.json").write_text("{}\n")
        (project / "index.motion.json").write_text(json.dumps({"duration": round(total, 3), "maxStaticSec": 2, "assertions": [{"kind": "appearsBy", "selector": "#title-card", "bySec": 1.5}, {"kind": "before", "a": "#title-card", "b": "#visual-1"}]}, indent=2) + "\n")
        plan_rows = ["# Scene Plan", "", "| Scene | Audio start | Duration | Visual source |", "| --- | ---: | ---: | --- |"]
        for scene in scenes:
            plan_rows.append(f"| {scene['id']} | {scene['audio_start']:.3f} | {scene['duration']:.3f} | Approved unlettered panel sequence |")
        plan_rows.extend(["", f"Narration ends at {message_start:.3f} seconds; the approved closing card holds for 7 seconds."])
        (directory / "scene-plan.md").write_text("\n".join(plan_rows) + "\n")
        print(f"Built Day {day}: {total:.3f}s with {len(visuals)} story visuals")


if __name__ == "__main__":
    main()
