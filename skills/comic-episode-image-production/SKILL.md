---
name: comic-episode-image-production
description: "Create and package a polished comic episode as a three-section release from an approved McCall-Hart University storyboard: title card, lettered story page, and approved message card. Use the current v2 continuity assets and a two-pass art-then-lettering workflow. Refuse image production while the repository approval gate is closed."
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

## Produce the Story Page

Default to one image containing the full four-panel episode page unless the user explicitly requests a single panel.

1. Identify the episode purpose, emotional turn, four panel visuals, and exact text.
2. Create a first-pass prompt for one four-panel page.
3. Preserve panel order, clean gutters, phone readability, character continuity, and negative space.
4. Generate art without dialogue, captions, logos, or incidental text.
5. Inspect the page for continuity and staging.
6. Edit the same page in a second pass to add exact dialogue and captions.
7. Inspect lettering for spelling, balloon order, face clearance, and mobile legibility.

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
- Use modern animated comic, clean semi-cartoon linework, expressive faces, soft shading, and readable staging.
- Keep the result G-rated and grounded.
- Do not render text in pass one.
- Do not invent dialogue, institution names, signs, or logos.

Read `references/prompt-template.md` when constructing the two image prompts.

## Lettering Rules

- Add text only in pass two unless the user explicitly requests one-pass lettering.
- Use white balloons, clean outlines, crisp black lettering, and restrained caption boxes.
- Preserve storyboard wording exactly unless the user asks for a dialogue revision.
- Keep reading order unambiguous and do not cover faces, hands, equations, or essential props.

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
