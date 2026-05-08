# Drawing Production Backlog

## Immediate Next Episodes
1. **Week 01 Episode 01 — Before the First Bell** ✅ storyboard + prompts prepared
2. **Week 01 Episode 02 — Nia’s system vs Malik’s system**
3. **Week 01 Episode 03 — Why math at FAMU?**
4. **Week 01 Episode 04 — Campus organizations fair**
5. **Week 01 Episode 05 — Research starts to feel possible**

## Recommended Production Order
### Phase 1 — Lock visual identity
- Create final reference portraits for Malik
- Create final reference portraits for Nia
- Create one reusable FAMU campus establishing background

### Phase 2 — Build first publishable week
- Rough all 5 weekday episodes
- Review dialogue spacing and phone readability
- Finalize line art / color / caption space

### Phase 3 — Expand cadence
- Convert each completed weekly prose file into panel-ready episodes
- Batch-produce 5-7 episodes at a time
- Save exported assets in `art/final/`

## Current Bottleneck Solved
The repo now has a first-pass drawing layer. Next step is to either:
1. generate character reference art, or
2. generate/draw Episode 01 panels.

## 2026-04-29 Nightly Production Note
- Added reusable three-quarter reference portraits for Malik and Nia in `art/final/characters/`
- Added `week-01-episode-02` panel 3 in `art/final/panels/week-01-episode-02/`
- Created storyboard and prompt pack for Episode 02
- Stopped after panel 4 generation failed with provider limit/error behavior; next safest continuation is to resume with Episode 02 panel 4 before expanding Week 01 further

## 2026-04-29 20:25 UTC Nightly Run Note
- Reviewed the image budget plan, current storyboards, asset library, and generated outputs before attempting new work.
- Confirmed the highest-value next target is `week-01-episode-02` panel 4, per the existing backlog and prompt pack.
- Attempted a single conservative generation for Episode 02 panel 4 and stopped after strong provider warnings.
- Google returned `RESOURCE_EXHAUSTED` because the project exceeded its monthly AI Studio spending cap.
- OpenAI fallback aborted during the same attempt, so no new panel was saved this run.
- Safest next continuation remained: generate the Episode 02 panel 4 file once provider capacity/billing was restored, then continue Week 01 comic production.

## 2026-04-30 04:00 UTC Nightly Run Note
- Reviewed the budget plan, storyboards, asset library, and final art before generating anything.
- Prioritized comic completion over new asset expansion because Episode 02 only needed panel 4 to finish.
- Generated and saved `art/final/panels/week-01-episode-02/2026-04-30_week-01_episode-02_panel-04_on-brand.png` using `openai/gpt-image-2`.
- Stopped after the single successful panel to keep the run conservative and leave Week 01 Episode 02 in a clean completed state.
- Best next continuation: storyboard and prompt Week 01 Episode 03, then resume Week 01 comic production.

## 2026-04-30 07:30 UTC Nightly Run Note
- Reviewed the budget plan, current storyboards, asset library, and generated panel state before attempting any new image work.
- Created `art/storyboards/week-01-episode-03.md` to keep Week 01 comic production moving forward in a clean, prompt-ready way.
- Made one conservative `openai/gpt-image-2` attempt for Episode 03 panel 1 using existing character/panel references.
- The provider returned `Failed to optimize image`, so no new panel file was saved.
- Stopped immediately after the first failed attempt to avoid spammy retries, continuity drift, or abuse-like behavior.
- Safest next continuation: retry Episode 03 panel 1 later with a simplified single-panel prompt/reference set, then continue Week 01 comic production.

