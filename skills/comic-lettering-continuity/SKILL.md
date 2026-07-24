---
name: comic-lettering-continuity
description: Lock The Formula of Becoming comic title cards, weekly part numbering, dialogue lettering, speech-balloon tails, narration boxes, page marks, and recurring-character silhouettes to the approved Week 1 visual system. Use when lettering, correcting, packaging, reviewing, or rebuilding comic pages or weekly social-media releases.
---

# Comic Lettering Continuity

Treat the approved Week 1 `sequence-v2` images as the visual authority. Do not
silently restyle lettering or branding between weeks.

## Read the Locks

Before rendering, read:

1. `references/week-01-visual-lock.md`
2. `art/style_guide.md`
3. `story/character_bible_v2.md`
4. `art/final/foundational-assets/coordinate-registry.md`
5. The target storyboard and accepted unlettered art

Use only active files outside `archive/`.

## Preserve the Title Card

Use
`art/final/series-endcards/approved/formula-of-becoming-series-logo-v1.png`
as the title-card base. Preserve its growing leaf, graph, copper frame, navy
texture, series title, and subtitle. Never redraw or replace the growing leaf
with a generic curve.

Add only the exact weekly arc title and the local part number in the lower safe
area. Restart parts at `PART 1` every week. Compute:

`part = episode_number - first_episode_number_in_week + 1`

Verify that a seven-day week contains `PART 1` through `PART 7`.

## Lock the Lettering

- Dialogue font: `Comic Sans MS Regular`, never Arial, Georgia, or a bold UI
  sans-serif.
- Dialogue color: near-black `#171717`.
- Dialogue balloons: organic white ovals with a thin near-black outline.
- Every spoken balloon must have a visible triangular or curved tail that
  points toward the correct speaker's mouth.
- Use a separate balloon for each speaker turn. Do not combine two speakers in
  one rounded rectangle.
- Text messages may use a rounded device-message box only when the storyboard
  explicitly labels the line as text.
- Narration font: the same `Comic Sans MS Regular`.
- Narration boxes: pale cream/yellow `#FFF4D6` with a thin near-black outline
  and subtly square corners. Narration boxes never have tails.
- Preserve storyboard wording, punctuation, speaker attribution, and reading
  order exactly.
- Never place a balloon, narration box, or text-message box over a face. Face
  clearance is a release-blocking requirement, not a preference.
- Reserve a dedicated lettering band above each panel whenever the accepted
  art does not contain verified empty space. Proportionally fit the artwork
  beneath the band; do not crop, stretch, or cover faces to preserve the old
  layout.
- Only a narrow speech tail may enter the art area, ending near the correct
  speaker's mouth. Keep the balloon body entirely inside the lettering band.
- Keep all text clear of faces, hands, equations, and decisive props.

Do not place visible speaker labels such as `Malik:` or `Caption:` inside the
comic. The tail and panel context identify dialogue; the box style identifies
narration.

## Lock Character Separation

Check silhouettes before lettering:

- Malik: slim-to-average build, dark brown skin, rectangular glasses, short
  tight curls with a low taper, measured posture.
- Julian: visibly taller than Malik, broader and more muscular through the
  shoulders and arms, slightly lighter brown skin, no glasses, high twist fade,
  relaxed media-performer posture.
- DJ: visibly shorter than Malik, compact athletic build, dark brown skin, no
  glasses, short cropped locs with a temple fade, energetic posture.

Reject a page when Malik, Julian, or DJ could be mistaken for one another at
thumbnail size. Correct the unlettered art before adding text.

## Add the Page Mark

Place
`art/final/series-endcards/approved/formula-of-becoming-famu-math-page-mark-v1.png`
once at the bottom-right of every comic page. Preserve its circular shape and
keep it small and clear of text and important art. Do not add it again during
PDF export.

## Package and Verify

Package each daily release in `sequence-v2`:

1. `01-title-card-vN.png`
2. `02-comic-page-01-vN.png`
3. `03-comic-page-02-vN.png`
4. `04-<approved-message>-end-card-vN.png`

Before acceptance, visually inspect the title card, every comic page, and the
closing card. Check:

- growing leaf present and unobscured;
- local part number correct;
- Week 1 font unchanged;
- organic balloons with speaker-directed tails;
- cream/yellow caption boxes;
- no balloon, narration box, or message box intersects character artwork;
- dedicated lettering bands are used whenever face-safe negative space is not
  proven;
- no speaker or caption labels printed in the art;
- Malik, Julian, and DJ visibly distinct;
- one page mark per comic page;
- exact dialogue and captions;
- one approved closing card.

Run the bundled verifier after packaging:

```bash
python3 skills/comic-lettering-continuity/scripts/verify_week_release.py \
  --repo . --week 2 --first-episode 8 --count 7
```

Use a Python environment with Pillow. The verifier checks the leaf-logo pixels,
local part sequence, locked font and box metadata, mandatory face-clearance
metadata, page-mark metadata, required page count, and byte-identical approved
end cards. Visual inspection remains required for tail direction and character
silhouettes.

Do not call a weekly batch complete until every check passes.
