# Art Production

This folder will hold the v2 visual workflow for *The Formula of Becoming*, set at fictional McCall-Hart University.

## Current Status

- The 54-week v2 story script is drafted and awaiting approval.
- New storyboards, prompt packs, panels, pages, and visual assets are blocked.
- Existing legacy storyboards and generated art are preserved under `art/archive/` and must not be reused as v2 continuity.
- The active `art/final/` path contains no approved v2 visual assets yet.

## Approval Gate

Read `story/approval_status.json` before any art task.

Do not create visual production material unless both values are true:

- `script_approved`
- `comic_production_allowed`

Changing a README or preparing a prompt is not a way around the gate. Approval must be recorded explicitly in the status file after the user approves the script.

## Active Sources

- `story/setting_bible_v2.md`
- `story/character_bible_v2.md`
- `story/script-v2-output/the-formula-of-becoming-script-v2.md`
- `art/style_guide.md`
- `art/assets/asset_manifest.md`
- `skills/comic-episode-image-production/SKILL.md`

## Post-Approval Workflow

1. Select an approved weekly script.
2. Draft episode storyboards under `art/storyboards/week-XX/`.
3. Review continuity, dialogue, and phone readability.
4. Build prompt packs under `art/prompts/week-XX/`.
5. Produce one four-panel page without text.
6. Add lettering in a second pass.
7. Save approved v2 output under `art/final/`.

## Organization Rule

Keep storyboard, prompt, and final files grouped by week and episode. Do not place episode files loose at the root of those folders.
