# Comic Video QA Checklist

## Composition

- Run the HyperFrames check command required by the installed HyperFrames skill.
- Review every warning; do not ignore a warning that can affect rendering.
- Confirm zero runtime, layout, and motion errors.
- Render a draft before the high-quality final.

## Technical Inspection

Use `ffprobe` or the HyperFrames-bundled probe to confirm:

- Duration matches the title hold, all narration clips, transitions, and closing hold.
- Video is 1080 by 1920 and 30 fps unless the user requested another format.
- Video codec is H.264.
- Audio codec is AAC with a normal sample rate and at least one channel.

Use FFmpeg `volumedetect` to confirm:

- Speech is not silent.
- Peaks do not clip at 0 dB.
- The average speech level is reasonable for spoken-word playback.

Do not normalize blindly. Listen to representative dialogue when playback is available and adjust only after identifying the actual problem.

## Visual Sampling

Extract and inspect frames from:

1. The title-card hold.
2. The first narrated scene.
3. At least one frame from every distinct location.
4. A middle dialogue or emotional beat.
5. The final narrated scene.
6. The closing message-card hold.
7. The last half-second before fade-out.

Confirm:

- Cards remain intact and readable.
- No title or message wording is cropped.
- Story images are unlettered.
- The active speaker, listener reaction, and decisive props remain visible.
- Wide panels preserve both sides of the scene.
- Blurred backgrounds use the same panel rather than unrelated filler.
- Motion never reveals outside the source image.
- Transitions contain no black flash, frozen partial crop, or unintended overlap.

## Audio and Story

- Compare all full-cast manifest utterances against the selected prose with a normalized word-order audit.
- Inspect `generation-report.json`; confirm the expected distinct `speaker/voice` pairs and one item per utterance.
- Confirm `audio/voice-casting/pronunciation-lexicon.json` is valid and every recurring named
  character has one stable pronunciation entry.
- Confirm every generated utterance containing a locked name records the expected
  pronunciation ID in `generation-report.json`.
- Confirm all character and narrator clips exist and are in order.
- Build or inspect a representative audition containing narrator, Malik, Nia, and any other principal speaker.
- Reject any production in which one voice ID performs all dialogue merely through style instructions.
- Confirm narration begins after the title card.
- Confirm each visual changes at the correct story beat.
- Confirm narration ends before the message card.
- Audibly check each recurring character name at least once, and check corrected names in
  both narrator and character voices. Reject inconsistent pronunciation across clips.
- Confirm names, dialogue, equations, and punctuation are pronounced acceptably.
- Confirm the published description can disclose AI-generated voices.

## Ken Burns Motion

- Sample at least two frames from within the same long story scene.
- For portrait social delivery, confirm the scene starts approximately 8 to 10 percent
  enlarged and the later frame is visibly wider than the earlier frame.
- Confirm the movement is continuous and does not reverse from zoom-out to zoom-in.
- Confirm no image edge, empty canvas, or unsafe crop becomes visible.
- Keep title and message-card motion subordinate to readability.
- Repeat the paired-frame check against the encoded final MP4. Source transforms alone do
  not prove the delivered video contains perceptible motion.

## Word-Highlight Captions

- Keep the approved clean video and captioned comparison as separate files.
- Confirm the word transcript was generated from the finished scene audio, not estimated
  from prose length.
- Compare normalized transcript content with the approved prose scene by scene.
- Review `transcription-report.json`; resolve every scene marked `needs_review`.
- Confirm every caption word has a positive duration and monotonic timing.
- Confirm title and message cards have no generated caption overlay.
- Sample the first, middle, and final narration scenes at exact word timestamps.
- Confirm all words are white and only the currently spoken word receives the highlight.
- For a requested FAMU treatment, confirm the active-word backing is dark green `#215732`
  and the word itself remains white for contrast.
- Confirm groups contain no more than six words and fit without clipping or overlap.
- Confirm the caption rail remains above social-platform controls and does not cover faces
  or required mathematical objects.
- Run a HyperFrames check with explicit samples during several caption groups and require
  zero runtime, layout, motion, and contrast errors.
- Verify the captioned MP4 retains the clean video's duration, full-cast audio, dimensions,
  frame rate, opening title, Ken Burns motion, and closing message card.
- If narration timing or Ken Burns motion changed, confirm captions were rendered from the
  primary composition rather than overlaid on an obsolete clean MP4.

## Repository Safety

- Run `git diff --check`.
- Inspect the relevant `git status` paths.
- Confirm `.env`, `.env.local`, API keys, temporary frames, browser caches, and generated dependency folders are not staged.
- Keep the final MP4 local unless the user explicitly requests version control or another upload destination.
