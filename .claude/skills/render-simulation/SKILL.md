---
name: render-simulation
description: Render a simulation scene from this repo (the light scenes in src/light/scenes.py, or any other scene the user names) with the right render profile, wait for the output and report where the video landed. Invoke whenever the user asks to render, preview, re-render, or produce the final video of a scene, or to check how a scene looks after a change.
---

# render-simulation

Render one scene with manim and report the result. The scene code is the source of truth; this skill only runs it. Profiles, their resolutions and frame rates, and how to call manim are documented in `CLAUDE.md` (Setup and rendering); this skill only decides which profile to use and checks the output.

## Hard rules

- **Render only the scenes the user names.** If no scene is named, ask once; do not render every scene in the file.
- **Run from the repo root** with the venv executables named in `CLAUDE.md`, so that `src/` imports resolve.
- **Simulation scenes always use a `*_sim*.cfg` profile.** These disable caching, which matters because spawn sounds are added only while frames are actually rendered; a cached partial movie would be reused silently. Pass `--disable_caching` yourself if the user insists on another profile for a scene with sound.
- **Never lower the frame rate below 60 fps** for scenes with `MirrorPath` mirrors (`MathShortLight`, `ZShortLight`); dots tunnel through the thin mirrors otherwise. The sim profiles already satisfy this.
- **Do not edit scene code** to make a render work. Report the failure instead.
- **Do not commit renders.** `media/` is gitignored.

## Choosing the profile

- `dev_sim` by default; `pro_sim` when the user asks for the final, production, publish or high-quality render.
- The `*_short.cfg` variant for vertical scenes: class names containing `Short`, or any scene the user calls a Short.
- Say which profile you are using. The dev profiles open a preview window when the render finishes; that is expected.

## Workflow

1. **Locate the scene.** Confirm the class exists in the named module (default `src/light/scenes.py`) with Grep. Note `simulation_time` so you can estimate the render.
2. **Choose the profile** as above.
3. **Render** from the repo root, for example:

   ```bash
   .venv/Scripts/manim.exe -c dev_sim_short.cfg src/light/scenes.py ZShortLight
   ```

   A 60 fps dev render takes roughly 10 seconds of wall time per second of video for a few thousand dots; a `pro_sim` render takes several times that. Run anything expected to exceed a minute in the background and wait for the notification instead of polling.
4. **Check the result.** The video lands in `media/videos/<module>/<quality>/<Scene>.mp4` (for `src/light/scenes.py`, `<module>` is `scenes`). Confirm the file exists and is new. Skim the log for warnings and tracebacks. For a scene with sound, confirm the mp4 has an audio stream (PyAV is installed: open the file and list `container.streams`).
5. **Show a frame only when asked.** `-s` renders just the last frame without running updaters, so it shows a simulation before it starts; to show a frame of a simulation, decode one from the finished mp4 with PyAV and save it in the scratchpad.
6. **Report** the profile, the output path, the render time, and anything odd in the log. If the render failed, give the traceback and stop.
