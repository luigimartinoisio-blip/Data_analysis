"""
Script for Generating High-Impact Publication Figures for Phases 05 and 06
===========================================================================
Replicates the visual designs of:
- "fase 05a.png": 3-Panel Bivariate Semi-Log Scaling vs Sand, Silt, Clay
- "fase 05b.png": Unified Universal Exponential Scaling vs Fines
- "fase06.png": Master USDA Triangle + 4 Outer Regimes + Bottom Landslide Slope Profile

* Strictly adheres to user directive: "togli nei plot ogni traccia dell'eliminazione di ML6".
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import pearsonr, linregress
from scipy.signal import savgol_filter

# Output directories
BASE_DIR = Path(__file__).resolve().parents[1]
FIG_DIR_05 = BASE_DIR / "output" / "figures" / "fase05"
FIG_DIR_06 = BASE_DIR / "output" / "figures" / "fase06"
FIG_DIR_05.mkdir(parents=True, exist_ok=True)
FIG_DIR_06.mkdir(parents=True, exist_ok=True)

# Publication styling settings
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "legend.fontsize": 9,
    "figure.titlesize": 13,
    "lines.linewidth": 1.8,
    "axes.linewidth": 1.1,
    "xtick.major.width": 1.1,
    "ytick.major.width": 1.1,
    "xtick.minor.width": 0.8,
    "ytick.minor.width": 0.8,
    "axes.grid": True,
    "grid.alpha": 0.35,
    "grid.linestyle": "-",
    "grid.color": "#E2E8F0",
})

# Dataset of 7 validated cores (excluding ML6 completely)
DATA = [
    {"name": "Sand_R", "sand": 100.0, "silt": 0.0, "clay": 0.0, "fines": 0.0, "nA": 1.841, "alpha": 0.1825, "nVG": 8.395, "mVG": 0.8809, "D_EH": 2.09, "gap": 0.048, "marker": "s", "col": "#C85215", "offset_x": 2.0, "offset_y": 0.95},
    {"name": "ML7", "sand": 40.1, "silt": 41.7, "clay": 18.2, "fines": 59.9, "nA": 1.956, "alpha": 0.7566, "nVG": 1.244, "mVG": 0.1961, "D_EH": 9.97, "gap": 0.630, "marker": "o", "col": "#1B9E77", "offset_x": -7.0, "offset_y": 1.15},
    {"name": "ML4", "sand": 30.6, "silt": 44.7, "clay": 24.7, "fines": 69.4, "nA": 1.985, "alpha": 0.6310, "nVG": 1.192, "mVG": 0.1610, "D_EH": 12.33, "gap": 0.492, "marker": "^", "col": "#C51B7D", "offset_x": -6.5, "offset_y": 1.18},
    {"name": "ML8", "sand": 7.7, "silt": 69.5, "clay": 22.8, "fines": 92.3, "nA": 2.284, "alpha": 0.8390, "nVG": 1.117, "mVG": 0.1050, "D_EH": 21.75, "gap": 0.735, "marker": "p", "col": "#4575B4", "offset_x": -6.5, "offset_y": 0.95},
    {"name": "ML1", "sand": 7.6, "silt": 66.2, "clay": 26.2, "fines": 92.4, "nA": 3.249, "alpha": 0.2490, "nVG": 1.139, "mVG": 0.1220, "D_EH": 26.63, "gap": 0.776, "marker": "v", "col": "#8C510A", "offset_x": 2.0, "offset_y": 0.95},
    {"name": "ML10", "sand": 6.8, "silt": 60.2, "clay": 33.0, "fines": 93.2, "nA": 3.633, "alpha": 0.2356, "nVG": 1.159, "mVG": 0.1372, "D_EH": 26.48, "gap": 1.018, "marker": "D", "col": "#5AAE61", "offset_x": 2.5, "offset_y": 0.95},
    {"name": "ML9", "sand": 16.5, "silt": 57.3, "clay": 26.2, "fines": 83.5, "nA": 4.384, "alpha": 0.3732, "nVG": 1.138, "mVG": 0.1213, "D_EH": 36.14, "gap": 1.234, "marker": "o", "col": "#E6AB02", "offset_x": 2.0, "offset_y": 1.05},
]


# ==============================================================================
# 1. FIGURE FASE 05a: 3-Panel Bivariate Semi-Log Scaling vs Sand, Silt, Clay
# ==============================================================================
def generate_figure_05a():
    print("Generating Figure Fase 05a (Bivariate Semi-Log Scaling)...")
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 5.0), sharey=True)
    
    log_D = np.array([np.log10(d["D_EH"]) for d in DATA])
    
    fractions = [
        ("sand", "Sand Content [%]", "#1F78B4", 108, [-5, 108], [0, 20, 40, 60, 80, 100]),
        ("silt", "Silt Content [%]", "#2CA02C", 78, [-3, 75], [0, 10, 20, 30, 40, 50, 60, 70]),
        ("clay", "Clay Content [%]", "#984EA3", 50, [-2, 50], [0, 10, 20, 30, 40, 50]),
    ]
    
    custom_y_ticks = [2, 3, 4, 5, 6, 10, 20, 30, 40]
    custom_y_labels = [r"$2$", r"$3 \times 10^0$", r"$4 \times 10^0$", r"$5$", r"$6 \times 10^0$", r"$10$", r"$20$", r"$30$", r"$40$"]
    
    for ax, (key, label, line_col, max_x_fit, x_lim, x_ticks) in zip(axes, fractions):
        x = np.array([d[key] for d in DATA])
        res = linregress(x, log_D)
        r, p = pearsonr(x, log_D)
        
        # Regression curve
        x_grid = np.linspace(0, max_x_fit, 100)
        y_fit = 10**(res.intercept + res.slope * x_grid)
        ax.plot(x_grid, y_fit, color=line_col, linestyle="--", linewidth=2.0, zorder=3,
                label=rf"Exponential Fit" + "\n" + rf"$r = {r:+.3f}\ (p = {p:.3f})$")
        
        # Plot data points with specific markers and colors
        for d in DATA:
            ax.scatter(d[key], d["D_EH"], s=130, marker=d["marker"], facecolor=d["col"],
                       edgecolor="#222222", linewidth=1.2, zorder=5)
            
            # Label placement adjustments per panel
            lbl_x = d[key]
            lbl_y = d["D_EH"]
            
            if key == "sand":
                if d["name"] == "Sand_R":
                    ax.annotate("Sand_R", (lbl_x, lbl_y), xytext=(lbl_x - 18, lbl_y * 0.95), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML8":
                    ax.annotate("ML8", (lbl_x, lbl_y), xytext=(lbl_x - 8, lbl_y * 0.95), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML10":
                    ax.annotate("ML10", (lbl_x, lbl_y), xytext=(lbl_x - 10, lbl_y * 1.08), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML1":
                    ax.annotate("ML1", (lbl_x, lbl_y), xytext=(lbl_x + 2.5, lbl_y * 0.98), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML9":
                    ax.annotate("ML9", (lbl_x, lbl_y), xytext=(lbl_x + 2.5, lbl_y * 0.98), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML4":
                    ax.annotate("ML4", (lbl_x, lbl_y), xytext=(lbl_x - 5, lbl_y * 1.15), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML7":
                    ax.annotate("ML7", (lbl_x, lbl_y), xytext=(lbl_x - 3, lbl_y * 1.15), fontsize=10, fontweight="bold", color="#1E293B")
            elif key == "silt":
                if d["name"] == "Sand_R":
                    ax.annotate("Sand_R", (lbl_x, lbl_y), xytext=(lbl_x + 2.2, lbl_y * 0.95), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML7":
                    ax.annotate("ML7", (lbl_x, lbl_y), xytext=(lbl_x - 5.5, lbl_y * 1.15), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML4":
                    ax.annotate("ML4", (lbl_x, lbl_y), xytext=(lbl_x - 4.0, lbl_y * 1.20), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML9":
                    ax.annotate("ML9", (lbl_x, lbl_y), xytext=(lbl_x - 3.5, lbl_y * 1.12), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML10":
                    ax.annotate("ML10", (lbl_x, lbl_y), xytext=(lbl_x - 11.0, lbl_y * 0.95), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML1":
                    ax.annotate("ML1", (lbl_x, lbl_y), xytext=(lbl_x + 2.5, lbl_y * 1.05), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML8":
                    ax.annotate("ML8", (lbl_x, lbl_y), xytext=(lbl_x + 2.2, lbl_y * 0.95), fontsize=10, fontweight="bold", color="#1E293B")
            else: # clay
                if d["name"] == "Sand_R":
                    ax.annotate("Sand_R", (lbl_x, lbl_y), xytext=(lbl_x + 1.5, lbl_y * 0.95), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML7":
                    ax.annotate("ML7", (lbl_x, lbl_y), xytext=(lbl_x - 3.5, lbl_y * 1.12), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML4":
                    ax.annotate("ML4", (lbl_x, lbl_y), xytext=(lbl_x - 3.5, lbl_y * 1.15), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML8":
                    ax.annotate("ML8", (lbl_x, lbl_y), xytext=(lbl_x - 4.5, lbl_y * 0.95), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML9":
                    ax.annotate("ML9", (lbl_x, lbl_y), xytext=(lbl_x - 1.5, lbl_y * 1.15), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML1":
                    ax.annotate("ML1", (lbl_x, lbl_y), xytext=(lbl_x + 2.2, lbl_y * 0.95), fontsize=10, fontweight="bold", color="#1E293B")
                elif d["name"] == "ML10":
                    ax.annotate("ML10", (lbl_x, lbl_y), xytext=(lbl_x + 2.5, lbl_y * 1.02), fontsize=10, fontweight="bold", color="#1E293B")
                    
        ax.set_yscale("log")
        ax.set_ylim(1.6, 48)
        ax.set_xlim(x_lim)
        ax.set_xticks(x_ticks)
        ax.set_yticks(custom_y_ticks)
        ax.set_yticklabels(custom_y_labels)
        ax.set_xlabel(label, fontweight="bold", fontsize=11.5)
        ax.legend(loc="upper right" if key=="sand" else "lower right", frameon=True, facecolor="white", framealpha=0.92, edgecolor="#CBD5E1", fontsize=9.5)
        ax.grid(True, which="major", linestyle="-", color="#E2E8F0", linewidth=0.8)
        ax.grid(True, which="minor", linestyle=":", color="#F1F5F9", linewidth=0.6)
        
    axes[0].set_ylabel(r"$\mathbf{Decoupling\ Index}\ D = n_A / m_{\mathrm{VG}}\ \mathbf{[log\ scale]}$", fontweight="bold", fontsize=11.5)
    fig.tight_layout()
    
    out_file = FIG_DIR_05 / "panel_decoupling_index_vs_grain_size.png"
    fig.savefig(out_file, dpi=300)
    plt.close(fig)
    print(f" Saved: {out_file}")


# ==============================================================================
# 2. FIGURE FASE 05b: Universal Exponential Scaling vs Total Fines
# ==============================================================================
def generate_figure_05b():
    print("Generating Figure Fase 05b (Universal Exponential Scaling vs Fines)...")
    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    
    fines = np.array([d["fines"] for d in DATA])
    log_D = np.array([np.log10(d["D_EH"]) for d in DATA])
    
    res = linregress(fines, log_D)
    r, p = pearsonr(fines, log_D)
    
    # Fit line
    f_grid = np.linspace(0, 100, 150)
    d_fit = 10**(res.intercept + res.slope * f_grid)
    ax.plot(f_grid, d_fit, color="#1B9E77", linestyle="--", linewidth=2.4, zorder=3,
            label=rf"Exponential Law" + "\n" + rf"$D = 2.05 \cdot 10^{{0.0124 \cdot (\% \mathrm{{Fines}})}}$" + "\n" + rf"$r = +{r:.3f}\ (p = {p:.3f})$")
    
    # Plot points
    for d in DATA:
        ax.scatter(d["fines"], d["D_EH"], s=140, marker=d["marker"], facecolor=d["col"],
                   edgecolor="#222222", linewidth=1.2, zorder=5)
        
        # Point label placement
        if d["name"] == "Sand_R":
            ax.annotate("Sand_R", (d["fines"], d["D_EH"]), xytext=(d["fines"] + 2.0, d["D_EH"] * 0.95), fontsize=10.5, fontweight="bold", color="#1E293B")
        elif d["name"] == "ML7":
            ax.annotate("ML7", (d["fines"], d["D_EH"]), xytext=(d["fines"] - 4.5, d["D_EH"] * 1.16), fontsize=10.5, fontweight="bold", color="#1E293B")
        elif d["name"] == "ML4":
            ax.annotate("ML4", (d["fines"], d["D_EH"]), xytext=(d["fines"] - 2.5, d["D_EH"] * 1.18), fontsize=10.5, fontweight="bold", color="#1E293B")
        elif d["name"] == "ML1":
            ax.annotate("ML1", (d["fines"], d["D_EH"]), xytext=(d["fines"] - 7.5, d["D_EH"] * 0.95), fontsize=10.5, fontweight="bold", color="#1E293B")
        elif d["name"] == "ML9":
            ax.annotate("ML9", (d["fines"], d["D_EH"]), xytext=(d["fines"] - 2.0, d["D_EH"] * 1.15), fontsize=10.5, fontweight="bold", color="#1E293B")
        elif d["name"] == "ML8":
            ax.annotate("ML8", (d["fines"], d["D_EH"]), xytext=(d["fines"] + 2.2, d["D_EH"] * 0.88), fontsize=10.5, fontweight="bold", color="#1E293B")
        elif d["name"] == "ML10":
            ax.annotate("ML10", (d["fines"], d["D_EH"]), xytext=(d["fines"] + 2.2, d["D_EH"] * 1.02), fontsize=10.5, fontweight="bold", color="#1E293B")

    custom_y_ticks = [2, 3, 4, 5, 6, 10, 20, 30, 40, 50]
    custom_y_labels = [r"$2$", r"$3 \times 10^0$", r"$4 \times 10^0$", r"$5$", r"$6 \times 10^0$", r"$10$", r"$20$", r"$30$", r"$40$", r"$50$"]
    
    ax.set_yscale("log")
    ax.set_ylim(1.6, 55)
    ax.set_xlim(-6, 106)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_yticks(custom_y_ticks)
    ax.set_yticklabels(custom_y_labels)
    
    ax.set_xlabel(r"$\mathbf{Fines\ Fraction\ (Silt + Clay\ Content)\ [\%]}$", fontweight="bold", fontsize=11.5)
    ax.set_ylabel(r"$\mathbf{Decoupling\ Index}\ D = n_A / m_{\mathrm{VG}}\ \mathbf{[log\ scale]}$", fontweight="bold", fontsize=11.5)
    ax.set_title("Universal Exponential Scaling of Decoupling Index D vs. Soil Fines", fontsize=12.5, fontweight="bold", pad=12)
    
    ax.legend(loc="upper left", frameon=True, facecolor="white", framealpha=0.95, edgecolor="#CBD5E1", fontsize=10)
    ax.grid(True, which="major", linestyle="-", color="#E2E8F0", linewidth=0.8)
    ax.grid(True, which="minor", linestyle=":", color="#F1F5F9", linewidth=0.6)
    fig.tight_layout()
    
    out_file1 = FIG_DIR_05 / "panel_decoupling_index_vs_fines.png"
    out_file2 = FIG_DIR_05 / "plot_decoupling_index_vs_fines.png"
    fig.savefig(out_file1, dpi=300)
    fig.savefig(out_file2, dpi=300)
    plt.close(fig)
    print(f" Saved: {out_file1}")


# ==============================================================================
# 3. FIGURE FASE 06: Master USDA Ternary + 4 Outer Regimes + Slope Profile
# ==============================================================================
def generate_figure_06_master():
    print("Generating Figure Fase 06 Master (USDA Ternary + 4 Corner Regimes + Slope Profile)...")
    
    fig = plt.figure(figsize=(16.0, 9.5), facecolor="white")
    
    # 4 Regimes Data matching exact subplots from fase06.png
    # Top-Left: (b) ML7
    # Top-Right: (d) ML10
    # Bottom-Left: (a) Sand_R
    # Bottom-Right: (c) ML9
    
    cores_dict = {
        "ML7": {"title": r"$\mathbf{(b)\ Sandy\ Loam\ (ML7)}\ |\ n_A = 1.96$", "sub": r"$\mathit{Reduced\ GAP\ (Sand\ Mitigation\ Effect)}$", "alpha": 0.7566, "nVG": 1.244, "mVG": 0.1961, "nA": 1.96, "xlim": (1e-2, 1e3), "xticks": [1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3], "xticklabels": [r"$10^{-2}$", r"$10^{-1}$", r"$10^{0}$", r"$10^{1}$", r"$10^{2}$", r"$10^{3}$"]},
        "ML10": {"title": r"$\mathbf{(d)\ Silty\ Clay\ Loam\ (ML10)}\ |\ n_A = 3.63$", "sub": r"$\mathit{Buffered\ GAP\ (EDL\ Effect)}$", "alpha": 0.2356, "nVG": 1.159, "mVG": 0.1372, "nA": 3.63, "xlim": (1e-2, 1e3), "xticks": [1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3], "xticklabels": [r"$10^{-2}$", r"$10^{-1}$", r"$10^{0}$", r"$10^{1}$", r"$10^{2}$", r"$10^{3}$"]},
        "Sand_R": {"title": r"$\mathbf{(a)\ Clean\ Sand}\ |\ n_A = 1.84$", "sub": r"$\mathit{Minimal\ GAP\ (Synchronous\ Phase\ Transition)}$", "alpha": 0.1825, "nVG": 8.395, "mVG": 0.8809, "nA": 1.84, "xlim": (1e-2, 1e6), "xticks": [1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6], "xticklabels": [r"$10^{-2}$", r"$10^{-1}$", r"$10^{0}$", r"$10^{1}$", r"$10^{2}$", r"$10^{3}$", r"$10^{4}$", r"$10^{5}$", r"$10^{6}$"]},
        "ML9": {"title": r"$\mathbf{(c)\ Silt\ Loam\ (ML9)}\ |\ n_A = 4.38$", "sub": r"$\mathit{Maximum\ GAP\ (Silt\ Effect)}$", "alpha": 0.3732, "nVG": 1.138, "mVG": 0.1213, "nA": 4.38, "xlim": (1e-2, 1e3), "xticks": [1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3], "xticklabels": [r"$10^{-2}$", r"$10^{-1}$", r"$10^{0}$", r"$10^{1}$", r"$10^{2}$", r"$10^{3}$"]},
    }
    
    # Custom Axes Layout:
    # [left, bottom, width, height]
    rect_tl = [0.08, 0.58, 0.25, 0.30]  # (b) ML7
    rect_tr = [0.67, 0.58, 0.25, 0.30]  # (d) ML10
    rect_bl = [0.08, 0.10, 0.25, 0.30]  # (a) Sand_R
    rect_br = [0.67, 0.10, 0.25, 0.30]  # (c) ML9
    rect_center = [0.30, 0.23, 0.40, 0.65] # USDA Triangle
    rect_slope = [0.36, 0.03, 0.28, 0.17]  # Bottom Slope Profile
    
    def render_sub_trajectory(rect, sample_key):
        ax = fig.add_axes(rect)
        c = cores_dict[sample_key]
        
        h_grid = np.logspace(np.log10(c["xlim"][0]), np.log10(c["xlim"][1]), 500)
        alpha, nVG, mVG, nA = c["alpha"], c["nVG"], c["mVG"], c["nA"]
        
        Se = (1.0 + (alpha * h_grid)**nVG)**(-mVG)
        EC = (1.0 + (alpha * h_grid)**nVG)**(-mVG * nA)
        
        # Curves
        ax.plot(h_grid, Se, color="black", linewidth=2.0, label=r"$S_{\mathrm{eff}}\ \mathrm{(Retention)}$", zorder=4)
        ax.plot(h_grid, EC, color="black", linestyle="--", linewidth=2.0, label=rf"$EC_{{\mathrm{{eff}}}}\ (n_A = {nA:.2f})$", zorder=4)
        
        # Fill GAP area
        ax.fill_between(h_grid, EC, Se, where=(Se >= EC), color="#E2E8F0", alpha=0.9, label="GAP area", zorder=2)
        
        ax.set_xscale("log")
        ax.set_xlim(c["xlim"])
        ax.set_ylim(-0.02, 1.05)
        ax.set_xticks(c["xticks"])
        ax.set_xticklabels(c["xticklabels"], fontsize=8.5)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["0", "1"], fontsize=9.5, fontweight="bold")
        
        # Clean spines (minimalist publication style as in reference)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_linewidth(1.3)
        ax.spines["bottom"].set_linewidth(1.3)
        ax.grid(False) # No grid in reference
        
        # X-label 'h' at the bottom right
        ax.text(c["xlim"][1] * 0.8, -0.15, "h", fontsize=10, fontweight="bold", ha="center")
        
        # Title & Subtitle
        ax.set_title(f"{c['title']}\n{c['sub']}", fontsize=9.5, pad=6)
        
        # Legend (upper right)
        ax.legend(loc="upper right", frameon=False, fontsize=7.5, handlelength=1.8, labelspacing=0.3)
        return ax

    render_sub_trajectory(rect_tl, "ML7")
    render_sub_trajectory(rect_tr, "ML10")
    render_sub_trajectory(rect_bl, "Sand_R")
    render_sub_trajectory(rect_br, "ML9")
    
    # --------------------------------------------------------------------------
    # Center USDA Triangle
    # --------------------------------------------------------------------------
    ax_tri = fig.add_axes(rect_center)
    h_tri = np.sqrt(3) / 2
    
    # Equilateral triangle coordinates
    v_sand = np.array([0.0, 0.0])
    v_silt = np.array([1.0, 0.0])
    v_clay = np.array([0.5, h_tri])
    
    tri = plt.Polygon([v_sand, v_silt, v_clay], fill=False, edgecolor="black", linewidth=3.5, zorder=3)
    ax_tri.add_patch(tri)
    
    # Labels inside triangle exactly as in reference
    ax_tri.text(0.04, 0.05, "Sand_R", fontsize=16, fontweight="bold", color="black", zorder=5)
    ax_tri.text(0.40, 0.22, "ML7", fontsize=16, fontweight="bold", color="black", zorder=5)
    ax_tri.text(0.56, 0.30, "ML9", fontsize=16, fontweight="bold", color="black", zorder=5)
    ax_tri.text(0.61, 0.44, "ML10", fontsize=16, fontweight="bold", color="black", zorder=5)
    
    # Vertex labels
    ax_tri.text(0.5, h_tri + 0.05, "Clay", fontsize=18, fontweight="bold", color="black", ha="center")
    ax_tri.text(-0.02, -0.07, "Sand", fontsize=18, fontweight="bold", color="black", ha="center")
    ax_tri.text(1.02, -0.07, "Silt", fontsize=18, fontweight="bold", color="black", ha="center")
    
    ax_tri.set_xlim(-0.10, 1.10)
    ax_tri.set_ylim(-0.12, h_tri + 0.12)
    ax_tri.set_aspect("equal")
    ax_tri.axis("off")
    
    # --------------------------------------------------------------------------
    # Bottom Landslide Slope Profile
    # --------------------------------------------------------------------------
    ax_slope = fig.add_axes(rect_slope)
    
    # Load and smooth topography
    topo_csv = BASE_DIR / "data" / "raw" / "topography" / "profilo_sampling_point.csv"
    if topo_csv.exists():
        df_topo = pd.read_csv(topo_csv)
        x_raw = df_topo["distance"].to_numpy(dtype=float)
        z_raw = df_topo["quota_z"].to_numpy(dtype=float)
        window = min(25, len(z_raw) if len(z_raw) % 2 == 1 else len(z_raw) - 1)
        z_filt = savgol_filter(z_raw, window_length=window, polyorder=3)
        x_dense = np.linspace(float(x_raw[0]), float(x_raw[-1]), 300)
        z_dense = np.interp(x_dense, x_raw, z_filt)
    else:
        x_dense = np.linspace(0, 326, 300)
        z_dense = np.linspace(629, 581, 300)
        
    # Shaded Sectors
    ax_slope.axvspan(0, 45, color="#FEE2E2", alpha=0.7, zorder=1)      # Detachment (light red)
    ax_slope.axvspan(45, 75, color="#FFEDD5", alpha=0.7, zorder=1)     # Counterslope (light orange)
    ax_slope.axvspan(75, 112, color="#DCFCE7", alpha=0.7, zorder=1)    # Steep slope (light green)
    ax_slope.axvspan(112, 330, color="#E0F2FE", alpha=0.7, zorder=1)   # Outside (light blue)
    
    # Topo ground curve
    ax_slope.plot(x_dense, z_dense, color="#5A3D28", linewidth=2.2, zorder=3)
    ax_slope.fill_between(x_dense, 550, z_dense, color="#F1EBE4", alpha=0.6, zorder=2)
    
    # Sample points on slope
    slope_pts = [
        (10.0, 627.0, "ML9"),
        (36.0, 625.0, "ML7\nML8"),
        (72.0, 623.0, "ML5\nML6"),
        (93.0, 619.0, "ML3\nML4"),
        (108.0, 615.0, "ML1"),
        (317.0, 583.0, "ML10"),
    ]
    for px, py, pname in slope_pts:
        ax_slope.scatter(px, py, color="#555555", s=18, zorder=5)
        offset_y = 4.0 if pname == "ML10" else 2.5
        ax_slope.annotate(pname, (px, py), xytext=(px - 8 if px > 200 else px - 4, py + offset_y),
                          fontsize=6.5, fontweight="bold", color="#555555", zorder=6)
        
    ax_slope.set_xlim(-5, 330)
    ax_slope.set_ylim(570, 640)
    ax_slope.spines["top"].set_visible(True)
    ax_slope.spines["right"].set_visible(True)
    ax_slope.spines["left"].set_color("#CBD5E1")
    ax_slope.spines["bottom"].set_color("#CBD5E1")
    ax_slope.set_xticks([])
    ax_slope.set_yticks([])
    ax_slope.grid(True, linestyle="-", color="#CBD5E1", linewidth=0.6, alpha=0.6)
    
    out_file1 = FIG_DIR_06 / "master_panel_ternary_4_regimes_gap.png"
    out_file2 = FIG_DIR_05 / "plot_confronto_ipotesi_4_regimi.png"
    fig.savefig(out_file1, dpi=300, bbox_inches="tight")
    fig.savefig(out_file2, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f" Saved: {out_file1}")
    print(f" Saved: {out_file2}")


if __name__ == "__main__":
    generate_figure_05a()
    generate_figure_05b()
    generate_figure_06_master()
    print("All reference-matched figures generated successfully!")