## 2026-05-01 04:00 UTC Nightly Run Note
- Reviewed `art/IMAGE_GENERATION_BUDGET_PLAN.md`, the storyboards, asset manifest, and existing final art before generating anything.
- Confirmed the highest-value next target remained `week-01-episode-03` panel 1 so Week 01 comic production could continue from the current conversation scene.
- Made three calm, sequential `openai/gpt-image-2` attempts for Episode 03 panel 1, simplifying the prompt/reference load between attempts.
- All three attempts returned `Failed to optimize image`, so no new panel file was saved and no further image work was attempted this run.
- Stopped after the third attempt for that panel to avoid spammy retries, continuity drift, or abuse-like behavior.
- Safest next continuation: retry Episode 03 panel 1 in a later run with an even simpler continuity-preserving prompt or after provider conditions improve, then resume the rest of Episode 03.

## 2026-05-01 07:30 UTC Nightly Run Note
- Re-reviewed `art/IMAGE_GENERATION_BUDGET_PLAN.md`, all Week 01 storyboards, the asset manifest, and the generated library before attempting new work.
- Confirmed the highest-value comic target was still `week-01-episode-03` panel 1 because Episode 03 remains the active Week 01 blocker.
- Made three calm, sequential `openai/gpt-image-2` attempts for that same panel during this run: one continuity-heavy attempt with two prior panel references, one simplified single-reference attempt, and one ultra-simple fallback attempt.
- The first two attempts returned `Failed to optimize image`; the third attempt aborted before producing an image, so no new panel file was saved.
- Stopped immediately after the third total attempt for this run to stay within the retry cap for that image and avoid spammy or abuse-like generation behavior.
- Verified that previously generated but uncommitted reusable assets were present in `art/final/expressions/`, `art/final/props/`, and `art/final/wardrobe/`, leaving the repo in a cleaner continuation state for the next run.
- Safest next continuation: either retry Episode 03 panel 1 in a future run after provider conditions improve, or pivot briefly to assembling/reusing the newly tracked expression/prop/wardrobe assets if the optimization failures persist.

## 2026-05-02 04:00 UTC Nightly Run Note
- Reviewed `art/IMAGE_GENERATION_BUDGET_PLAN.md`, the current Week 01 storyboards/prompt packs, the asset manifest, and existing final art before generating anything.
- Kept the highest-value target on `week-01-episode-03` panel 1 because Episode 03 is still the active Week 01 blocker and already had a panel-specific prompt pack.
- Made three calm, sequential `openai/gpt-image-2` attempts for that panel in this run: first with 2 same-scene references and the normal concise panel prompt, then with 1 reference and a shortened prompt, then with 1 reference and an ultra-simple fallback prompt.
- All three attempts aborted before an image was produced, so no new panel file was saved in `art/final/panels/week-01-episode-03/`.
- Stopped after the third attempt for this run to avoid wild experimentation, continuity drift, or spammy retry behavior.
- Safest next continuation: pause further Episode 03 panel 1 generation until provider stability improves, then retry with the same minimal single-reference strategy before expanding to later panels.

## 2026-05-02 07:30 UTC Nightly Run Note
- Re-reviewed `art/IMAGE_GENERATION_BUDGET_PLAN.md`, `art/storyboards/production_backlog.md`, the Week 01 Episode 02-03 storyboard/prompt files, `art/assets/asset_manifest.md`, and the current `art/final/` outputs before generating anything.
- Confirmed the single highest-value target was still `week-01-episode-03` panel 1 because Episode 03 remains the active Week 01 blocker for moving the current week forward.
- Attempt 1 used 2 references (`week-01-episode-02` panels 4 and 3) with the normal concise panel prompt focused on the continuing two-shot conversation.
- Attempt 2 simplified to 1 reference (`week-01-episode-02` panel 4) and a shorter prompt.
- Attempt 3 kept 1 reference and used an ultra-simple fallback prompt with only the essential table conversation continuity.
- All three `openai/gpt-image-2` attempts returned an aborted operation before any image file was produced, so no panel was saved into `art/final/panels/week-01-episode-03/`.
- Stopped after the third attempt for this run to stay within the retry ladder and avoid continuity drift or spammy retry behavior.
- Safest next continuation: keep Episode 03 panel 1 paused until provider stability improves, then retry from the minimal single-reference prompt strategy rather than adding more references or prompt complexity.

