---
name: comic-to-video
description: Convert an approved comic episode, day, or week into a full-cast narrated vertical video using its timeline outline, prose, title card, unlettered comic art, approved closing message card, distinct OpenAI synthetic character voices, and HyperFrames. Use when Codex is asked to make or fix a comic video, animated-comic slideshow, narrated social video, motion-comic episode, captioned social comparison, active-word karaoke caption version, or prose-read-along from The Formula of Becoming assets, including voice casting, Ken Burns motion, word-level captions, draft renders, revisions, and final production exports.
---

# Comic to Video

Produce a source-faithful motion-comic video that begins with the approved title card, performs the selected prose with distinct character voices over scene-matched unlettered art, and ends with one approved message card.

## Confirm Production Is Open

Read `story/approval_status.json` before creating narration or video output. Proceed only when both `script_approved` and `comic_production_allowed` are `true`.

Do not expose, copy, print, or commit API keys. Use `OPENAI_API_KEY` from the environment or the repository's ignored `.env.local`.

Before sending prose to an external voice API, confirm that the user has authorized it in the current or an earlier task. Do not ask again when authorization is already explicit.

## Load the Required Skills

Read and follow the installed `hyperframes` skill first, then its CLI and creative or animation guidance as needed. Use HyperFrames for composition, timing, motion, validation, and rendering.

Use `media-use` when resolving media not already supplied by the comic repository. Do not add stock imagery, music, sound effects, or generated filler unless requested.

## Ground the Episode

Read the sources listed in `references/famu-comic-conventions.md`. Use:

- The timeline outline for required events, chronology, and continuity.
- The prose for exact narration, dialogue, scene texture, and emotional pacing.
- The active unlettered comic pages for the story visuals.
- The packaged title and message cards unchanged.

Identify a requested day or episode by its dated heading and story event, not only by ordinal position. Preserve every selected prose word unless the user requests an adaptation or abridgment.

Create and verify only one video at a time. Finish the selected day's voiceover,
captions, render, QA frames, resource ledger, and final path report before starting
another day, because multi-video batches create large media files and have caused
reliability issues.

Do not narrate Markdown headings, dates, source notes, or production metadata by default. Narrate the prose section body only.

Never use archive assets, obsolete continuity, lettered pages, review images, or real-university imagery as silent substitutes. If required unlettered art is missing, report the exact missing scene or request permission for another visual treatment.

## Require True Speaker Separation

Default to **full cast whenever the selected prose contains dialogue**:

- Read `audio/voice-casting/README.md` and every speaking character's casting file.
- Load `audio/voice-casting/pronunciation-lexicon.json` and apply every matching name
  instruction to each generated utterance.
- Assign prose and dialogue tags to the narrator.
- Assign every quoted or interior line to its actual character.
- Generate each speaker turn with that speaker's own voice ID and API call.
- Preserve the casting directions across episodes.
- Split clips at speaker changes while retaining natural pauses.
- Never ask one narrator voice to imitate Malik, Nia, or another character. Performance instructions do not create distinct voices.

Use **single-voice narrated prose** only when the source contains no dialogue or the user explicitly requests one narrator. Do not silently downgrade full-cast dialogue to one-voice narration.

Treat casting files marked proposed as audition directions, not final approval. Generate only a short audition when a voice configuration has not been accepted. Reuse an accepted setup when no casting change is requested.

Disclose in publication notes that the voiceover uses AI-generated voices.

## Build Full-Cast Narration

1. Copy `assets/full-cast-manifest.example.json` into the episode output folder.
2. Create a speaker entry with a distinct voice ID and casting direction for every speaking role.
3. Divide the prose into scene-faithful groups and split every group at each speaker change.
4. Keep narration, quoted dialogue, interior speech, and dialogue tags in exact source order.
5. Keep each utterance under 4,000 characters.
6. Use stable scene IDs such as `01-arrival` and `02-first-joke`.
7. Preserve punctuation because it controls pauses and expression.
8. Run a normalized word-order comparison between the source passage and all manifest utterances.
9. Validate the pronunciation lexicon, including unique character IDs and at least one
   spoken-name match for every recurring named character.
10. Run the generator with `--dry-run` and inspect every `speaker/voice` pair and listed
    pronunciation lock.
11. Generate the speaker turns:

