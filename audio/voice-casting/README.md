# The Formula of Becoming Voice Cast

## Status

These are proposed synthetic voice assignments for audition and approval. Keep one base voice and one performance-instruction block per character throughout season one. Do not imitate a real person or use exaggerated racial, regional, or class markers.

The production voice model may change, but the character direction in these files is the continuity lock. Current presets use supported OpenAI built-in voice IDs.

Name pronunciations are locked in
[`pronunciation-lexicon.json`](pronunciation-lexicon.json). Voice generation must load that
file and append every matching character instruction without changing the written dialogue
or caption spelling.

## Cast Index

| Character | Story function | Base voice | Casting file |
|---|---|---|---|
| Narrator | Warm story guide | `cedar` | [narrator.md](narrator.md) |
| Malik Baptiste | Co-lead | `ash` | [malik-baptiste.md](malik-baptiste.md) |
| Nia Reynolds | Co-lead | `coral` | [nia-reynolds.md](nia-reynolds.md) |
| Julian Cross | Fall relationship and media collaborator | `verse` | [julian-cross.md](julian-cross.md) |
| Simone Hart | Analytics teammate and spring relationship | `marin` | [simone-hart.md](simone-hart.md) |
| Darius "DJ" Cole | Malik's roommate and athlete | `echo` | [dj-cole.md](dj-cole.md) |
| Keisha Morgan | Nia's roommate and research co-lead | `sage` | [keisha-morgan.md](keisha-morgan.md) |
| Imani Cole | Older-student mentor | `alloy` | [imani-cole.md](imani-cole.md) |
| Dr. Camille Brooks | Calculus I professor | `marin` | [dr-camille-brooks.md](dr-camille-brooks.md) |
| Dr. Victor Delgado | Calculus II professor | `onyx` | [dr-victor-delgado.md](dr-victor-delgado.md) |
| Dr. Renee Okafor | Calculus III and research professor | `marin` | [dr-renee-okafor.md](dr-renee-okafor.md) |
| Dr. Isaac Bennett | Analytics coach and career mentor | `echo` | [dr-isaac-bennett.md](dr-isaac-bennett.md) |
| Dr. Alana Price | Applied mathematics and research mentor | `ballad` | [dr-alana-price.md](dr-alana-price.md) |
| Celeste Baptiste | Malik's mother | `shimmer` | [celeste-baptiste.md](celeste-baptiste.md) |
| Marcel Baptiste | Malik's father | `onyx` | [marcel-baptiste.md](marcel-baptiste.md) |
| Micah | Malik's 12-year-old cousin | `nova` | [micah.md](micah.md) |
| Denise Reynolds | Nia's mother | `sage` | [denise-reynolds.md](denise-reynolds.md) |
| Alexis Grant | Graduate research mentor | `alloy` | [alexis-grant.md](alexis-grant.md) |
| Elaine Carter | Community preparedness reviewer | `cedar` | [elaine-carter.md](elaine-carter.md) |
| Ms. Alvarez | North Star supervisor | `shimmer` | [ms-alvarez.md](ms-alvarez.md) |
| Zoe | Curious seventh-grade student | `fable` | [zoe.md](zoe.md) |
| DJ's auntie | Family and game-day supporting voice | `coral` | [dj-auntie.md](dj-auntie.md) |

## Production Rules

1. Generate a short audition before producing a full episode.
2. Judge voices in dialogue pairs, especially Malik/Nia, Nia/Julian, Malik/Simone, and student/faculty scenes.
3. Preserve natural pauses and conversational overlap in editing; do not make every line sound like narration.
4. Give mathematical language confidence and clarity without turning it into a lecture unless the scene is explicitly instructional.
5. Re-render only the affected line when direction changes, then compare it in scene context.
6. Disclose that published voiceovers use AI-generated voices.
7. Generate each character's dialogue with that character's assigned voice ID; performance instructions are not a substitute for separate voices.
8. Apply `pronunciation-lexicon.json` to every generated utterance. Do not rely on a model's
   default pronunciation of a recurring name.
9. Recheck the pronunciation entry before changing a generated line. A pronunciation fix
   must not alter the prose text or on-screen caption spelling.

## Sources

- `story/character_bible_v2.md`
- `story/prose-v2-output/the-formula-of-becoming-prose-v2.md`
- `story/script-v2-output/the-formula-of-becoming-script-v2.md`
