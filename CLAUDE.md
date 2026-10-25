# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A personal collection of [Manim Community](https://www.manim.community/) (>=0.22, Python 3.12, managed with `uv`) scenes for YouTube videos and experiments. There is no test suite, linter, or build step; "running" code means rendering a scene. The global Scala/Maven rules in `~/.claude/AGENTS.md` do not apply here.

## Setup and rendering

```sh
uv sync                      # or: pip install -e .   (puts src/ on the path via setuptools package-dir)
manim -c dev.cfg src/light/scenes.py <SceneName>       # fast preview render
```

Imports are rooted at `src/` (e.g. `from utils.MeineLiebeScene import MeineLiebeScene`), so the editable install (or running with `src` on `PYTHONPATH`) is required.

Render profiles are manim config files passed with `-c`; they differ only in resolution/fps/outputs (all use the cairo renderer):

| File | Use |
|---|---|
| `dev.cfg` | 1280x720 @60fps, opens preview |
| `dev_short.cfg` | 720x1280 (vertical/Shorts) @60fps, opens preview |
| `prod_scene.cfg` | 2560x1440 @240fps, saves PNGs and sections |
| `prod_simulation.cfg` / `prod_simulation_short.cfg` | 2560x1440 / 1440x2560 @120fps, saves PNGs |
| `prod_thumbnail.cfg` | single PNG frame, 2560x1440 |

Output goes to `media/` (gitignored).

## Architecture

- `src/utils/` — shared helpers used by every video.
  - `MeineLiebeScene` is the base `Scene` for nearly all scenes. It sets default `Tex`/`Text` font size to 60, shows a debug frame counter (`scene_number`) only when `config.preview` is on, and overrides `next_section` to save a PNG of the previous section's last frame to `media/images/<SceneClass>/NNNN_<section>.png` (used for thumbnails/stills). New scenes should subclass it rather than `Scene`.
  - `SourceCode` renders code listings (used with files under `code/` or `src/` next to a video); `FollowingLines` is another reusable mobject.
- `src/youtube/<video>/` — one package per published video, each with its scene module(s) plus local assets (`svg/`, `code/`, `src/*.java`). Asset paths are often relative (e.g. `SourceCode("code/stack.txt", ...)`), so render from the directory the scene expects or check how the path is resolved before moving files.
- `src/background_noise/` — looping ambient scenes (DVD logo, network).
- `src/light/` — the most active work: particles of light bouncing inside a shape. `boundaries.py` has the `Boundary` ABC (signed-distance `sdf_many`/`normal_many` vectorised over `(N, 2)` numpy arrays, numerical-gradient normals by default) and concrete shapes like `RectBoundary`; `world.py` has `World`, built from a boundary, a cannon and a duration: each `step(dt)` fires whatever the cannon has released by then, advances all live points in batch and reflects them off the boundary ; `World.to_mobject(dot_radius, scene)` returns its own view (boundary plus dots, with the per-frame updaters attached; the scene is needed to play spawn sounds), so scenes only build the world and add that view; `cannon.py` has the `Cannon` interface, which decides how dots are created, with three kinds: `RadialCannon` (a fixed `amount` of dots in evenly spaced directions, `spawn_rate` `INSTANT` or dots per second), `StreamCannon` (one direction, one speed, firing at a finite rate until the scene ends or its `firing_time` runs out, sized by `amount_for(simulation_time)`) and `WideCannon` (like a stream, but each dot starts at a random point of a face of the given `width` perpendicular to `direction`, placed by a `distribution` from `distribution.py`: `Uniform`; `Normal(sigmas)`, where the face spans that many standard deviations and samples outside it are redrawn; `Bimodal`, two such peaks centred on each half of the face; or `Arcsine(edge)`, densest at the two edges, the Beta shape `edge` defaulting to the classical 0.5 and smaller values pushing more dots outward; `seed` makes renders repeatable); each cannon takes a `coloring` from `coloring.py` (`StaticColor`, `Palette` of color groups, or `Gradient` across the dots in firing order) and a `sound` from `sound.py` (`Silence` by default, or `Sample(path, gain, every, every_jitter, gain_jitter, seed)`, which the world plays through the scene for one dot in each block of `every` dots by firing index, the dot's position in the block and the clip's gain each offset by a normal draw with the given standard deviation, deterministic per `seed`; keep `every` high enough that a 120-dots-per-second lane does not add thousands of clips and slow the final audio mix, and give cannons that fire in step different seeds or they pop in sync). Sounds are added only while frames are actually rendered, so after a sound-only change render with `--disable_caching`, or the cached partial movie is reused silently; `scenes.py` has `BoundaryScene` plus one scene per shape, each configured with a `boundary` and a `cannon` (the scene docstrings hold the YouTube metadata), and two boundary-free demos of the spawn distributions built with `wide_lane`: `WideCannonsLight` (16:9, four lanes firing upward) and `WideCannonsShortLight` (9:16, all six distributions stacked as horizontal lanes, each spawn playing `assets/bubble.wav`). `MirrorPath` (in `boundaries.py`) puts a mirror at every corner of a polyline so a stream fired along its first segment traces the whole line; `lettering.py` builds such a polyline for the word MATH, and `MathShortLight` traces it in 9:16 (render it with `dev_short.cfg` or `prod_simulation_short.cfg`, at 60 fps or more so dots cannot tunnel through the thin mirrors). `ZShortLight` does the same for a single Z with a `WideCannon` beam, so its two mirrors get a `half_length` longer than the beam's width divided by the cosine of the incidence angle. Render scenes from `scenes.py`.
- `src/tests/` — experiments and physics/visual sandboxes (misnamed: not automated tests). Several files here have non-identifier names (`3x+1.py`) and must be run by path.
- `assets/` — shared sound effects (`ball_hit*.wav`).

## Notes

- `README.md` refers to the package as `manim_i`; the project is actually named `manim-me` and imports resolve from `src/`.
- `media/`, `build/`, `.venv/`, and `.idea/` are gitignored; don't commit renders.
