---
name: comic-week-generator
description: Build a complete, consistent weekly comic package from approved McCall-Hart story sources. Use when Codex needs to adapt a timeline week and its prose into daily releases with a title card, one or more lettered comic pages, and a rotating approved message card, especially when longer dialogue, location transitions, character continuity, source-faithful wording, and visual-quality checks must remain consistent across a week.
---

# Comic Week Generator

Create a coherent seven-day comic sequence, not a disconnected batch of images. Plan the week as one story unit; generate and letter each daily release as a deliberate part of that unit.

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

Create `art/storyboards/week-XX/week-XX-episode-YY-page-01.md` and
`week-XX-episode-YY-page-02.md` for every daily episode before generating a
new weekly batch. Create `page-03` only when the prose needs an additional
location transition, emotional turn, or conversation to remain understandable.

Each storyboard must include:

1. Date, source files, and concise story purpose.
2. Coordinate-cited continuity references, such as `CHAR-MALIK:A2`, `ENV-CORE:C1`, and `PROP-ACADEMIC:B1`.
3. A panel plan in left-to-right, top-to-bottom reading order.
4. One dominant visual and emotional beat per panel.
5. Exact listed dialogue and captions for the lettering pass.
6. A clear initial setting introduction and clear location transitions.
7. Pass-one restrictions: no dialogue, captions, readable equations, incidental signs, or logos.

Use four panels as a default phone-readable page. Every daily release normally
uses at least two comic pages: Page 1 for setup and forward action; Page 2 for
the longer banter, explanation, reaction, or emotional turn that would
otherwise be lost in compression. Use Page 3 when the prose needs an
additional location transition, emotional beat, or dialogue sequence. Never
force a whole day into one page simply to preserve a fixed panel count.

## Preserve Longer Banter

For every daily episode, compare the prose scene with Page 1's selected text
before finalizing Page 2. Put the omitted material with the greatest character
value on Page 2, prioritizing:

1. Back-and-forth dialogue that changes how Malik and Nia understand each other.
2. A reply, pause, or joke that changes the emotional meaning of the scene.
3. Explanations that connect a mathematical idea to a person or lived context.
4. Private reactions that the art can show with a concise caption or silent panel.
5. A clear aftermath that hands the day forward to the next episode.

Do not repeat dialogue already used on Page 1. Preserve the prose wording
exactly unless a dialogue revision is explicitly approved.

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

### Apply the Series Mark and Package Each Release

After lettering, add the approved transparent page mark
`art/final/series-endcards/approved/formula-of-becoming-famu-math-page-mark-v1.png`
to the bottom-right of every final comic page. Preserve its scale and circular
shape, keep it clear of dialogue and important art, and do not substitute an
official FAMU mark. The circular text is plain attribution only.

For every daily episode, create `sequence/` within its final episode folder
and package these sections in reading order:

1. `01-title-card-v1.png`: Begin with the approved series logo, the exact
   weekly timeline title as the arc title, then `PART N` for that episode's
   one-indexed day in the week.
2. `02-comic-page-01-v1.png`: The first lettered comic page, carrying setup
   and action.
3. `03-comic-page-02-v1.png`: The second lettered comic page, carrying
   expanded banter, reaction, explanation, or emotional turn.
4. `04-<approved-message>-end-card-v1.png`: One approved message card from
   `art/final/series-endcards/approved/`.

Use `04-comic-page-03-v1.png` and move the message card to `05-` only when a
third comic page is genuinely needed.

Do not invent arc labels or message wording. Preserve the selected approved
closing card unchanged.

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
    sequence/
      01-title-card-v1.png
      02-comic-page-01-v1.png
      03-comic-page-02-v1.png
      04-<approved-message>-end-card-v1.png
      README.md
  ...
```

Copy accepted generated images from the image tool's default location into the project. Never overwrite a prior accepted page unless the user explicitly asks for replacement; create a versioned sibling instead.

## Verify the Whole Week

Before presenting the week as complete, verify:

- Every required daily episode has a storyboard.
- Every required daily episode has Page 1 and Page 2 storyboards, unlettered
  art, and lettered final pages.
- Every page has a recognizable opening setting.
- Every location change is visible rather than implied by generic backgrounds.
- Character faces, hair, body language, wardrobe logic, and recurring props match the cited asset boards.
- All identity is fictional McCall-Hart and all archive material is excluded.
- Lettering is legible, correctly ordered, source-faithful, and clear of important art.
- Page 2 carries distinct prose banter, reaction, or explanation rather than
  repeating Page 1's dialogue.
- The approved FAMU Mathematics Department page mark is visible in the
  bottom-right of every final comic page.
- Every daily release begins with the series-logo title card, exact weekly arc
  title, and correct `PART N` label.
- Every daily release ends with one approved series message card.
- The weekly turn and end-of-week handoff remain intact across the full sequence.

Report the saved storyboard and final-page paths, the source files used, and any residual visual limitation honestly.
