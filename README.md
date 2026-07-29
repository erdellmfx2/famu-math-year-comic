# The Formula of Becoming

A story-development repository for a daily social comic about two first-year mathematics students at McCall-Hart University, a wholly fictional Deep South HBCU.

The GitHub repository slug is a legacy project name. The active story is not set at Florida A&M University and must not use FAMU identity, venues, marks, colors, opponents, or institutional claims.

## Current Status

- The v1 FAMU-based manuscript and visual experiments are preserved under `archive/famu-v1/`, `story/archive/famu-v1/`, `art/archive/famu-v1/`, and `assets/archive/famu-v1/`.
- The v2 fictional setting and season arc are active.
- All 54 weekly approval scripts and 374 daily episode beats have been drafted.
- The v2 script is approved and comic production is open.
- The production and posting loop is documented in `docs/production-and-posting-loop.md`.

## Review First

The primary review document is:

- `story/script-v2-output/the-formula-of-becoming-script-v2.md`

Supporting authorities:

- `story/setting_bible_v2.md`
- `story/character_bible_v2.md`
- `story/season_arc_v2.md`
- `story/season_plan_v2.json`
- `story/master_calendar_2025_2026.md`
- `story/approval_status.json`

## Story Commitments

- Fall: Nia dates Julian while Malik hopes for Nia; Malik's analytics challenge ends in failure.
- Spring: Malik dates Simone while Nia hopes for Malik; Nia's fellowship challenge ends in failure.
- Summer: The students turn rejected research into useful community work, resolve family and emotional arcs, and choose each other.
- Across the year: Calculus I, II, and III topics; football, basketball, softball, baseball, track, and band culture; a family storm crisis; conferences, talks, outreach, presentations, and Delta National Laboratory.

## Build Workflow

1. Edit the authored plan in `story/season_plan_v2.json`.
2. Run `python3 scripts/build_master_calendar.py`.
3. Run `python3 scripts/write_next_week_timeline.py --all`.
4. Run `python3 scripts/combine_timeline_scripts.py`.
5. Run `python3 scripts/validate_story_v2.py`.
6. Review and explicitly approve the script before creating new storyboards or images.

The scripts validate and format authored plot. They do not generate story by rotating generic activity lists.

## Production Workflow

Use `docs/production-and-posting-loop.md` for the weekly comic and video process. The active constraint is to keep each production week under 50% of the OpenAI weekly compute allocation, do most creation on Saturdays, and hand approved posting packages to Hermes for scheduled social publishing.

## Research Boundary

Files under `research/` retain their real source names for provenance. They are structural references only and are not claims about the fictional university.
