# Production Backlog

## Current Week 01 Priority
1. **Week 01 Episode 03 — Why math at FAMU?**
   - Panel 1 ✅ saved in logs
   - Panel 2 ✅ saved in logs
   - Panel 3 ✅ saved in `art/final/panels/week-01-episode-03/`
   - Panel 4 ✅ saved in `art/final/panels/week-01-episode-03/`

## Next Target
- Highest-value next panel: [blocked on next storyboard selection]
- Reason: `week-01-episode-03` is now complete, so the next nightly run should choose the next Week 01 comic blocker after storyboard review.

## Continuity Guidance
- Prefer the most recent same-scene conversation panels as references.
- Default to a maximum of 2 references on first attempt.
- Simplify prompt/reference load before retrying if optimization stability drops.

## 2026-05-08 Nightly Run Note
- Reviewed the budget plan, available storyboard/prompt material, asset manifest, and current final outputs before generating.
- Recreated the missing `art/storyboards/week-01-episode-03.md`, `art/prompts/week-01-episode-03-prompts.md`, and `art/storyboards/production_backlog.md` files so the comic can continue from the expected repo locations.
- Confirmed the highest-value target was `week-01-episode-03` panel 3 because Episode 03 remained the active Week 01 blocker.
- Attempt 1 used 2 references (`week-01-episode-03` panels 2 and 1 from `logs/`) with the normal concise panel prompt and timed out.
- Attempt 2 simplified to 1 reference (`week-01-episode-03` panel 2 from `logs/`) and a shorter prompt.
- Attempt 2 succeeded, and the image was saved as `art/final/panels/week-01-episode-03/2026-05-08_week-01_episode-03_panel-03_nia-shares-her-side.png`.
- Stopped after the single successful save to keep the run conservative and protect continuity.
- Best next continuation: move to `week-01-episode-03` panel 4 with the same minimal-reference discipline.

## 2026-05-08 Nightly Run Note — Panel 4 Blocker
- Highest-value target for this run was `week-01-episode-03` panel 4, the current Week 01 blocker.
- Added concise panel-4 prompts to `art/prompts/week-01-episode-03-prompts.md` before generating.
- Attempt 1 used 2 references (`week-01-episode-03` panel 2 from `logs/` and panel 3 from `art/final/`) with the normal concise panel prompt and timed out.
- Attempt 2 used 1 reference (`week-01-episode-03` panel 1 from `logs/`) with the simplified prompt and timed out.
- Attempt 3 kept 1 reference (`week-01-episode-03` panel 1 from `logs/`) and used the ultra-simple prompt; it also timed out.
- No final image was saved for panel 4 in this run.
- Stopped after the 3-attempt ladder to avoid continuity drift and unproductive retries.
- Best next continuation: retry panel 4 in a later run starting from the ultra-simple 1-reference setup, unless provider stability improves enough to restore the 2-reference version.

## 2026-05-09 Nightly Run Note — Panel 4 Success
- Highest-value target for this run was still `week-01-episode-03` panel 4, the current Week 01 blocker.
- Reused the existing concise panel-4 prompt pack and kept the reference package minimal.
- Attempt 1 used 1 reference (`logs/week-01-episode-03/2026-05-03_week-01_episode-03_panel-01_why-math-question.png`) with the normal concise prompt and timed out.
- Attempt 2 kept the same 1 reference and used the simplified prompt.
- Attempt 2 succeeded, and the image was saved as `art/final/panels/week-01-episode-03/2026-05-09_week-01_episode-03_panel-04_famu-made-the-connection.png`.
- Prompt simplification was applied once after the timeout, and no extra references were added.
- Stopped after the single successful save to protect continuity and keep the run conservative.
