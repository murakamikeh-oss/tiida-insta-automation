#!/usr/bin/env python3
"""Render verified @tiida_saga post-performance metrics for the 2026-09-05 analysis."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager

OUTPUT = Path(__file__).resolve().parents[1] / "reports" / "assets" / "tiida_performance_20260905.png"
POSTS = [
    {"label": "8/31\n22:23\nCarousel", "reach": 47, "views": 141, "interactions": 6},
    {"label": "9/2\n06:54\nReel", "reach": 72, "views": 105, "interactions": 6},
    {"label": "9/4\n19:43\nCarousel", "reach": 25, "views": 61, "interactions": 2},
    {"label": "9/5\n06:51\nReel", "reach": 36, "views": 57, "interactions": 1},
]


def choose_font() -> str:
    candidates = ["Noto Sans CJK JP", "Noto Sans JP", "IPAexGothic", "DejaVu Sans"]
    installed = {f.name for f in font_manager.fontManager.ttflist}
    return next((font for font in candidates if font in installed), "DejaVu Sans")


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    labels = [post["label"] for post in POSTS]
    reach = [post["reach"] for post in POSTS]
    views = [post["views"] for post in POSTS]
    interactions = [post["interactions"] for post in POSTS]
    font = choose_font()

    plt.rcParams["font.family"] = font
    plt.rcParams["axes.unicode_minus"] = False
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [1.55, 1]})
    fig.patch.set_facecolor("#FAFAF7")
    for axis in axes:
        axis.set_facecolor("#FAFAF7")

    x = range(len(POSTS))
    axes[0].bar([i - 0.19 for i in x], reach, width=0.38, color="#2A9D8F", label="Reach")
    axes[0].bar([i + 0.19 for i in x], views, width=0.38, color="#264653", label="Views")
    axes[0].set_title("@tiida_saga: reach and views by post", fontsize=14, fontweight="bold", loc="left")
    axes[0].set_ylabel("Accounts / plays")
    axes[0].set_xticks(list(x), labels, fontsize=10)
    axes[0].set_ylim(0, 165)
    axes[0].grid(axis="y", alpha=0.18)
    axes[0].spines[["top", "right", "left"]].set_visible(False)
    axes[0].legend(frameon=False, loc="upper right")

    rates = [value / reach_value * 100 for value, reach_value in zip(interactions, reach)]
    bars = axes[1].bar(range(len(POSTS)), rates, color=["#E76F51", "#F4A261", "#E9C46A", "#B9C6AE"])
    axes[1].set_title("Interaction rate by reach", fontsize=14, fontweight="bold", loc="left")
    axes[1].set_ylabel("Interactions / reach (%)")
    axes[1].set_xticks(range(len(POSTS)), ["8/31", "9/2", "9/4", "9/5"])
    axes[1].set_ylim(0, 15)
    axes[1].grid(axis="y", alpha=0.18)
    axes[1].spines[["top", "right", "left"]].set_visible(False)
    for bar, rate, count in zip(bars, rates, interactions):
        axes[1].text(bar.get_x() + bar.get_width() / 2, rate + 0.35, f"{rate:.1f}%\n({count})", ha="center", va="bottom", fontsize=10)

    fig.suptitle("2026-08-29 to 2026-09-05 (JST) · Verified Insights", x=0.07, y=0.98, ha="left", color="#5E6472", fontsize=11)
    fig.text(0.07, 0.01, "Interactions = likes + comments + shares + saves. Reach totals are post-level and should not be treated as unique accounts.", fontsize=9, color="#5E6472")
    fig.tight_layout(rect=(0, 0.05, 1, 0.93))
    fig.savefig(OUTPUT, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())


if __name__ == "__main__":
    main()
