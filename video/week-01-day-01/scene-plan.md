# Week 1 Day 1 Scene Plan

## Release Structure

1. Approved title card
2. Eight full-cast prose chapters over unlettered comic panels
3. Approved Day 1 thank-you message card

The audio clips determine the final scene lengths. Each visual scene begins with its matching narration clip and remains on screen until that clip ends. Use a 0.25-second pause between prose chapters.

## Scene Map

| Scene | Narration | Visual source | Framing and motion |
|---|---|---|---|
| Title | None | `art/final/week-01/episode-01/sequence-v2/01-title-card-v2.png` | Full card, five-second hold, subtle push-in |
| 1 | `01-arrival.mp3`, 37.824s | `week-01-episode-01-art-v1.png`, upper-left panel | Malik and Eliza Moss Hall; slow zoom out with a slight leftward drift |
| 2 | `02-red-number.mp3`, 39.792s | `week-01-episode-01-art-v1.png`, upper-right panel | Hold Malik, laptop, notebook, and calculator; slow zoom out from the red graph |
| 3 | `03-first-joke.mp3`, 66.624s | `week-01-episode-01-art-v1.png`, lower-left panel | Keep both faces and Nia's headphones visible; slow zoom out across their eyeline |
| 4 | `04-two-kinds-of-plans.mp3`, 46.368s | `week-01-episode-01-art-v1.png`, lower-left panel | Reframe slightly wider than Scene 3; slow zoom out from Nia toward Malik |
| 5 | `05-dr-brooks.mp3`, 37.248s | `week-01-episode-01-art-v1.png`, lower-right panel | Begin on Dr. Brooks and slowly zoom out toward the full group |
| 6 | `06-the-situation.mp3`, 58.800s | `week-01-episode-01-art-v1.png`, lower-right panel | Emphasize Nia's diagram and Malik's notebook, then slowly zoom out |
| 7 | `07-visible-assumptions.mp3`, 24.048s | `week-01-episode-01-art-v1.png`, lower-right panel | Begin higher on Dr. Brooks and the board, then slowly zoom out |
| 8A | Opening through Nia's question | `week-01-episode-01-page-02-art-v1.png`, panel 1 | Lunch two-shot; subtle zoom out |
| 8B | Malik's repair explanation through Nia's spreadsheet line | Same page, panel 2 | Preserve both reactions; subtle zoom out |
| 8C | Malik's color correction and "Corporate yelling" | Same page, panel 3 | Keep the exchange centered; subtle zoom out |
| 8D | Final narrator reflection | Same page, panel 4 | Begin close enough to read Malik's expression, then slowly zoom out |
| Message | None | `art/final/week-01/episode-01/sequence-v2/04-thank-you-end-card-v1.png` | Full card, seven-second hold, subtle push-in, fade to indigo |

## Audio Direction

- Narrator: `cedar`, warm, grounded, observant, and quietly lyrical
- Malik: `ash`, precise, measured, guarded, and dry
- Nia: `coral`, lively, curious, playful, and emotionally available
- Dr. Brooks: `marin`, calm, warm, intellectually demanding, and clearly distinct from the narrator
- Preserve the prose wording and speaker order in `full-cast-manifest.json`
- Generate every speaker turn separately; never ask one voice to imitate the others
- Do not add music or sound effects in the first review render

## Verification Targets

- The title card is the first visible frame.
- Every prose chapter has audible full-cast narration from the OpenAI Audio API.
- Narrator, Malik, Nia, and Dr. Brooks use distinct voice IDs and separate generated files.
- Every narrated beat uses an unlettered comic panel matching the action.
- No speech bubbles or added captions appear.
- All visual scene changes use crossfades.
- Every story image uses a continuous, subtle Ken Burns zoom-out during narration.
- The thank-you message card is the final content scene.
- The rendered file is a 1080 x 1920 MP4 with audible narration.
