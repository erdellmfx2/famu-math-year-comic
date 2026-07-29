---
name: comic-episode-image-production
description: "Create and package a polished comic episode as a three-section release from an approved McCall-Hart University storyboard: title card, lettered story page, and approved message card. Use current v2 continuity assets, a dialogue-first balloon map, and a per-image art-then-lettering quality loop. Refuse image production while the repository approval gate is closed."
---

# Comic Episode Image Production

## Check the Gate First

Read `story/approval_status.json` before opening a storyboard or calling an image tool.

Proceed only when both are true:

- `script_approved` is `true`
- `comic_production_allowed` is `true`

If either value is false, stop image production and report that script approval is still required. Do not create a sample, storyboard, prompt pack, panel, or page as a workaround.

## Read Current Sources

After the gate is open, read:

1. `story/setting_bible_v2.md`
2. `story/character_bible_v2.md`
3. `art/style_guide.md`
4. The target storyboard under `art/storyboards/week-XX/`
5. Current v2 continuity assets under `art/final/`

Never use files under any `archive/` path as visual references. They preserve obsolete continuity and institutional identity.

## Plan Lettering Before Art

Before generating or editing a story-page image, write a balloon map in the
target storyboard. It is a layout plan, not text to render in pass one. For
every spoken line or narration box, record:

1. Panel number and reading order.
2. Exact source-faithful text and speaker or narrator.
3. Approximate text length: short (1-8 words), medium (9-18), long (19-32),
   or split/repage (more than 32 words).
4. Balloon or caption type, estimated footprint, and reserved panel area.
5. The speaker's visible face/mouth target and the tail path.

Use the map to decide whether the scene needs a larger panel, a less crowded
shot, a separate page, or a shorter source-approved turn. Do not shrink type
below phone-readable scale or force more than one speaker turn into a balloon
to make text fit. If a line needs more room than its panel can safely reserve,
move that beat to another panel or page before artwork begins.

## Produce the Story Page

Default to one image containing the full four-panel episode page unless the user explicitly requests a single panel.

1. Identify the episode purpose, emotional turn, panel visuals, exact text,
   and approved balloon map.
2. Create a first-pass prompt for one four-panel page that names each panel's
   reserved lettering area and keeps faces, hands, equations, and decisive
   props outside it.
3. Preserve panel order, clean gutters, phone readability, character
   continuity, and the mapped negative space.
4. Generate art without dialogue, captions, logos, or incidental text.
5. Run the pre-lettering balloon check below. Re-compose this image before
   lettering if even one mapped balloon cannot fit inside its panel without
   covering a story principle or leaving its speaker unclear.
6. Edit the same accepted page in a second pass to add exact dialogue and
   captions, using the mapped placements and speaker tails.
7. Run the final balloon check immediately after this lettering edit. Fix the
   same page before moving to another image; do not defer balloon review to a
   batch-level finishing pass.

Apply `skills/comic-lettering-continuity/SKILL.md` for all title cards,
lettering, character-separation checks, page marks, and release packaging.
Treat any balloon or caption overlapping a face as a failed page that must be
re-lettered before packaging.

## Per-Image Balloon Check

Run this check after every generated or edited story-page image, including
replacement versions:

- Each mapped balloon or caption has a visible, protected place in its own
  panel; dialogue balloons never live outside the comic page as a workaround.
- The image composition leaves the reserved area genuinely empty. A plain
  wall, sky, desk surface, or non-story background is acceptable; a face,
  hand, equation, decisive prop, action, or setting clue is not.
- A reader can identify the speaker from the visible character and a clear
  mouth-directed tail. Reframe or separate the speakers if this is ambiguous.
- Balloon bodies remain inside their own panel. They may cross a gutter only
  when both panels belong to the same uninterrupted speaker turn and no
  reading order or speaker ambiguity results.
- Text is readable at phone size. Split a crowded exchange across panels or
  pages rather than shrinking lettering or stacking balloons over art.
- The approved page-mark corner remains free.

Any failed check requires a targeted re-composition or lettering edit of that
one page, followed by this check again. Only a passing page can advance.

## Continuity Rules

- Setting: Fictional McCall-Hart University in Bellwether, Alabama
- Palette: Indigo, copper, cream, cypress gray, warm limestone, and dark walnut
- Campus: Honey brick, pale limestone, wrought iron, live oaks, magnolias, cypress trees, and copper sunset light
- Identity: Great blue heron mark and Herons athletics only when a mark is necessary
- Malik: Indigo, cream, charcoal, and muted copper; composed posture and dry warmth
- Nia: Copper, cream, indigo accents, denim, and warm brown; open and expressive posture
- Avoid: Green-and-orange legacy identity, snake mascots, real-university marks, real-university buildings, and archived visual assets

## Prompt Rules

- Say `one finished four-panel comic page` for combined-page output.
- Keep one main story beat per panel.
- Describe only characters and locations required by the storyboard.
- State each panel's reserved balloon or caption zone and place all important
  faces and action outside that zone. Do not ask the image model to draw
  placeholder balloons, empty boxes, text, or guides in pass one.
- Use modern animated comic, clean semi-cartoon linework, expressive faces, soft shading, and readable staging.
- Keep the result G-rated and grounded.
- Do not render text in pass one.
- Do not invent dialogue, institution names, signs, or logos.

Read `references/prompt-template.md` when constructing the two image prompts.

## Lettering Rules

Follow `skills/comic-lettering-continuity/SKILL.md` without substitutions.
Use the accepted unlettered image as the base and preserve its panel order,
character designs, composition, props, and lighting. Run the per-image balloon
check after every lettering edit before continuing.

## Package the Three-Section Release

After the story page passes review, package the episode under
`art/final/week-XX/episode-YY/sequence/` in this exact reading order:

1. `01-title-card-v1.png`: Start with the approved series logo. Add the exact
   weekly title from `story/timeline-weeks/XX.md` as the arc title, followed by
   `PART N`, where `N` is the episode's one-indexed day within that week.
2. `02-comic-page-v1.png`: Place the approved lettered comic itself here. For
   episodes needing several story pages, number them consecutively after the
   title card and before the closing card.
3. `03-<approved-message>-end-card-v1.png`: End with exactly one approved
   message card selected from `art/final/series-endcards/approved/`.

Use the title card only for series and arc information. Do not invent an arc
title, part number, university identity, or promotional language. Preserve the
approved wording and artwork of the closing card.

## Output Rule

Save approved v2 outputs under `art/final/` using week and episode folders.
Never write new output into an archive path. Add a short `sequence/README.md`
recording the title card, story page or pages, and closing card used.

## Series Mark and Closing Card

Use the approved transparent page mark at
`art/final/series-endcards/approved/formula-of-becoming-famu-math-page-mark-v1.png`
at the bottom-right of every final comic page. Keep it small, legible, and clear
of lettering and decisive art. It contains plain-text FAMU Mathematics Department
attribution and is not an official FAMU mark.

Use one approved closing card from `art/final/series-endcards/approved/` as
the last section of every release. Do not invent a new advertising message or
use review assets.
