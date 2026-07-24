# Week 02 Production Resource Ledger

## Starting Context

- Reported Codex weekly usage remaining before this batch: 52%.
- Reported Codex weekly usage remaining before the consistency rebuild: 40%.
- Production target: 7 episodes, 14 comic pages, two-pass art then lettering.
- Planned image operations: 14 unlettered page generations and 14 lettering edits.
- Token-meter limitation: the Codex weekly meter does not expose a per-call token count to this workflow. This ledger records prompt words, image calls, output files, and any model-reported usage; those are the auditable inputs for estimating weekly cost.

## Generation Log

| Operation | Page | Prompt words | Result | Available token usage |
| --- | --- | ---: | --- | --- |
| Generate | Episodes 08-14, Pages 1-2 unlettered | 14 calls | Accepted: 14 four-panel pages under `art/final/week-02/` | Not exposed |
| Finish | Episodes 08-14 lettering, page marks, title cards, and end-card packages | 0 calls | Completed with deterministic layout from approved assets | Not exposed |
| Export | Week 02 social-media PDF | 0 calls | Completed: 28-page PDF | Not exposed |
| Redesign | Julian and DJ continuity boards | 2 calls | Accepted: `char-julian-board-v2.png` and `char-dj-board-v2.png` | Not exposed |
| Rebuild | Episodes 08-14, Pages 1-2 unlettered v2 | 14 calls | Accepted: 14 replacement four-panel pages | Not exposed |
| Re-letter | Week 02 v2 title cards, balloons, captions, page marks, and packages | 0 calls | Completed with locked Week 1 deterministic renderer | Not exposed |
| Re-export | Week 02 v2 social-media PDF | 0 calls | Completed: 28-page PDF | Not exposed |
| Face-clear re-letter | Week 02 v3 comic pages with dedicated lettering bands | 0 calls | Completed: 14 corrected pages with unobstructed faces | Not exposed |
| Face-clear export | Week 02 v3 social-media PDF | 0 calls | Completed: 28-page PDF | Not exposed |

## Estimation Method

Estimate total effort from the recorded number of image operations and prompt words. The unlettered art pass used 14 image-model operations. To preserve the remaining weekly allocation, the final lettering and packaging pass used reproducible local composition rather than 14 additional image edits. Any future art regeneration is logged as an additional operation rather than hidden in the total.

The consistency rebuild used 16 additional successful image-model operations:
two new character continuity boards and fourteen replacement unlettered pages.
All title-card restoration, Part 1-7 numbering, Week 1 font locking, organic
speech balloons, cream caption boxes, page marks, packaging, verification, and
PDF export used local deterministic composition and no additional image calls.
The v3 face-clear correction and PDF rebuild also used local deterministic
composition and no additional image-model calls.
