---
name: youtube-metadata
description: Add YouTube publishing metadata (title, description, tags, hashtags, category, language, visibility, thumbnail text) as a copy-ready docstring on the named Manim scene classes in this repo, derived from what each scene actually renders. Invoke whenever the user asks to add, generate, update, or review YouTube metadata, a title, a description, or tags for a scene (e.g. one in src/light/light.py) they plan to publish.
---

# youtube-metadata

Write the publishing text as the class docstring of a scene, so it lives next to the code that produces the video and can be copied straight into YouTube Studio.

## Hard rules

- **Work only on the scenes the user names** (one or several). If a scene is missing or ambiguous, ask once; do not guess.
- **Describe only what the code renders.** Read the scene and everything it inherits or configures (boundary shape, point count, speed, colors, `simulation_time`, sections, audio). Never invent effects, math claims, or facts the scene does not show.
- **Never fabricate external facts, and never leave placeholders.** Do not write `TODO:` lines. Links, channel name, social handles, music credits, and sponsor text are included only if the user supplied them; otherwise omit them entirely and mention in the report that the user can add them.
- **Do not publish or upload anything.** This skill only edits source. The visibility recorded in the docstring defaults to `public`; it is only text to copy, not a setting this skill applies.
- **Edit only the named scene classes.** Do not touch the base class or other scenes.
- **Docstring, not a field.** The metadata is the class docstring (`__doc__`), with no `youtube_metadata` attribute. A class that already has a metadata docstring or a legacy `youtube_metadata` dict is updated in place: show the user what changes instead of silently overwriting hand-written text, and keep fields the user did not ask to change.
- **No indentation inside the docstring.** Every line between the opening and closing quotes starts at column 0 (no leading spaces, even though the class body is indented), so a block copies out clean. Only the opening and closing `"""` lines keep the class-body indent. This is specific to this skill and overrides the usual docstring indentation.
- **Line length is 120 at most.** Every line of the docstring, including descriptions and tags, is at most 120 characters. Wrap longer paragraphs and the tags line at 120; blank lines still separate paragraphs, and never break a line inside a hyphenated word (it pastes as "off- center"). Tell the user in the report that wrapped lines carry line breaks when pasted.

## Docstring layout

The docstring is the first statement in the class body, with its content flush left at column 0. Section labels sit on their own line with the pasteable content directly below, so each block can be selected and copied on its own. Blank lines separate sections.

```python
class HexagonLight(BoundaryScene):
    """
Title:
Light Bouncing Inside a Hexagon

Description:
<hook paragraph>

<what-you-see paragraph>

<how-it-was-made paragraph>

#Manim #Simulation #Math

Tags:
tag one, tag two, tag three

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Six Colors
    """
```

- **Title**: at most 100 characters, ideally under 70 so it is not truncated. Lead with the strongest searchable phrase (the shape and the phenomenon, e.g. "Light Bouncing Inside a Hexagon"), no clickbait the video does not deliver, no emoji spam, no ALL CAPS.
- **Description**: plain text, paragraphs separated by one blank line, under 5000 characters.
  1. A one- or two-sentence hook in the first ~150 characters (the part shown before "show more"), containing the main keywords.
  2. What the viewer is seeing, stated from the code (shape, number of points, how they move, what the colors mean).
  3. How it was made: Manim Community (`manim` version from `uv.lock`) and a short plain-language note on the simulation, only if true for the scene.
  4. The hashtags on the last line, at most 3, each starting with `#`, no spaces. The first two also appear above the title on the watch page.
  - Add links, music credits, or socials as extra paragraphs only when the user supplied them.
- **Tags**: a comma-separated list, all lowercase (including proper nouns), 8 to 15 entries, most specific first, total length under 500 characters including separators. Mix the specific (shape, "ray reflection", "billiards"), the tool ("manim", "python"), and the broad ("simulation", "mathematics", "physics visualization"). No repeats of the title wording as one long tag, no misleading tags.
- **Category**: one of YouTube's category names; default `Science & Technology`, use `Education` only when the scene teaches step by step.
- **Language**: BCP-47 code of the spoken or on-screen text, `en` by default.
- **Visibility**: `public`, unless the user says otherwise.
- **Made for kids**: `no` unless the user says otherwise.
- **Thumbnail text**: at most 4 words, readable at small size, complementing (not repeating) the title.
- **Chapters**: add a `Chapters:` section (one `MM:SS Label` per line, first at `00:00`, at least three, each at least 10 seconds apart) only if the scene uses `next_section` or has clearly distinct phases. Otherwise omit the section.

## Example

`CircleLight` in `src/light/light.py` is the reference for tone, level of detail, and wrapping:

```python
class CircleLight(BoundaryScene):
    """
Title:
Light Bouncing Inside a Circle (Off-Center Source)

Description:
5,760 points of light start from one spot inside a circle and bounce off its wall for 15 seconds. The source is
off-center, so the pattern is not symmetric.

The circle has radius 2 and the source sits one third of the radius above the center. The points leave in 5,760 evenly
spaced directions at speed 1.3. The directions pointing left are blue and the directions pointing right are orange, so
you can follow where each half of the light ends up.

Made with Manim Community 0.22 in Python. Every dot is an independent point particle that moves in a straight line at
constant speed and reflects perfectly off the wall: the angle of incidence equals the angle of reflection. The
simulation is vectorised with NumPy, so all 5,760 points advance together every frame, and the exact moment each point
meets the wall is found by bisection.

#Manim #Simulation #Math

Tags:
circle billiard, off-center light source, mathematical billiards, dynamical billiards, reflection, light simulation,
manim, python, simulation, mathematics, physics visualization

Category: Science & Technology
Language: en
Visibility: public
Made for kids: no
Thumbnail text: Off-Center Source
    """
```

## Workflow

1. **Locate the scenes.** Read the file and each named scene class, including class attributes inherited from its base. Note the render profile if the user mentions one (`dev_short.cfg` and `prod_simulation_short.cfg` are vertical 9:16 Shorts; the others are 16:9).
2. **Detect Shorts.** If the video is for a vertical profile and 60 seconds or less (`simulation_time`), use `#Shorts` as one of the three hashtags and mention Shorts in the description only if it is short enough to qualify; omit chapters.
3. **Gather facts** to use in the text: shape name and dimensions, `points_count`, `points_speed`, color groups (`colors_fractions`, `colors_start_angle`), `simulation_time`, and anything else in `construct`.
4. **Draft the sections** following the rules above. Prefer concrete wording over superlatives.
5. **Write the docstring** as the first statement of each scene class, keeping the surrounding formatting, and remove any legacy `youtube_metadata` dict from that class.
6. **Verify.** Import the module (`python -c "import light.light"` from `src/`, or the equivalent for the file) to confirm it still loads, read each `__doc__` back, and check the limits above: title length, tag count and total length, hashtag count, description length, no line over 120 characters, and no leading spaces inside the docstring.
7. **Report.** List each scene's title and tags, say which extras (links, credits, socials) the user can still add, and state that nothing was published.
