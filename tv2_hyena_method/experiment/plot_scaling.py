"""
plot_scaling.py — Vẽ biểu đồ scaling từ E2/E3 CSV.
TV2 deliverable (phan_cong §8.2: phần scaling runtime).

Usage:
  python tv2_hyena_method/experiment/plot_scaling.py

Input:
  E2_transformer_scale.csv, E3_hyena_scale.csv  (cùng thư mục hoặc results/)
Output:
  scaling_time.png        — time/step vs seq_len (log-log) + điểm crossover
  scaling_throughput.png  — throughput vs seq_len
"""
import csv
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]  # repo root
RESULTS = ROOT / "results"


def load(path):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            if r["time_ms"] == "OOM":
                continue
            rows.append((int(r["seq_len"]), float(r["time_ms"]),
                         float(r["throughput"])))
    rows.sort()
    return rows


t = load(HERE / "E2_transformer_scale.csv")
h = load(HERE / "E3_hyena_scale.csv")

tL = [r[0] for r in t]; tT = [r[1] for r in t]
hL = [r[0] for r in h]; hT = [r[1] for r in h]
tThru = [r[2] for r in t]; hThru = [r[2] for r in h]

# màu theo visual_checklist: xanh Transformer, đỏ/cam Hyena
C_T, C_H = "#2563eb", "#ea580c"

# ── Plot 1: time vs L (log-log) ──────────────────────────────
fig, ax = plt.subplots(figsize=(7.5, 5))
ax.loglog(tL, tT, "o-", color=C_T, linewidth=2.2, markersize=8, label="Transformer (Attention)")
ax.loglog(hL, hT, "s-", color=C_H, linewidth=2.2, markersize=8, label="Hyena")

# tham chiếu O(L^2) và O(L log L)
import numpy as np
Lref = np.array(sorted(set(tL + hL)))
# normalize tại L=256
base = 256
t_at_256 = tT[0]
ax.loglog(Lref, t_at_256 * (Lref / base) ** 2, ":", color=C_T, alpha=0.5,
          label=r"$O(L^2)$ tham chiếu")
h_at_256 = hT[0]
ax.loglog(Lref, h_at_256 * (Lref / base) * (np.log2(Lref) / np.log2(base)),
          ":", color=C_H, alpha=0.5, label=r"$O(L\log L)$ tham chiếu")

# tìm crossover (L lớn nhất chung)
common = sorted(set(tL) & set(hL))
cross = None
for i in range(1, len(common)):
    prev_t = tT[tL.index(common[i - 1])]; cur_t = tT[tL.index(common[i])]
    prev_h = hT[hL.index(common[i - 1])]; cur_h = hT[hL.index(common[i])]
    if (prev_h - prev_t) > 0 and (cur_h - cur_t) < 0:
        cross = common[i]
        break
if cross:
    ax.axvline(cross, color="#6b7280", linestyle="--", alpha=0.7)
    ax.text(cross, ax.get_ylim()[0] * 1.15, f"crossover\nL={cross}",
            fontsize=9, color="#6b7280", ha="center")

ax.set_xlabel("Sequence length L", fontsize=12)
ax.set_ylabel("Time / forward step (ms)", fontsize=12)
ax.set_title("Scaling: Transformer vs Hyena  (d_model=256, 4 layers, batch=8, MPS)",
             fontsize=11)
ax.grid(True, which="both", alpha=0.3)
ax.legend(fontsize=9, loc="upper left")
fig.tight_layout()
fig.savefig(HERE / "scaling_time.png", dpi=150)
plt.close(fig)

# ── Plot 2: throughput vs L ──────────────────────────────────
fig, ax = plt.subplots(figsize=(7.5, 5))
ax.plot(tL, [x / 1e3 for x in tThru], "o-", color=C_T, linewidth=2.2,
        markersize=8, label="Transformer")
ax.plot(hL, [x / 1e3 for x in hThru], "s-", color=C_H, linewidth=2.2,
        markersize=8, label="Hyena")
ax.set_xlabel("Sequence length L", fontsize=12)
ax.set_ylabel("Throughput (k tokens/s)", fontsize=12)
ax.set_title("Throughput vs L  — Hyena gần phẳng (O(L log L)),\nTransformer giảm nhanh (O(L²))",
             fontsize=11)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
fig.tight_layout()
fig.savefig(HERE / "scaling_throughput.png", dpi=150)
plt.close(fig)

print("✅ Saved:")
print("  ", HERE / "scaling_time.png")
print("  ", HERE / "scaling_throughput.png")
if cross:
    print(f"Crossover detected at L={cross}")