```bash
node <skill-dir>/scripts/generate_full_cast_voiceover.mjs \
  --manifest video/week-XX-day-YY/full-cast-manifest.json \
  --output video/week-XX-day-YY/audio-full-cast/utterances \
  --pronunciations audio/voice-casting/pronunciation-lexicon.json \
  --env .env.local
```

Use `--overwrite` only when replacement is approved.

Keep the written and captioned spelling unchanged. The lexicon changes only the speech
instructions sent to the voice model. When a pronunciation correction affects one name,
regenerate only utterances containing that name before rebuilding scene tracks:

```bash
node <skill-dir>/scripts/generate_full_cast_voiceover.mjs \
  --manifest video/week-XX-day-YY/full-cast-manifest.json \
  --output video/week-XX-day-YY/audio-full-cast/utterances \
  --pronunciations audio/voice-casting/pronunciation-lexicon.json \
  --match-text "Malik" \
  --env .env.local \
  --overwrite
```

Assemble scene-level tracks:

```bash
node <skill-dir>/scripts/assemble_full_cast_scenes.mjs \
  --manifest video/week-XX-day-YY/full-cast-manifest.json \
  --input video/week-XX-day-YY/audio-full-cast/utterances \
  --output video/week-XX-day-YY/audio-full-cast/scenes \
  --ffmpeg <ffmpeg-path>
```

The assembler normalizes turns, inserts controlled pauses, and creates one track per visual scene. Inspect `generation-report.json` and require:

- One generated item for every manifest utterance.
- A distinct expected voice ID for narrator, Malik, Nia, and every other speaking role.
- At least one generated character clip for every character who speaks.
- Every utterance containing a locked name lists the expected pronunciation ID.

For explicitly requested one-voice narration, use `assets/narration-manifest.example.json` with `scripts/generate_voiceover.mjs`.

Measure scene durations after assembly. Treat audio as the timing authority; do not speed up narration merely to fit a predetermined length.

## Map Narration to Art

Create `scene-plan.md` from `assets/scene-plan-template.md`. Give every scene track:

- Its exact source prose section.
- Its matching unlettered page and panel or full-page visual.
- The intended crop and focal point.
- A clearly perceptible Ken Burns zoom-out and optional directional drift.
- Its measured duration and transition.

Show the visual matching the event currently being performed. Do not leave a character, location, or emotional beat on screen after narration moves elsewhere.

Prefer full-screen panel crops for vertical scenes. For wide panels, preserve both speakers or the decisive action by centering the complete panel over a softly blurred copy of the same art. Never crop away an active speaker, listener reaction, mathematical object, or required setting cue.

Default story-panel motion to a continuous Ken Burns zoom-out: for portrait social
delivery, begin approximately 8 to 10 percent enlarged, then slowly settle toward the full
safe crop over the narration. Add at most a slight lateral or vertical drift. Do not
combine an entrance zoom with a second movement that reverses direction. Verify paired
frames from early and late in the same scene are visibly different both in composition
snapshots and in the encoded final MP4. A transform that exists in source code but is not
perceptible after encoding does not pass review.

Contain title and message cards that do not match the delivery aspect ratio over an indigo matte or softly blurred copy of that card. Never crop, stretch, or re-typeset an approved card to fill the frame.

## Build a Word-Highlight Caption Version

When the user requests social captions, karaoke captions, readable spoken words, or a
captioned comparison, preserve the approved clean video and create a separate captioned
version. Never overwrite the clean final.

Use word-level timing from the finished narration rather than estimating timing from
character counts:

1. Copy `assets/caption-timing-manifest.example.json` into the episode folder.
2. Record the exact master-timeline start time for every scene track.
3. Transcribe each scene track separately with the approved prose as the transcription
   prompt:

```bash
node <skill-dir>/scripts/transcribe_scene_tracks.mjs \
  --timing video/week-XX-day-YY/caption-timing-manifest.json \
  --source-manifest video/week-XX-day-YY/full-cast-manifest.json \
  --input video/week-XX-day-YY/audio-full-cast/scenes \
  --output video/week-XX-day-YY/captions \
  --env .env.local
```

The transcription script combines scene-relative word timestamps into the master timeline,
repairs zero-duration API word spans from neighboring boundaries, and writes
`transcript.json` plus `transcription-report.json`.

Require all of the following before authoring captions:

