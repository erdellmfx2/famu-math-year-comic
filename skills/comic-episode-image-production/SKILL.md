---
name: comic-episode-image-production
description: Create polished 4-panel comic episode page images from FAMU Math Year Comic storyboard files in `art/storyboards/`, using the art style guide, asset references, and a two-pass image workflow of page generation followed by lettering/dialogue integration. Use when the user wants a storyboard turned into a comic page image or wants the comic-image production workflow reused consistently across episodes.
---

# Comic Episode Image Production

Use this skill when converting one storyboard file into one finished comic page image.

## Inputs to read first

1. `art/style_guide.md`
2. The target storyboard in `art/storyboards/`
3. Relevant continuity assets in `art/final/` when the storyboard depends on character or location consistency

## Output target

Produce one single image that contains the full 4-panel episode page unless the user explicitly asks for separate panel files.

## Default workflow

1. Read the storyboard and identify:
   - episode purpose
   - emotional arc
   - all 4 panel visuals
   - all dialogue/captions
2. Build a first-pass prompt for a **single 4-panel comic page**:
   - preserve panel order
   - keep gutters clean
   - optimize for phone readability
   - preserve FAMU environment, Malik/Nia continuity, and negative space for lettering
   - do **not** render text in pass one
3. Generate the page image.
4. Build a second-pass edit prompt against that page:
   - preserve the exact artwork and layout
   - add dialogue balloons and caption boxes
   - keep lettering crisp and readable
   - avoid covering faces, props, or key storytelling
5. Generate the lettered version.

## Prompt rules

- Always describe the result as a **single finished 4-panel comic page** when using the combined-page approach.
- Keep one main emotional beat per panel.
- Reuse the style language from `art/style_guide.md`:
  - modern animated comic
  - youth / young adult
  - G-rated
  - clean semi-cartoon linework
  - expressive faces
  - soft shading
  - vibrant but balanced greens, oranges, golds, neutrals
  - hopeful, grounded, energetic, academic, communal
- For Malik:
  - composed, structured, slightly reserved
  - deep green / charcoal / white palette
- For Nia:
  - bright curiosity, warm confidence
  - orange with green accents, denim or neutral base
- Always preserve FAMU campus warmth: red brick, green lawns, student movement, HBCU community spirit.

## Lettering rules

- Add text only in the second pass unless the user explicitly asks for one-pass lettering.
- Use:
  - white speech balloons with clean outlines
  - crisp black lettering
  - polished caption boxes
- Keep text concise and verbatim from the storyboard unless the user asks for edits.

## Deliverable notes

- If the user says “create a picture for the storyboard,” default to a full episode page, not a single isolated panel.
- If the user says “panel 1” or similar, create only that panel.
