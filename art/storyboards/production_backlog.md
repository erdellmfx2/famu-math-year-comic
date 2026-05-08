# Production Backlog

## Current Week 01 Priority
1. **Week 01 Episode 03 — Why math at FAMU?**
   - Panel 1 ✅ saved in logs
   - Panel 2 ✅ saved in logs
   - Panel 3 ✅ saved in `art/final/panels/week-01-episode-03/`
   - Panel 4 ⏳ next active blocker

## Next Target
- Highest-value next panel: `week-01-episode-03` panel 4
- Reason: Episode 03 is the current in-progress Week 01 conversation scene, and panel 4 is now the next missing beat needed to move the week forward.

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
