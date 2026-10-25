def vertical_math_path(
    half_width: float = 1.35,
    height: float = 1.45,
    gap: float = 0.5,
    stem: float = 0.12,
    offscreen: float = 1.7,
) -> list[tuple[float, float]]:
    x, s = half_width, stem / 2
    top = (4 * height + 3 * gap) / 2
    t_m, t_a, t_t, t_h = (top - i * (height + gap) for i in range(4))
    b_m, b_a, b_t, b_h = (t - height for t in (t_m, t_a, t_t, t_h))
    v_m = b_m + 0.1 * height
    e_a = b_a + 0.45 * height
    c_a = b_a + 0.3 * height
    c_h = b_h + 0.5 * height
    left = -offscreen
    r1, r2, r3 = offscreen, offscreen + 0.15, offscreen + 0.3
    return [
        (left - 0.5, b_m),
        (-x, b_m),
        (-x, t_m),
        (0.0, v_m),
        (x, t_m),
        (x, b_m),
        (r1, b_m),
        (r1, b_a),
        (x, b_a),
        (x, e_a),
        (0.0, t_a),
        (-x, e_a),
        (-x, b_a),
        (left, b_a),
        (left, c_a),
        (r2, c_a),
        (r2, t_t),
        (s, t_t),
        (s, b_t),
        (-s, b_t),
        (-s, t_t),
        (left, t_t),
        (left, t_h),
        (-x, t_h),
        (-x, b_h),
        (left, b_h),
        (left, c_h),
        (r3, c_h),
        (r3, b_h),
        (x, b_h),
        (x, t_h),
        (r3 + 1.0, t_h),
    ]
