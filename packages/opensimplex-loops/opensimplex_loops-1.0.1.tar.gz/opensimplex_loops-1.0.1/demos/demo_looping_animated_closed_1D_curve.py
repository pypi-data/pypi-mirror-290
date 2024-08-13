#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dennis van Gils (https://github.com/Dennis-van-Gils)
"""

import sys

try:
    from matplotlib import pyplot as plt
    from matplotlib import animation
except ImportError:
    sys.exit("This demo requires the `matplotlib` package.")

import numpy as np
import opensimplex_loops as osl

N_FRAMES = 50
N_PIXELS = 256
FEATURE_SIZE = 10.0

# Generate noise
curve_stack = osl.looping_animated_closed_1D_curve(
    N_frames=N_FRAMES,
    N_pixels_x=N_PIXELS,
    t_step=0.1,
    x_step=1 / FEATURE_SIZE,
    seed=3,
    verbose=True,
)

# Plot
fig, ax = plt.subplots()
ax.plot((0, 2 * np.pi), (0, 0), color="red", linestyle="dashed", linewidth=1)
(curve,) = ax.plot(
    np.linspace(0, 2 * np.pi, N_PIXELS, endpoint=False), curve_stack[0]
)
ax.set_xlim((0, 2 * np.pi))
ax.set_ylim((-1, 1))
ax.set_xticks((0, np.pi, 2 * np.pi))
ax.set_xticklabels(("0", "1 $\pi$", "2 $\pi$"))
frame_text = ax.text(0, 1.02, "", transform=ax.transAxes)


def anim_init():
    curve.set_ydata(curve_stack[0])
    frame_text.set_text("")
    return curve, frame_text


def anim_fun(j):
    curve.set_ydata(curve_stack[j])
    frame_text.set_text(f"frame {j:03d}")
    return curve, frame_text


anim = animation.FuncAnimation(
    fig,
    anim_fun,
    frames=len(curve_stack),
    interval=40,
    init_func=anim_init,
    # blit=True,
)

# plt.grid(False)
# plt.axis("off")
plt.show()

# Export image to disk?
if 0:
    anim.save(
        "demo_looping_animated_closed_1D_curve.gif",
        dpi=120,
        writer="imagemagick",
        fps=25,
    )