## 2026-05-03 04:00 UTC Nightly Run Note
- Reviewed `art/IMAGE_GENERATION_BUDGET_PLAN.md`, `art/storyboards/production_backlog.md`, all current Week 01 storyboard/prompt files, `art/assets/asset_manifest.md`, and the existing `art/final/` panel library before generating anything.
- Kept the highest-value target on `week-01-episode-03` panel 1 because Episode 03 is still the active Week 01 blocker for moving the first week forward.
- Attempt 1 used 2 references (`week-01-episode-02` panels 4 and 3) with the normal concise panel prompt for the seated two-shot continuation.
- Attempt 2 simplified to 1 reference (`week-01-episode-02` panel 4) and a shorter prompt.
- Attempt 3 kept 1 reference and used an ultra-simple fallback prompt with only the essential table conversation continuity.
- All three `openai/gpt-image-2` attempts returned an aborted operation before any image file was produced, so no panel was saved into `art/final/panels/week-01-episode-03/`.
- Stopped after the third attempt for this run to avoid wild experimentation, continuity drift, or rapid-fire retries.
- Safest next continuation: leave Episode 03 panel 1 paused until provider stability improves, then retry from the minimal single-reference strategy instead of adding complexity.

## 2026-05-03 07:30 UTC Nightly Run Note
- Re-reviewed `art/IMAGE_GENERATION_BUDGET_PLAN.md`, `art/storyboards/production_backlog.md`, the active Week 01 storyboard/prompt files, `art/assets/asset_manifest.md`, and current `art/final/` outputs before generating anything.
- Confirmed the single highest-value target remained `week-01-episode-03` panel 1 because Episode 03 is still the active blocker for moving Week 01 forward.
- Attempt 1 used 2 references (`week-01-episode-02` panels 4 and 3) with the existing concise panel prompt focused on the seated conversation continuity.
- The first `openai/gpt-image-2` attempt succeeded, and the image was saved as `art/final/panels/week-01-episode-03/2026-05-03_week-01_episode-03_panel-01_why-math-question.png`.
- Stopped after the single success to keep the run conservative and protect continuity.
- Best next continuation: move to Episode 03 panel 2 with the same minimal-reference discipline.

## 2026-05-05 18:01 UTC Nightly Run Note
- Re-reviewed `art/IMAGE_GENERATION_BUDGET_PLAN.md`, `art/storyboards/production_backlog.md`, the active Week 01 storyboard/prompt files, `art/assets/asset_manifest.md`, and current `art/final/` outputs before generating anything.
- Confirmed the single highest-value target was `week-01-episode-03` panel 2 because Episode 03 is the next active blocker for moving Week 01 forward.
- Attempt 1 used 2 references (`week-01-episode-03` panel 1 and `week-01-episode-02` panel 4) with the normal concise panel prompt focused on Malik's reflective answer.
- Attempt 2 simplified to 1 reference (`week-01-episode-03` panel 1) and a shorter prompt after the first attempt aborted.
- Attempt 3 kept 1 reference and used an ultra-simple fallback prompt with only Malik, the table, laptop continuity, and balloon space.
- All three `openai/gpt-image-2` attempts returned an aborted operation before any image file was produced, so no panel was saved into `art/final/panels/week-01-episode-03/`.
- Stopped after the third attempt for this run to stay within the retry cap and avoid continuity drift or wild experimentation.
- Safest next continuation: leave Episode 03 panel 2 paused until provider stability improves, then retry from the minimal single-reference strategy rather than adding prompt or reference complexity.

