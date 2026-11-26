"""Erzeugt die Diagramme in docs/bilder aus den gemessenen Werten."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "docs" / "bilder"
C = ["#257de0", "#f47230", "#00b894"]
TXT, TXT2, GRID = "#191919", "#666666", "#e6e6e6"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10.5, "axes.edgecolor": GRID,
    "axes.labelcolor": TXT2, "xtick.color": TXT2, "ytick.color": TXT2, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False, "axes.axisbelow": True})

# --- Kennfeld FS 3601 (Raumeinfluss 0), gemessen K1-K2 ---
tag = {-3: 15442, -2: 15544, -1: 15762, 0: 15937, 1: 16097, 2: 16230, 3: 16297}
nacht = {"Sollwert −3": [None, 13410, 13855, 14170, 14590, 14954, 15250, 15438],
         "Sollwert 0 (Standard)": [14693, 14897, 15096, 15287, 15472, 15670, 15831, 15972],
         "Sollwert +3": [15491, 15610, 15737, 15860, 15976, 16116, 16225, 16294]}
nacht["Sollwert −3"][0] = 12964
pcb = (12883, 16370)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True, gridspec_kw={"width_ratios": [1, 1.4]})
for ax in (a1, a2):
    ax.axhspan(*pcb, color="#f0f0f0", zorder=0)
a1.plot(list(tag), [v / 1000 * 1000 for v in tag.values()], color=C[0], lw=2, marker="o", ms=8,
        markeredgecolor="white", markeredgewidth=2)
a1.set_title("Tag ☼  –  Sollwertknopf", loc="left", color=TXT, fontsize=12)
a1.set_xlabel("Sollwert"); a1.set_ylabel("Widerstand K1–K2 [Ω]")
a1.set_xticks(list(tag)); a1.set_xticklabels(["−3", "−2", "−1", "Std", "+1", "+2", "+3"])
xs = list(range(2, 10))
for (name, vals), col in zip(nacht.items(), C):
    a2.plot(xs, vals, color=col, lw=2, marker="o", ms=8, markeredgecolor="white", markeredgewidth=2, label=name)
    a2.annotate(name, (9, vals[-1]), xytext=(8, 0), textcoords="offset points", va="center", color=TXT, fontsize=9.5)
a2.set_title("Nacht ☾  –  Absenkregler (bei drei Sollwerten)", loc="left", color=TXT, fontsize=12)
a2.set_xlabel("Nachtregler (2 = stärkste Absenkung, 9 = keine)")
a2.set_xlim(1.6, 11.2); a2.set_xticks(xs)
a2.legend(loc="lower right", frameon=False, fontsize=9.5)
a2.text(2.1, pcb[1] - 60, "Stellbereich der Platine (12,88 … 16,37 kΩ)", color=TXT2, fontsize=9, va="top")
fig.suptitle("Kennfeld der Wolf FS 3601 – gemessener Widerstand zwischen Klemme 1 und 2", x=0.01, ha="left",
             color=TXT, fontsize=13, fontweight="bold")
fig.tight_layout(); fig.savefig(OUT / "kennfeld_fs3601.png", dpi=150); plt.close(fig)

# --- Nachtvergleich ---
nights = ["24./25.11. Therme intern", "25./26.11. Fernversteller Nacht 6"]
data = [("Vorlauf Ø [°C]", [57.2, 52.1]), ("Rücklauf Ø [°C]", [54.3, 49.9]), ("Brennerlaufzeit [min]", [57.7, 51.6])]
fig, axs = plt.subplots(1, 3, figsize=(11, 3.8))
for ax, (title, v) in zip(axs, data):
    bars = ax.bar([0, 1], v, color=[C[0], C[1]], width=0.6, edgecolor="white", linewidth=2)
    ax.set_title(title, loc="left", color=TXT, fontsize=11)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Therme\nintern", "Nacht 6"])
    for b, val in zip(bars, v):
        ax.text(b.get_x() + b.get_width() / 2, val, f"{val:.1f}".replace(".", ","), ha="center", va="bottom", color=TXT)
    ax.set_ylim(0, max(v) * 1.18); ax.grid(axis="x", visible=False)
fig.suptitle("Zwei Nächte bei gleicher Außentemperatur (Ø +0,2 °C), jeweils 23:18–07:00", x=0.01, ha="left",
             color=TXT, fontsize=13, fontweight="bold")
fig.tight_layout(); fig.savefig(OUT / "nachtvergleich.png", dpi=150); plt.close(fig)
print("ok")
