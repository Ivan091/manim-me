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
- `src/light/` — the most active work: particles of light bouncing inside a shape. `boundaries.py` has the `Boundary` ABC (signed-distance `sdf_many`/`normal_many` vectorised over `(N, 2)` numpy arrays, numerical-gradient normals by default) and concrete shapes like `RectBoundary`; `world.py` has `World`, which advances all points in batch and reflects them off a boundary; `cannon.py` has `Cannon`, which decides how dots are created (origin, amount, velocity, colors, and `spawn_rate`: `INSTANT` or dots per second); `scenes.py` has `BoundaryScene` plus one scene per shape, each configured with a `boundary` and a `cannon` (the scene docstrings hold the YouTube metadata). Render scenes from `scenes.py`.
- `src/tests/` — experiments and physics/visual sandboxes (misnamed: not automated tests). Several files here have non-identifier names (`3x+1.py`) and must be run by path.
- `assets/` — shared sound effects (`ball_hit*.wav`).

## Notes

- `README.md` refers to the package as `manim_i`; the project is actually named `manim-me` and imports resolve from `src/`.
- `media/`, `build/`, `.venv/`, and `.idea/` are gitignored; don't commit renders.
