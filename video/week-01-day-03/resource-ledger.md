# Week 1 Day 3 Video Resource Ledger

## Measurement Boundary

Codex does not expose this task's weekly allocation percentage or token count to the workspace. This ledger records the measurable inputs needed to estimate cost: prompt/narration words, external calls, produced audio duration, rendered frames, elapsed render time, and output size.

## Planned Operations

| Operation | Quantity | Measurable unit | Token telemetry |
| --- | ---: | --- | --- |
| Full-cast TTS | 33 utterances | source words and API calls | Not exposed |
| Word-level transcription | 5 scene tracks | audio seconds and API calls | Not exposed |
| Draft render | 1 | frames, seconds, output bytes | Not exposed |
| Final render | 1 | frames, seconds, output bytes | Not exposed |

## Actual Operations

| Full-cast TTS | 33 API calls | 289 normalized source words; 142.116 seconds of assembled audio | Not exposed |
| Word-level transcription | 5 API calls | 287 word timestamps; normalized similarity 1.0 | Not exposed |
| Draft render | 1 local render | 4,624 frames; 97 seconds; 34.2 MB | Not exposed |
| Final render | 1 local render | 4,624 frames; 176 seconds; 85.7 MB | Not exposed |

## Planning Estimate

For a similar five-scene, 2.5-minute captioned episode, budget 33 TTS calls, 5 transcription calls, one draft render, and one high-quality render. The external API calls are the billable steps; the local renders primarily consume workstation time. The app's weekly allocation percentage and internal-token accounting remain unavailable to this workspace.
