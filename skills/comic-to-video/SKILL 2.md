---
name: comic-to-video
description: Convert an approved comic episode, day, or week into a narrated vertical video using its timeline outline, prose, title card, unlettered comic art, approved closing message card, OpenAI synthetic voices, and HyperFrames. Use when Codex is asked to make a comic video, animated-comic slideshow, narrated social video, motion-comic episode, or prose-read-along from The Formula of Becoming assets, including draft renders, revisions, and final production exports.
---

# Comic to Video

Produce a source-faithful motion-comic video that begins with the approved title card, narrates the selected prose over scene-matched unlettered art, and ends with one approved message card.

## Confirm Production Is Open

Read `story/approval_status.json` before creating narration or video output. Proceed only when both `script_approved` and `comic_production_allowed` are `true`.

Do not expose, copy, print, or commit API keys. Use `OPENAI_API_KEY` from the environment or the repository's ignored `.env.local`.

Before sending prose to an external voice API, confirm that the user has authorized it in the current task or an earlier task. Do not ask again when authorization is already explicit.

## Load the Required Skills

Read and follow the installed `hyperframes` skill first, then its CLI and creative or animation guidance as needed. Use HyperFrames for composition, timing, motion, validation, and rendering.

Use `media-use` when resolving any media not already supplied by the comic repository. Do not add stock imagery, music, sound effects, or generated filler unless the user requests them.

## Ground the Episode

Read the sources listed in `references/famu-comic-conventions.md`. Use:

- The timeline outline for required events, chronology, and continuity.
- The prose for exact narration, dialogue, scene texture, and emotional pacing.
- The active unlettered comic pages for the story visuals.
- The packaged title and message cards unchanged.

For a requested day or episode, identify its prose section by its dated heading and story event, not only by ordinal position. Preserve every selected prose word unless the user requests an adaptation or abridgment.

Do not narrate Markdown headings, dates, source notes, or production metadata by default. Narrate the prose section body only, unless the heading is intentionally part of the requested performance.

Never use archive assets, obsolete continuity, lettered pages, review images, or real-university imagery as silent substitutes. If required unlettered art is missing, stop and report the exact missing scene or request permission to use another visual treatment.

## Choose the Voice Format

Default to **narrated prose**:

- Use `audio/voice-casting/narrator.md` as the current continuity direction.
- Direct the narrator to distinguish dialogue subtly through rhythm and attitude.
- Do not imitate real people or exaggerate racial, regional, or class markers.

Use **full cast** only when requested:

- Read `audio/voice-casting/README.md` and each speaking character's casting file.
- Assign the narrator to prose and the approved character voice to dialogue.
- Preserve the casting directions across episodes.
- Split clips at speaker changes while retaining natural pauses.

Disclose in publication notes that the voiceover uses AI-generated voices.

Treat casting files marked proposed as audition directions, not final approval. Generate only a short audition when a voice or cast configuration has not yet been accepted. Reuse an already accepted episode setup when the user has approved it and no casting change is requested.

## Build the Narration

1. Copy `assets/narration-manifest.example.json` into the episode output folder.
2. Divide the selected prose into scene-faithful clips, normally 20 to 50 seconds each.
3. Keep each clip under 4,000 characters.
4. Use stable ordered IDs such as `01-arrival` and `02-first-joke`.
5. Set manifest-level voice direction for narrated prose or clip-level voices for full cast.
6. Preserve punctuation because it controls pauses and expression.
7. Generate the clips with:

```bash
node <skill-dir>/scripts/generate_voiceover.mjs \
  --manifest video/week-XX-day-YY/narration-manifest.json \
  --output video/week-XX-day-YY/audio \
  --env .env.local
```

Run first with `--dry-run` to validate the manifest without using the API. Use `--overwrite` only when the user has approved replacing existing audio.

Inspect clip durations after generation. Treat the audio as the timing authority; do not speed up narration merely to fit a predetermined video length.

## Map Narration to Art

Create `scene-plan.md` from `assets/scene-plan-template.md`. Give every audio clip:

- Its exact source prose section.
- Its matching unlettered page and panel or full-page visual.
- The intended crop and focal point.
- A restrained camera move or hold.
- Its measured duration and transition.

Show the visual that matches the event currently being narrated. Do not leave a character, location, or emotional beat on screen after the narration has clearly moved elsewhere.

Prefer full-screen panel crops for vertical scenes. For wide panels, preserve both speakers or the decisive action by centering the complete panel over a softly blurred version of the same art. Never crop away the active speaker, listener reaction, mathematical object, or required setting cue.

Contain title and message cards that do not match the delivery aspect ratio over a series-appropriate indigo matte or a softly blurred copy of the same card. Never crop, stretch, or re-typeset an approved card merely to fill the frame.

## Build the HyperFrames Project

Create the working project at `video/week-XX-day-YY/hyperframes/` and freeze all media under its local `assets/` folder. Do not depend on remote runtime URLs.

Before editing the composition:

1. Complete the current HyperFrames intent or brief step and save `BRIEF.md`.
2. Write `DESIGN.md` with the visual direction, format, pacing, and audio policy.
3. Finish `scene-plan.md` with measured audio durations.
4. Use 1080 by 1920, 30 fps, unless the user requests another delivery format.
5. Hold the title card intact for approximately 4 to 6 seconds.
6. Begin narration after the title card.
7. Sequence story visuals against their audio clips without gaps or overlap.
8. Use restrained push-ins, pans, and crossfades that support reading rather than compete with it.
9. Add no speech balloons, captions, interface chrome, or promotional text unless requested.
10. End narration before the closing card.
11. Hold the approved message card intact for approximately 6 to 8 seconds.

Create a draft render first. Review and correct scene matching, crops, pacing, and audio before producing the high-quality final.

## Save Predictably

Use this layout:

```text
video/week-XX-day-YY/
  BRIEF.md
  DESIGN.md
  scene-plan.md
  narration-manifest.json
  audio/
  hyperframes/
  week-XX-day-YY-draft.mp4
  week-XX-day-YY-final.mp4
```

For a full week, use `video/week-XX/` with one day subfolder per episode. Do not overwrite an approved final; create a versioned sibling unless replacement is explicit.

## Verify Before Delivery

Read and complete `references/qa-checklist.md`.

Do not call the video complete until all of these are true:

- HyperFrames validation passes with no runtime, layout, or motion errors.
- The final MP4 is 1080 by 1920 at 30 fps unless another format was requested.
- The video has H.264 video and audible AAC audio.
- The title card is the first visible section.
- Narration follows the selected prose and begins after the title card.
- Every sampled story frame uses appropriate unlettered art with acceptable crops.
- The final section is one intact approved message card.
- Audio does not clip and remains understandable throughout.
- No secret or `.env` file appears in version-control changes.

Report the final video path, runtime, dimensions, narration mode, validation result, and any residual limitation. Do not claim a GitHub push unless it was requested and confirmed.
