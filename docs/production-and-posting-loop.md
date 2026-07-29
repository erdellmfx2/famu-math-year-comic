# Comic and Video Production Loop

This is the operating loop for producing *The Formula of Becoming* comic and video releases while protecting the weekly OpenAI compute budget.

## Core Constraint

Do not spend more than 50% of the weekly OpenAI compute allocation on one production week.

Because the weekly usage meter is reported as a remaining percentage rather than per-asset token totals, each production week must record:

- Starting weekly allocation remaining.
- Checkpoint allocation remaining after storyboards.
- Checkpoint allocation remaining after comic art.
- Checkpoint allocation remaining after lettering and PDF packaging.
- Checkpoint allocation remaining after video voiceover and captions.
- Final weekly allocation remaining after all accepted exports.

Stop new OpenAI generation when either condition is true:

- The weekly remaining allocation has dropped by 50 percentage points from the start of the production cycle.
- The remaining allocation is at or below the weekly reserve floor set in that week's ledger.

Local deterministic work does not count against the OpenAI generation budget, but it should still be logged.

## Weekly Rhythm

### Friday Setup

Goal: prepare the Saturday workbench without using meaningful compute.

1. Pick the target story week.
2. Read the timeline outline, prose, setting bible, character bible, style guide, and current continuity assets.
3. Create or update the weekly resource ledger from `docs/templates/weekly-resource-ledger-template.md`.
4. Record the current weekly allocation remaining before any generation.
5. Confirm which assets already exist and which days need new art or video.
6. Prepare a Saturday batch list with the minimum necessary generation calls.

Preferred output:

- `art/storyboards/week-XX/README.md`
- `art/storyboards/week-XX/resource-ledger.md`
- A clear day-by-day task list.

### Saturday Creation Block

Goal: create most assets while staying under the 50% weekly allocation cap.

Work in this order:

1. Storyboards first.
2. Unlettered comic pages second.
3. Local lettering, page marks, title cards, and message cards third.
4. Weekly PDF fourth.
5. Voiceover and captioned video only after comic images are accepted.

Use this stoplight:

- Green: less than 30% of the weekly allocation has been spent. Continue normal batch work.
- Yellow: 30% to 40% has been spent. Finish the current day or current pass, then review.
- Orange: 40% to 50% has been spent. Only do essential fixes for already-started assets.
- Red: 50% has been spent. Stop OpenAI generation for the week and switch to local QA, packaging, or scheduling notes.

Recommended Saturday batch shape:

- Morning: storyboard and prompt planning for all seven days.
- Midday: generate or revise comic art, starting with the highest-impact days.
- Afternoon: local lettering/package/PDF work.
- Evening: create videos only for approved comic days and only while still green or yellow.

### Sunday QA and Hermes Handoff

Goal: package approved materials so Hermes can publish them on the set schedule.

1. Review the comic sequence for every day:
   title card, comic page or pages, message card.
2. Review video exports:
   title card first, narration after title, caption safe area, Ken Burns motion, message card last.
3. Confirm no videos are staged for GitHub unless explicitly approved.
4. Refresh `art/current/week-XX/`.
5. Prepare the Hermes handoff manifest.
6. Commit and push non-video source assets and final images/PDF when requested.

Hermes should receive:

- Current social comic image paths by day.
- Current weekly PDF path.
- Current final video paths by day.
- Captions/disclosure note that video voiceovers use AI-generated voices.
- Posting schedule labels.
- Any day that is held back or requires review.

### Monday Through Thursday Publishing Window

Goal: Hermes publishes from the approved package without asking the production agent to create new assets midstream.

Hermes handles:

- Social upload.
- Scheduled release timing.
- Platform-specific captions.
- Posting confirmation.

Production handles only:

- Emergency corrections.
- Replacement exports for approved fixes.
- Ledger updates if a new OpenAI call is required.

## Comic Production Loop

Use `skills/comic-week-generator/SKILL.md` for a full week.

For each target week:

1. Read `story/approval_status.json`.
2. Read the target outline at `story/timeline-weeks/<week>.md`.
3. Read the target prose at `story/timeline-weeks-prose-v2/prose_<week>.md`.
4. Build all daily storyboards before generating art.
5. Preserve longer banter by defaulting to at least two comic pages per day.
6. Generate unlettered pages before lettering.
7. Letter locally or with the lowest viable generation path.
8. Keep speech bubbles and captions out of faces.
9. Add the approved FAMU Mathematics page mark to each comic page.
10. Package each day as title card, comic page or pages, and message card.
11. Export one complete social-media-size weekly PDF.
12. Refresh `art/current/week-XX/`.

OpenAI generation should be used primarily for:

- New unlettered comic art.
- Character, setting, or prop boards that unlock repeated use.
- Targeted visual fixes that cannot be solved locally.

Local deterministic work should be used for:

- Title cards.
- Page marks.
- Lettering when layout can be safely composed.
- Face-clear relettering.
- PDF export.
- Folder cleanup and manifests.

## Video Production Loop

Use `skills/comic-to-video/SKILL.md` for videos.

Production-size rule: make and verify only one video at a time. Complete the requested
day's voiceover, captions, render, QA, and ledger before starting another day, because
multi-video batches create large files and have caused reliability issues.

For each approved day:

1. Use the approved comic package as the visual source.
2. Use the prose as the narration source.
3. Use full-cast voices when the prose contains dialogue.
4. Apply the pronunciation lexicon for recurring names.
5. Generate voiceover scene tracks.
6. Build the HyperFrames video with title card first and message card last.
7. Use the captioned version as the default social version.
8. Keep active-word captions in white with FAMU dark green highlight.
9. Verify Ken Burns motion in the encoded output.
10. Save videos under `video/week-XX-day-YY/`.

OpenAI generation should be used primarily for:

- TTS voiceover.
- Word-level transcription for captions.

Local deterministic work should be used for:

- HyperFrames composition.
- Motion timing.
- Caption layout.
- Rendering.
- QA screenshots.

## Compute Budget Policy

Use the weekly resource ledger as the authority for production decisions.

Recommended reserve plan:

- Begin Saturday with at least 50% remaining if the goal is a full comic and video week.
- Reserve 10% to 15% for fixes after review.
- Reserve 5% to 10% for urgent voiceover or caption corrections.
- Do not spend the reserve on speculative improvements.

If the week starts with less than 50% remaining:

1. Prioritize comic images over video.
2. Prioritize accepted social pages over regenerated art.
3. Create fewer videos and let Hermes post still-image comics for the remaining days.
4. Defer nonessential character boards, setting boards, and alternate versions.

## Handoff Manifest

Create `handoff/hermes/week-XX-posting-manifest.md` before Hermes starts posting.

The manifest should include:

- Week number and arc title.
- Day-by-day comic image sequence.
- Day-by-day video path, if available.
- Weekly PDF path.
- Posting dates and platform notes.
- Required caption/disclosure text.
- Held items or pending approvals.

Hermes owns publication after this manifest is approved.

## Definition of Done

A production week is ready for Hermes when:

- `art/current/week-XX/` points to the current comic image package.
- The weekly PDF exists and opens.
- Every approved video exists locally and has passed QA.
- The resource ledger is updated through final export.
- The Hermes handoff manifest is complete.
- GitHub has the non-video production files, if a push was requested.
- Large videos remain local unless explicit upload storage is chosen.
