# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A personal collection of [Manim Community](https://www.manim.community/) (>=0.22, Python 3.12, managed with `uv`) scenes for YouTube videos and experiments. There is no test suite, linter, or build step; "running" code means rendering a scene. The global Scala/Maven rules in `~/.claude/AGENTS.md` do not apply here.

## Setup and rendering

```sh
uv sync                      # or: pip install -e .   (puts src/ on the path via setuptools package-dir)
manim -c dev_sim.cfg src/light/scenes.py <SceneName>   # fast preview render of a simulation scene
```

Imports are rooted at `src/` (e.g. `from utils.MeineLiebeScene import MeineLiebeScene`), so the editable install (or running with `src` on `PYTHONPATH`) is required.

`python` and `manim` are not on PATH in this environment: run `.venv/Scripts/manim.exe` and `.venv/Scripts/python.exe` from the repo root, or activate the venv first. Any `*_short.cfg` profile is a vertical 9:16 Short; the others are 16:9.

Render profiles are manim config files passed with `-c`; they differ only in resolution/fps/outputs (all use the cairo renderer):

| File | Use |
|---|---|
| `dev.cfg` | 1280x720 @60fps, opens preview |
| `dev_short.cfg` | 720x1280 (vertical/Shorts) @60fps, opens preview |
| `dev_sim.cfg` / `dev_sim_short.cfg` | same as the two above, with caching disabled, for simulation scenes |
| `pro.cfg` | 2560x1440 @240fps, saves PNGs and sections |
| `pro_sim.cfg` / `pro_sim_short.cfg` | 2560x1440 / 1440x2560 @120fps, saves PNGs |
| `pro_thumbnail.cfg` | single PNG frame, 2560x1440 |

Output goes to `media/` (gitignored).

## Architecture

- `src/utils/` — shared helpers used by every video.
  - `MeineLiebeScene` is the base `Scene` for nearly all scenes. It sets default `Tex`/`Text` font size to 60, shows a debug frame counter (`scene_number`) only when `config.preview` is on, and overrides `next_section` to save a PNG of the previous section's last frame to `media/images/<SceneClass>/NNNN_<section>.png` (used for thumbnails/stills). New scenes should subclass it rather than `Scene`.
  - `SourceCode` renders code listings (used with files under `code/` or `src/` next to a video); `FollowingLines` is another reusable mobject.