## 2026-05-05 18:09 UTC Nightly Run Note
- Re-reviewed `art/IMAGE_GENERATION_BUDGET_PLAN.md`, `art/storyboards/production_backlog.md`, the active Week 01 storyboard/prompt files, `art/assets/asset_manifest.md`, and current `art/final/` outputs before generating anything.
- Confirmed the single highest-value target remained `week-01-episode-03` panel 2 because Episode 03 is still the next blocker for moving Week 01 forward.
- Attempt 1 used 2 references (`week-01-episode-03` panel 1 and `week-01-episode-02` panel 4) with the normal concise panel prompt for Malik's reflective answer.
- Attempt 2 simplified to 1 reference (`week-01-episode-03` panel 1) and a shorter prompt after the first attempt aborted.
- Attempt 3 kept 1 reference and used an ultra-simple fallback prompt with only Malik, the campus table, laptop, notebook, calculator, and balloon space.
- All three `openai/gpt-image-2` attempts returned `This operation was aborted` before any image file was produced, so no panel was saved into `art/final/panels/week-01-episode-03/`.
- Stopped after the third attempt for this run to stay within the retry ladder and avoid continuity drift, optimization churn, or wild experimentation.
- Safest next continuation: keep Episode 03 panel 2 paused until provider stability improves, then retry from the minimal single-reference prompt strategy instead of adding more references or detail.

## 2026-05-06 04:00 UTC Nightly Run Note
- Re-reviewed `art/IMAGE_GENERATION_BUDGET_PLAN.md`, `art/storyboards/production_backlog.md`, the active Week 01 storyboard/prompt files, `art/assets/asset_manifest.md`, and current `art/final/` outputs before generating anything.
- Confirmed the single highest-value target remained `week-01-episode-03` panel 2 because Episode 03 is still the next blocker for moving Week 01 forward.
- Added simplified and ultra-simple fallback wording to `art/prompts/week-01-episode-03-prompts.md` so the panel could be retried cleanly without expanding the reference set.
- Attempt 1 used 2 references (`week-01-episode-03` panel 1 and `week-01-episode-02` panel 4) with the normal concise panel prompt and returned `This operation was aborted`.
- Attempt 2 simplified to 1 reference (`week-01-episode-03` panel 1) and the shortened prompt and also returned `This operation was aborted`.
- Attempt 3 kept 1 reference and used the ultra-simple fallback prompt focused only on Malik, the campus table, the open laptop, warm afternoon continuity, and balloon space.
- Attempt 3 succeeded, and the image was saved as `art/final/panels/week-01-episode-03/2026-05-06_week-01_episode-03_panel-02_malik-reflective-answer.png`.
- Stopped after the single successful save to keep the run conservative and protect continuity.
- Best next continuation: move to `week-01-episode-03` panel 3 with the same minimal-reference discipline.

## 2026-05-08 04:00 UTC Nightly Run Note
- Reviewed `art/IMAGE_GENERATION_BUDGET_PLAN.md`, the available storyboard/prompt material, `art/assets/asset_manifest.md`, and current generated outputs before attempting new image work.
- Recreated the missing `art/storyboards/week-01-episode-03.md`, `art/prompts/week-01-episode-03-prompts.md`, and `art/storyboards/production_backlog.md` files so the comic can continue from the expected repo locations.
- Confirmed the single highest-value target was `week-01-episode-03` panel 3 because Episode 03 remained the active Week 01 blocker.
- Attempt 1 used 2 references (`week-01-episode-03` panels 2 and 1 from `logs/`) with the normal concise panel prompt and timed out.
- Attempt 2 simplified to 1 reference (`week-01-episode-03` panel 2 from `logs/`) and the shorter prompt.
- Attempt 2 succeeded, and the image was saved as `art/final/panels/week-01-episode-03/2026-05-08_week-01_episode-03_panel-03_nia-shares-her-side.png`.
- Stopped after the single successful save to keep the run conservative and protect continuity.
- Best next continuation: move to `week-01-episode-03` panel 4 with the same minimal-reference discipline.
