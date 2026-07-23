---
name: comic-week-generator
description: Build a complete, consistent weekly comic package from approved McCall-Hart story sources. Use when Codex needs to adapt a timeline week and its prose into every daily episode's storyboard and finished lettered comic page, especially when location transitions, character continuity, source-faithful dialogue, and visual-quality checks must remain consistent across a week.
---

# Comic Week Generator

Create a coherent seven-day comic sequence, not a disconnected batch of images. Plan the week as one story unit; generate and letter each daily page as a deliberate part of that unit.

## Confirm Production Is Open

Read `story/approval_status.json` before creating, revising, or generating any comic artifact.

Proceed only when both values are `true`:

- `script_approved`
- `comic_production_allowed`

If either is false, do not create storyboards, prompts, panels, or comic pages. Report the approval state instead.

## Build Grounded Context

Read these active v2 sources before outlining the week:

1. `story/timeline-weeks/<week>.md` for daily events, required turning points, and handoff continuity.
2. `story/timeline-weeks-prose-v2/prose_<week>.md` for character voice, scene texture, and source-faithful dialogue or captions.
3. `story/setting_bible_v2.md` for fictional McCall-Hart place identity.
4. `story/character_bible_v2.md` for arcs, relationship guardrails, and character behavior.
5. `art/style_guide.md` for visual and lettering rules.
6. `art/final/foundational-assets/coordinate-registry.md` for stable visual references.
7. Existing active v2 pages under `art/final/` when they establish immediate visual continuity.

Never use paths under `archive/` as visual or story sources. Do not use real university names, logos, buildings, green-and-orange identity, or snake imagery.

## Plan the Week First

Create or update `art/storyboards/week-XX/README.md` before generating pages. Map every daily episode in a compact table with its title, purpose, and setting progression.

For every episode, identify:

- Its required event from the timeline.
- The emotional turn drawn from the prose.
- Exact dialogue or captions selected from the prose.
- The primary setting and each meaningful location change.
- Required characters, props, and coordinate citations.

Treat a named setting as part of the story, not generic scenery. Open each episode with an establishing panel for its first setting. Give every meaningful location change its own panel or a visually unambiguous transition. Use the setting's specific architecture, light, landscape, and social function.

Read `references/week-production-checklist.md` while assembling the episode map and final QA pass.

## Write the Storyboards

Create `art/storyboards/week-XX/week-XX-episode-YY.md` for every daily episode before generating a new weekly batch.

Each storyboard must include:

1. Date, source files, and concise story purpose.
2. Coordinate-cited continuity references, such as `CHAR-MALIK:A2`, `ENV-CORE:C1`, and `PROP-ACADEMIC:B1`.
3. A panel plan in left-to-right, top-to-bottom reading order.
4. One dominant visual and emotional beat per panel.
5. Exact listed dialogue and captions for the lettering pass.
6. A clear initial setting introduction and clear location transitions.
7. Pass-one restrictions: no dialogue, captions, readable equations, incidental signs, or logos.

Use four panels as a default phone-readable page. Use more panels or more than one page when the source material needs room for an understandable setting transition, emotional beat, or dialogue sequence. Never force a whole day into one page simply to preserve a fixed panel count.

## Generate Art Then Lettering

Use the built-in image generation workflow and generate each distinct page separately.

### Pass One: Unlettered Art

1. Supply the relevant character, environment, and prop boards as reference images.
2. Prompt for one finished, phone-readable multi-panel comic page with clean gutters and intentional negative space for later text.
3. Name the panels, locations, shot scale, character actions, emotional subtext, color language, and required visual transitions.
4. Prohibit all text, captions, signs, logos, and watermarks.
5. Inspect the output before accepting it.

Use only fictional McCall-Hart visual language: indigo, copper, cream, cypress gray, warm limestone, dark walnut, honey brick, pale limestone trim, wrought iron, live oaks, magnolias, cypress, and appropriate humid Southern light.

### Pass Two: Lettering

1. Use the accepted unlettered image as the edit target.
2. Preserve all artwork, panel borders, character designs, composition, props, and lighting.
3. Add only the storyboard's exact dialogue and captions.
4. Use clean white balloons with crisp black lettering and restrained cream caption boxes.
5. Keep reading order clear and never cover faces, hands, key props, equations, or decisive visual action.
6. Inspect every lettered image at a readable size.

Correct dialogue attribution or wording in the storyboard before lettering if source review exposes an error. Preserve prose wording unless a dialogue revision is explicitly approved.

## Save Predictably

Use this output layout:

```text
art/storyboards/week-XX/
  README.md
  week-XX-episode-01.md
  ...
art/final/week-XX/
  episode-01/
    week-XX-episode-01-art-v1.png
    week-XX-episode-01-lettered-v1.png
  ...
```

Copy accepted generated images from the image tool's default location into the project. Never overwrite a prior accepted page unless the user explicitly asks for replacement; create a versioned sibling instead.

## Verify the Whole Week

Before presenting the week as complete, verify:

- Every required daily episode has a storyboard.
- Every required daily episode has both an unlettered and lettered final page.
- Every page has a recognizable opening setting.
- Every location change is visible rather than implied by generic backgrounds.
- Character faces, hair, body language, wardrobe logic, and recurring props match the cited asset boards.
- All identity is fictional McCall-Hart and all archive material is excluded.
- Lettering is legible, correctly ordered, source-faithful, and clear of important art.
- The weekly turn and end-of-week handoff remain intact across the full sequence.

Report the saved storyboard and final-page paths, the source files used, and any residual visual limitation honestly.