- `src/youtube/<video>/` — one package per published video, each with its scene module(s) plus local assets (`svg/`, `code/`, `src/*.java`). Asset paths are often relative (e.g. `SourceCode("code/stack.txt", ...)`), so render from the directory the scene expects or check how the path is resolved before moving files.
- `src/background_noise/` — looping ambient scenes (DVD logo, network).
- `src/light/` — the most active work: particles of light bouncing inside a shape. `boundaries.py` has the `Boundary` ABC (signed-distance `sdf_many`/`normal_many` vectorised over `(N, 2)` numpy arrays, numerical-gradient normals by default) and concrete shapes like `RectBoundary`; `world.py` has `World`, built from a boundary, a cannon and a duration: each `step(dt)` fires whatever the cannon has released by then, advances all live points in batch and reflects them off the boundary ; `World.to_mobject(dot_radius, scene)` returns its own view (boundary plus dots, with the per-frame updaters attached; the scene is needed to play spawn sounds), so scenes only build the world and add that view; the view holds only dots that have been fired and lie within the frame plus `view_margin` (0.5 units by default), adding and removing them as they cross that line, so unfired and far-off dots cost nothing to render; `cannon.py` has the `Cannon` interface, which decides how dots are created, with three kinds: `RadialCannon` (a fixed `amount` of dots in evenly spaced directions, `spawn_rate` `INSTANT` or dots per second), `StreamCannon` (one direction, one speed, firing at a finite rate until the scene ends or its `firing_time` runs out, sized by `amount_for(simulation_time)`) and `WideCannon` (like a stream, but each dot starts at a random point of a face of the given `width` perpendicular to `direction`, placed by a `distribution` from `distribution.py`: `Uniform`; `Normal(sigmas)`, where the face spans that many standard deviations and samples outside it are redrawn; `Bimodal`, two such peaks centred on each half of the face; or `Arcsine(edge)`, densest at the two edges, the Beta shape `edge` defaulting to the classical 0.5 and smaller values pushing more dots outward; `seed` makes renders repeatable); each cannon takes a `coloring` from `coloring.py` (`StaticColor`, `Palette` of color groups, or `Gradient` across the dots in firing order) and a `sound` from `sound.py` (`Silence` by default, or `Sample(path, gain, every, every_jitter, gain_jitter, seed)`, which the world plays through the scene on a schedule of firing indexes where each gap between pops is a normal draw around `every` with standard deviation `every_jitter`, each pop's gain a normal draw around `gain`, and each pop placed at a random moment within its frame, all deterministic per `seed` and free of any fixed grid so cannons do not fall into a shared beat; keep `every` high enough that a 120-dots-per-second lane does not add thousands of clips and slow the final audio mix, and give cannons that fire in step different seeds or they pop in sync). Sounds are added only while frames are actually rendered, and a cached partial movie would be reused silently, so the `dev_sim` and `pro_sim` render configs set `disable_caching = true`; render simulation scenes with those, or pass `--disable_caching` yourself with any other config; `scenes.py` has `BoundaryScene` plus one scene per shape, each configured with a `boundary` and a `cannon` (the scene docstrings hold the YouTube metadata), and two boundary-free demos of the spawn distributions built with `wide_lane`: `WideCannonsLight` (16:9, four lanes firing upward) and `WideCannonsShortLight` (9:16, all six distributions stacked as horizontal lanes, each spawn playing `assets/bubble.wav`). `MirrorPath` (in `boundaries.py`) puts a mirror at every corner of a polyline so a stream fired along its first segment traces the whole line; `lettering.py` builds such a polyline for the word MATH, and `MathShortLight` traces it in 9:16 (render it with `dev_sim_short.cfg` or `pro_sim_short.cfg`, at 60 fps or more so dots cannot tunnel through the thin mirrors). `letters.py` has one 9:16 scene per capital letter (`AShortLight` to `ZShortLight`) drawn by a `WideCannon` beam: each letter is a list of straight passes inside a 3x4 box (`alphabet.py`), and `letter_path` turns them into one mirrored path by routing the beam off-screen between passes on concentric rectangular rings, picking for each transition the first ring whose mirrors stay clear of every other beam line; the scene base `LetterShortLight` builds the mirrors (each exactly as long as the beam's footprint at its incidence angle, since `MirrorPath` takes per-mirror half-lengths), the cannon, which fires until the beam fills the whole path and then `hold_time` seconds more so the complete letter is lit at once, and a `simulation_time` long enough for the last dot to leave the frame; everything outside the box plus half a beam width is dimmed by a translucent black veil made of four non-overlapping strips (overlapping ones would darken the corners twice), and the mirrors are 0.14 thick (`mirror_radius` 0.07) so the speed-7 dots cannot tunnel through at 60 fps. Off-screen routing dominates how long a letter takes to appear, so prefer one pass (a closed rectangle is one pass that leaves through its own starting corner) and, between passes, make the exit and the next entry cross the same side of the frame at right angles, which keeps the detour short. Design rules the router cannot bend: a mirror blocks every other pass, two mirrors cannot share a point, strokes may only end on other strokes at the box edge (the beam passes straight through and vanishes behind the curtain), and the beam never reverses, except that a last pass may end on an earlier pass's mirror (the Y's stem on the V's vertex), which sends the beam back along the whole path and out through the cannon's entry line, doubling the video. Closed shapes therefore use a straight pass-through side, and gentle turns are out because a small deflection is a grazing hit whose mirror footprint exceeds 2 units, so every corner deflects by about 90 degrees or more and the letters are square or sharply pointed. The scratchpad-free way to check a letter is `letter_path` plus a `World` simulation: every dot inside the window must lie on a visible stroke, every stroke must be traversed, and the window must be empty before `simulation_time`. `base.py` holds `BoundaryScene` and `ASSETS_DIR` for both scene modules. Render scenes from `scenes.py` or `letters.py`.
- `src/tests/` — experiments and physics/visual sandboxes (misnamed: not automated tests). Several files here have non-identifier names (`3x+1.py`) and must be run by path.
- `assets/` — shared sound effects (`ball_hit*.wav`).

## Notes

- `README.md` refers to the package as `manim_i`; the project is actually named `manim-me` and imports resolve from `src/`.
- `media/`, `build/`, `.venv/`, and `.idea/` are gitignored; don't commit renders.
