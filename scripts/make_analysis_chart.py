#!/usr/bin/env python3
"""分析レポート用のグラフを生成する。"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "reports" / "data_20261107.json").read_text(encoding="utf-8"))

# 日本語フォント
candidates = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
]
for path in candidates:
    if Path(path).exists():
        font_manager.fontManager.addfont(path)
plt.rcParams["font.family"] = "Noto Sans CJK JP"
plt.rcParams["axes.unicode_minus"] = False

accounts = [a for a in data["accounts"] if a["post_count"] > 0]
accounts.sort(key=lambda a: a["avg_likes"])

labels = [a["handle"] for a in accounts]
colors = ["#d95f02" if a.get("is_own") else "#4c78a8" for a in accounts]

fig, axes = plt.subplots(1, 2, figsize=(13, 5.6), dpi=180)

# 左：投稿あたり平均いいね
ax = axes[0]
vals = [a["avg_likes"] for a in accounts]
bars = ax.barh(labels, vals, color=colors, height=0.6)
for bar, a in zip(bars, accounts):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
            f"{a['avg_likes']:.1f}（{a['post_count']}件）", va="center", fontsize=9)
ax.set_xlim(0, max(vals) * 1.35)
ax.set_xlabel("投稿あたり平均いいね数")
ax.set_title("① 投稿あたり平均いいね（2026/10/31〜11/06）", fontsize=12, pad=12)
ax.grid(axis="x", alpha=0.25, linestyle="--")
ax.set_axisbelow(True)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

# 右：フォロワーあたり反応率
ax = axes[1]
er = [a["engagement_rate_pct"] for a in accounts]
bars = ax.barh(labels, er, color=colors, height=0.6)
for bar, a in zip(bars, accounts):
    ax.text(bar.get_width() + 0.04, bar.get_y() + bar.get_height() / 2,
            f"{a['engagement_rate_pct']:.2f}%", va="center", fontsize=9)
ax.set_xlim(0, max(er) * 1.3)
ax.set_xlabel("（いいね＋コメント）÷フォロワー数 ÷ 投稿数（%）")
ax.set_title("② フォロワーあたり反応率（1投稿平均）", fontsize=12, pad=12)
ax.grid(axis="x", alpha=0.25, linestyle="--")
ax.set_axisbelow(True)
for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

fig.suptitle("Instagram 競合比較：直近1週間（自社＝オレンジ）", fontsize=14)
fig.text(0.5, 0.005,
         "出典：Instagram公開ページ（2026-11-07 14:20 JST取得）。保存・シェア・リーチは公開値では取得不可。",
         ha="center", fontsize=8, color="#555555")
fig.tight_layout(rect=(0, 0.03, 1, 0.95))
out = ROOT / "assets" / "analysis_20261107_engagement.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, bbox_inches="tight")
print("wrote", out)
