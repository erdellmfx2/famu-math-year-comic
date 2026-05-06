# Art Production Layer

This folder holds the assets and instructions used to turn story beats into drawn comic episodes.

## Structure
- `story/timeline-weeks/*.md` — short point by point form of the story being told broken down by week
- `story/timeline-weeks-prose/*.md`  — full prose of the story being told broken down by week
- `art/style_guide.md` — visual consistency rules for all comic images
- `art/assets/` — exported final comic pages/episodes
- `art/storyboards/` — panel-ready scripts and shot sheets
- `art/prompts/` — image-generation prompts or artist-ready drawing briefs
- `art/final/` — exported final comic pages/episodes

## Production Flow
The goal of this production flow is to convert the story of two mathematics students into comic as that will appeal to younger students who might be intersted in mathematics!
1. Start by finding the last panel created in `art/prompts/` and `art/final/`
2. Use `story/timeline-weeks/*.md` and `story/timeline-weeks-prose/*.md` to find the next week in the story.
3. Consult the `art/final/` to find info on backgrounds, characters, character expressions, props, and character wardrode.
4. Convert the selected week into a storyboard file save it to `art/storyboards/`
5. Build panel-specific visual prompts, each panel should have between 2 and 6 images. Each image should help express the storyboard in picture format
6. Review continuity against character bible and style guide
7. Use the Image-2 model to generate each panel image 
8. Export final episode assets into `art/final/` in the appropriate folder
