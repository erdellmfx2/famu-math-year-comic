# FAMU Math Comic Video Conventions

## Source Priority

Read these active sources before building a video:

1. `story/approval_status.json`
2. `story/timeline-weeks/<week>.md`
3. `story/timeline-weeks-prose-v2/prose_<week>.md`
4. `story/setting_bible_v2.md`
5. `story/character_bible_v2.md`
6. `art/style_guide.md`
7. `audio/voice-casting/README.md`
8. The matching storyboards under `art/storyboards/week-XX/`
9. Relevant active files under `art/final/week-XX/episode-YY/`

Read individual character casting files only for characters who speak in the selected episode.

## Episode Mapping

- Week numbers map to `timeline-weeks/<week>.md` and `prose_<week>.md`.
- Episode numbers map to the dated daily sections within that week.
- Match a day by date, heading, and required story event. Do not rely only on "first section equals episode one" when headings or production order differ.
- Use the outline to confirm the event and handoff.
- Use the prose as the exact narration source.
- Treat `story/approval_status.json` as authoritative when an old timeline or production note still says approval is pending.
- Do not narrate the dated Markdown heading unless the user explicitly includes it in the performance.

## Visual Asset Priority

Use the following order:

1. Approved title card from the episode's current `sequence-v2/` or current packaged sequence.
2. Unlettered files named `*-art-vN.png` or other explicitly approved unlettered pages.
3. Current foundational character, environment, and prop assets only when the user approves additional visual construction.
4. Approved closing card from the episode package or `art/final/series-endcards/approved/`.

Treat `*-lettered-vN.png` and packaged comic pages as reading references, not narration backgrounds. Never use a path containing `archive/`.

## Visual Identity

- Fictional setting: McCall-Hart University in Bellwether, Alabama.
- Palette: indigo, copper, cream, cypress gray, warm limestone, and dark walnut.
- Campus cues: honey brick, pale limestone, wrought iron, live oaks, magnolias, cypress trees, and copper sunset light.
- Preserve established character appearance, wardrobe logic, props, architecture, and panel order.
- Do not introduce real-university buildings, official marks, green-and-orange legacy identity, snake imagery, or unrelated generated filler.

## Required Video Order

1. Approved title card.
2. Narrated story over scene-matched unlettered art.
3. Exactly one approved message card.

Keep title and message cards intact. Do not crop away their wording or add replacement labels.

When a card is not the same aspect ratio as the video, contain the whole card over a deep-indigo matte or a softly blurred copy of that same card. Do not stretch or crop it to 9:16.

## Voice Continuity

- Use `audio/voice-casting/narrator.md` as the current direction for narrated prose.
- For full cast, use the speaker's individual casting file.
- Treat a casting file marked proposed as an audition direction until the user accepts that setup.
- Reuse a previously accepted voice setup when the user requests no casting change.
- Keep mathematical language confident and clear.
- Preserve natural pauses, humor, and conversational tension.
- Do not imitate a real person or add stereotyped accents.
- Include an AI-generated-voice disclosure in publication notes.