- Every source scene has a corresponding transcription.
- Normalized transcription content matches the approved prose in the same order.
- `review_required` is false or every flagged scene is manually reconciled.
- Every word has a positive duration and monotonically ordered start time.
- Captions begin only after the title card and end before the message card.

Create short caption groups:

```bash
node <skill-dir>/scripts/build_caption_data.mjs \
  --input video/week-XX-day-YY/captions/transcript.json \
  --output video/week-XX-day-YY/captioned/hyperframes/assets/captions-data.js \
  --max-words 5 \
  --pause-break 0.32
```

For portrait social video:

- Place the caption rail near the bottom but above platform controls, approximately 220 to
  260 pixels from the bottom of a 1080 by 1920 frame.
- Keep groups to three to five words when practical and never more than six.
- Render all words in white over a restrained translucent dark rail.
- Highlight only the word currently being spoken.
- When the user requests the darker FAMU university color, use FAMU dark green
  (`#215732`) as the active-word pill or backing color while retaining white word text.
- Use a small scale lift only; avoid bounce, pulsing, or decorative motion that competes
  with the comic.
- Keep title and message cards caption-free.
- Preserve faces, mathematical objects, dialogue reactions, and social-media safe areas.

When narration timing, crops, or Ken Burns motion changes, author the caption layer inside
the primary HyperFrames composition and rerender once. This keeps captions, audio, scene
timing, and motion on the same master timeline. Use a lightweight overlay project only
when the underlying clean MP4 is already approved and no audio, crop, timing, or motion
change is required.

## Build the HyperFrames Project

Create the working project at `video/week-XX-day-YY/hyperframes/` and freeze all media under its local `assets/` folder. Do not depend on remote runtime URLs.

Before editing:

1. Complete the current HyperFrames brief step and save `BRIEF.md` for a fresh project.
2. Write `DESIGN.md` with visual direction, format, pacing, and audio policy.
3. Finish `scene-plan.md` with measured audio durations.
4. Use 1080 by 1920, 30 fps, unless another format is requested.
5. Hold the title card intact for approximately 4 to 6 seconds.
6. Begin narration after the title card.
7. Sequence visuals against scene audio without gaps or overlap.
8. Use clearly perceptible 8 to 10 percent Ken Burns zoom-outs, safe-area drifts, and crossfades for portrait social delivery.
9. Add no speech balloons, captions, interface chrome, or promotional text unless requested.
10. End narration before the closing card.
11. Hold the approved message card intact for approximately 6 to 8 seconds.

Create a draft render first. Review and correct voice separation, scene matching, crops, pacing, and motion before producing the high-quality final.

## Save Predictably

```text
video/week-XX-day-YY/
  BRIEF.md
  DESIGN.md
  scene-plan.md
  full-cast-manifest.json
  audio-full-cast/
    utterances/
    scenes/
  captions/
    raw/
    transcript.json
    transcription-report.json
  captioned/
    hyperframes/
  hyperframes/
  week-XX-day-YY-draft.mp4
  week-XX-day-YY-final.mp4
  week-XX-day-YY-captioned-draft.mp4
  week-XX-day-YY-captioned-final.mp4
```

For a full week, use `video/week-XX/` with one day subfolder per episode. Do not overwrite an approved final; create a versioned sibling unless replacement is explicit.

## Verify Before Delivery

Read and complete `references/qa-checklist.md`.

Do not call the video complete until:

- HyperFrames validation passes with no runtime, layout, or motion errors.
- The final MP4 has the requested dimensions, H.264 video, and audible AAC audio.
- The title card is the first visible section.
- Full-cast narration follows the selected prose and begins after the title card.
- The generation report proves distinct voice IDs and separate files for every speaking role.
- The generation report proves each spoken recurring name received its locked pronunciation instruction.
- A representative audition or encoded scene audibly alternates narrator and character voices.
- Every sampled story frame uses appropriate unlettered art with acceptable crops.
- Paired frames from both the composition and encoded final prove the Ken Burns zoom-out is clearly present.
- Requested captions match the prose, remain in the portrait safe area, and highlight the
  word being spoken.
- Captioned comparison exports preserve the clean version, full-cast audio, title card, and
  closing message card.
- The final section is one intact approved message card.
- Audio does not clip and remains understandable.
- No secret or `.env` file appears in version-control changes.

Report the final video path, runtime, dimensions, speaker/voice pairs, validation result, and residual limitations. Do not claim a GitHub push unless requested and confirmed.
