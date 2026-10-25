---
name: youtube-metadata
description: Add YouTube publishing metadata (title, description, tags, category, language, visibility, thumbnail text, hashtags, chapters) to a given Manim scene class in this repo, derived from what the scene actually renders. Invoke whenever the user asks to add, generate, update, or review YouTube metadata, a title, a description, or tags for a scene (e.g. one in src/light/light.py) they plan to publish.
---

# youtube-metadata

Add a `youtube_metadata` class attribute to one scene class so the publishing text lives next to the code that produces the video.

## Hard rules

- **One scene per run.** The user names the scene class (and file if ambiguous). If it is missing or ambiguous, ask once; do not guess.
- **Describe only what the code renders.** Read the scene and everything it inherits or configures (boundary shape, point count, speed, colors, `simulation_time`, sections, audio). Never invent effects, math claims, or facts the scene does not show.
- **Never fabricate external facts.** Links, channel name, social handles, music credits, and sponsor text are placeholders (`TODO:`) unless the user supplied them or they already exist in another scene's metadata in this repo.
- **Do not publish or upload anything.** This skill only edits source. Visibility defaults to `private`.
- **Edit only the named scene class.** Do not touch the base class or other scenes. Follow PEP 8 (79-column lines) and add no code comments.
- **Update in place.** If the scene already has `youtube_metadata`, show the user the diff of what changes instead of silently overwriting hand-written text; keep fields the user did not ask to change.

## Fields

Add the attribute as a plain dict literal, keys in this order:

```python
youtube_metadata = {
    "title": "...",
    "description": "...",
    "tags": [...],
    "hashtags": [...],
    "category": "Science & Technology",
    "language": "en",
    "visibility": "private",
    "made_for_kids": False,
    "thumbnail_text": "...",
    "chapters": [...],
}
```

- **title**: at most 100 characters, ideally under 70 so it is not truncated. Lead with the strongest searchable phrase (the shape and the phenomenon, e.g. "Light bouncing inside a hexagon"), no clickbait the video does not deliver, no emoji spam, no ALL CAPS.
- **description**: plain text, paragraphs separated by `\n\n`, under 5000 characters.
  1. A one- or two-sentence hook in the first ~150 characters (the part shown before "show more"), containing the main keywords.
  2. What the viewer is seeing, stated from the code (shape, number of points, how they move, what the colors mean).
  3. How it was made: Manim Community (`manim` version from `pyproject.toml`) and a short plain-language note on the simulation, only if true for the scene.
  4. `TODO:` lines for links, music/sound credits, and socials.
  5. The hashtags on the last line.
- **tags**: 8 to 15 entries, most specific first, total length under 500 characters including separators. Mix the specific (shape, "ray reflection", "billiards"), the tool ("manim", "python"), and the broad ("simulation", "mathematics", "physics visualization"). No repeats of the title wording as one long tag, no misleading tags.
- **hashtags**: at most 3 (YouTube ignores all if more than 15), each starting with `#`, no spaces. The first two also appear above the title on the watch page.
- **category**: one of YouTube's category names; default `Science & Technology`, use `Education` only when the scene teaches step by step.
- **language**: BCP-47 code of the spoken or on-screen text, `en` by default.
- **visibility**: `private`, unless the user says otherwise.
- **made_for_kids**: `False` unless the user says otherwise.
- **thumbnail_text**: at most 4 words, readable at small size, complementing (not repeating) the title.
- **chapters**: list of `"MM:SS Label"` entries, first at `00:00`, at least three, each at least 10 seconds apart. Include only if the scene uses `next_section` or has clearly distinct phases; otherwise use an empty list.

## Workflow

1. **Locate the scene.** Read the file and the scene class, including class attributes inherited from its base. Note the render profile if the user mentions one (`dev_short.cfg` and `prod_simulation_short.cfg` are vertical 9:16 Shorts; the others are 16:9).
2. **Detect Shorts.** If the video is for a vertical profile and 60 seconds or less (`simulation_time`), add `#Shorts` as one of the three hashtags and mention Shorts in the description only if it is short enough to qualify; do not add chapters.
3. **Gather facts** to use in the text: shape name and dimensions, `points_count`, `points_speed`, color groups (`colors_fractions`), `simulation_time`, and anything else in `construct`.
4. **Draft the fields** following the rules above. Prefer concrete wording over superlatives.
5. **Write the attribute** into the scene class, after its existing class attributes and before any methods, keeping the surrounding formatting.
6. **Verify.** Import the module (`python -c "import light.light"` from `src/`, or the equivalent for the file) to confirm it still loads, and check the limits above: title length, tag count and total length, hashtag count, description length, 79-column lines.
7. **Report.** Show the final title, description, tags, and hashtags, list every `TODO:` the user still has to fill in, and state that nothing was published.
