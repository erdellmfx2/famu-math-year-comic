---
name: comic-episode-image-production
description: Create one polished, lettered 4-panel comic page from an approved McCall-Hart University episode storyboard, using current v2 continuity assets and a two-pass art-then-lettering workflow. Use when the user asks to turn an approved storyboard into a comic page or reuse the established episode-image process. Refuse image production while the repository approval gate is closed.
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

## Produce One Page

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

## Output Rule

Save approved v2 outputs under `art/final/` using week and episode folders. Never write new output into an archive path.
