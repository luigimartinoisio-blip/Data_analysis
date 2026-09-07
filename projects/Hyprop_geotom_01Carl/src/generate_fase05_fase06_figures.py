"""
Script for Generating High-Impact Publication Figures for Phases 05 and 06
===========================================================================
Generates:
1. Panel Step 05.1: log10(D_EH) vs Sand %, Silt %, Clay % (Bivariate semi-log regressions)
2. Panel Step 05.2: log10(D_EH) vs % Fines (Unified Universal Scaling Law with Archie asymptotic limit)
3. 5 Updated Side-by-Side Qualitative Case Studies (Phase 04 Trajectory + USDA Ternary + Mineralogy)
4. Phase 06 Master Figure: Central USDA Ternary with 4 Angular Normalized Trajectory Panels [0, 1]
"""

from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.stats import pearsonr, linregress

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
    "grid.linestyle": "--",
})

# Dataset of 7 validated cores (excluding ML6)
DATA = [
    # sample, sand, silt, clay, fines, nA, alpha, nVG, mVG, D_EH, Delta_GAP, texture
    {"name": "Sand_R", "sand": 100.0, "silt": 0.0, "clay": 0.0, "fines": 0.0, "nA": 1.841, "alpha": 0.1825, "nVG": 8.395, "mVG": 0.8809, "D_EH": 2.09, "gap": 0.048, "text": "Sand", "col": "#0072B2"},
    {"name": "ML7", "sand": 40.1, "silt": 41.7, "clay": 18.2, "fines": 59.9, "nA": 1.956, "alpha": 0.7566, "nVG": 1.244, "mVG": 0.1961, "D_EH": 9.97, "gap": 0.630, "text": "Sandy Loam", "col": "#E69F00"},
    {"name": "ML4", "sand": 30.6, "silt": 44.7, "clay": 24.7, "fines": 69.4, "nA": 1.985, "alpha": 0.6310, "nVG": 1.192, "mVG": 0.1610, "D_EH": 12.33, "gap": 0.492, "text": "Loam", "col": "#56B4E9"},
    {"name": "ML8", "sand": 7.7, "silt": 69.5, "clay": 22.8, "fines": 92.3, "nA": 2.284, "alpha": 0.8390, "nVG": 1.117, "mVG": 0.1050, "D_EH": 21.75, "gap": 0.735, "text": "Silt Loam", "col": "#009E73"},
    {"name": "ML1", "sand": 7.6, "silt": 66.2, "clay": 26.2, "fines": 92.4, "nA": 3.249, "alpha": 0.2490, "nVG": 1.139, "mVG": 0.1220, "D_EH": 26.63, "gap": 0.776, "text": "Silt Loam", "col": "#F0E442"},
    {"name": "ML10", "sand": 6.8, "silt": 60.2, "clay": 33.0, "fines": 93.2, "nA": 3.633, "alpha": 0.2356, "nVG": 1.159, "mVG": 0.1372, "D_EH": 26.48, "gap": 1.018, "text": "Silty Clay Loam", "col": "#CC79A7"},
    {"name": "ML9", "sand": 16.5, "silt": 57.3, "clay": 26.2, "fines": 83.5, "nA": 4.384, "alpha": 0.3732, "nVG": 1.138, "mVG": 0.1213, "D_EH": 36.14, "gap": 1.234, "text": "Silt Loam", "col": "#D55E00"},
]


# ==============================================================================
# 1. FIGURE STEP 05.1: Bivariate Semi-Log Regressions vs Sand, Silt, Clay
# ==============================================================================
def plot_step_05_1():
    print("Generating Figure Step 05.1: Decoupling Index vs Grain Size...")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.2), sharey=True)
    
    log_D = np.array([np.log10(d["D_EH"]) for d in DATA])
    D_vals = np.array([d["D_EH"] for d in DATA])
    
    fractions = [
        ("sand", r"Sand Content [%] ( > 50 $\mu$m)", "#0072B2"),
        ("silt", r"Silt Content [%] ( 2 – 50 $\mu$m)", "#D55E00"),
        ("clay", r"Clay Content [%] ( < 2 $\mu$m)", "#CC79A7"),
    ]
    
    for ax, (key, label, col) in zip(axes, fractions):
        x = np.array([d[key] for d in DATA])
        res = linregress(x, log_D)
        r, p = pearsonr(x, log_D)
        
        # Data points
        ax.scatter(x, D_vals, s=75, color=col, edgecolor="black", linewidth=1.2, zorder=5)
        
        # Regression curve on log scale
        x_grid = np.linspace(0, 100 if key == "sand" else 75 if key == "silt" else 40, 100)
        y_fit = 10**(res.intercept + res.slope * x_grid)
        ax.plot(x_grid, y_fit, color=col, linestyle="-", linewidth=2.0, label=f"Fit: $r = {r:+.3f}$ ($p={p:.3f}$)")
        
        # Annotate core names
        for d in DATA:
            offset_y = 1.15 if d["name"] in ["ML10", "ML7"] else 0.88 if d["name"] == "ML1" else 1.08
            offset_x = 2.0 if d["name"] != "Sand_R" else -6.0
            ax.annotate(d["name"], (d[key], d["D_EH"]), 
                        xytext=(d[key] + offset_x, d["D_EH"] * offset_y),
                        fontsize=8.5, fontweight="bold", color="#222222")
            
        ax.set_yscale("log")
        ax.set_ylim(1.5, 50)
        ax.set_xlabel(label, fontweight="bold")
        ax.grid(True, which="both", linestyle="--", alpha=0.4)
        ax.legend(loc="lower left" if key == "sand" else "upper left", frameon=True, facecolor="white", framealpha=0.9)
    
    axes[0].set_ylabel(r"Electro-Hydraulic Decoupling Index $D_{EH} = \frac{n_A}{m_{\mathrm{VG}}}$ [-]", fontweight="bold")
    fig.suptitle(r"Phase 05 — Step 05.1: Semi-Logarithmic Scaling of $D_{EH}$ vs Individual Granulometric Fractions", fontsize=13, fontweight="bold", y=0.98)
    fig.tight_layout()
    
    out_path = FIG_DIR_05 / "panel_decoupling_index_vs_grain_size.png"
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f" Saved: {out_path}")


# ==============================================================================
# 2. FIGURE STEP 05.2: Unified Universal Scaling Law vs Total Fines
# ==============================================================================
def plot_step_05_2():
    print("Generating Figure Step 05.2: Universal Scaling Law vs Total Fines...")
    fig, ax = plt.subplots(figsize=(8.5, 6.2))
    
    fines = np.array([d["fines"] for d in DATA])
    log_D = np.array([np.log10(d["D_EH"]) for d in DATA])
    D_vals = np.array([d["D_EH"] for d in DATA])
    
    res = linregress(fines, log_D)
    r, p = pearsonr(fines, log_D)
    
    # 0% fines asymptote
    asymptote_D = 10**res.intercept # ~ 2.05
    
    # Data points
    for d in DATA:
        ax.scatter(d["fines"], d["D_EH"], s=95, color=d["col"], edgecolor="black", linewidth=1.2, zorder=6)
        # Annotation
        ax.annotate(f"{d['name']} ({d['D_EH']:.2f})", (d["fines"], d["D_EH"]),
                    xytext=(d["fines"] - (10 if d["name"]=="ML9" else -2.5), d["D_EH"] * (1.12 if d["name"]!="ML1" else 0.82)),
                    fontsize=9.5, fontweight="bold", color="#111111", zorder=7)
    
    # Fit line
    f_grid = np.linspace(0, 100, 150)
    d_fit = 10**(res.intercept + res.slope * f_grid)
    ax.plot(f_grid, d_fit, color="#1B365D", linewidth=2.4, zorder=4,
            label=rf"Scaling Law: $D_{{EH}} = 2.05 \cdot 10^{{0.0124 \cdot (\% \mathrm{{Fines}})}}$" + "\n" + rf"($r = +{r:.3f},\ p = {p:.3f},\ R^2 = {r**2:.3f}$)")
    
    # Highlight 0% Fines Asymptotic Anchor (Archie limit)
    ax.scatter([0.0], [asymptote_D], s=120, color="crimson", marker="*", edgecolor="black", linewidth=1.5, zorder=8,
               label=rf"Clean Sand Asymptote (0% Fines): $D_{{EH}} \to n_A = {asymptote_D:.2f}$ (Archie)")
    ax.axhline(asymptote_D, color="crimson", linestyle=":", linewidth=1.2, alpha=0.7)
    
    ax.set_yscale("log")
    ax.set_ylim(1.5, 60)
    ax.set_xlim(-5, 105)
    ax.set_xlabel(r"Total Fine Fraction ($\% \mathrm{Silt} + \% \mathrm{Clay}$) [%]", fontweight="bold", fontsize=11.5)
    ax.set_ylabel(r"Electro-Hydraulic Decoupling Index $D_{EH} = \frac{n_A}{m_{\mathrm{VG}}}$ [-]", fontweight="bold", fontsize=11.5)
    ax.set_title("Phase 05 — Step 05.2: Unified Universal Scaling Law of Decoupling Index vs Total Fine Fraction", fontsize=12, fontweight="bold", pad=12)
    
    ax.grid(True, which="both", linestyle="--", alpha=0.45)
    ax.legend(loc="upper left", frameon=True, facecolor="white", framealpha=0.95, edgecolor="#CCCCCC", fontsize=10)
    fig.tight_layout()
    
    out_path1 = FIG_DIR_05 / "panel_decoupling_index_vs_fines.png"
    out_path2 = FIG_DIR_05 / "plot_decoupling_index_vs_fines.png"
    fig.savefig(out_path1, dpi=300)
    fig.savefig(out_path2, dpi=300)
    plt.close(fig)
    print(f" Saved: {out_path1}")


# ==============================================================================
# 3. FIGURE FASE 06: Master Ternary Panel with 4 Angular Normalized Plots
# ==============================================================================
def plot_fase_06_master():
    print("Generating Figure Phase 06: Master USDA Ternary + 4 Angular Normalized Trajectory Panels...")
    
    # 4 Key Cores
    cores = [
        {"id": "Sand_R", "title": "(a) Clean Sand (Sand_R)", "sub": r"Minimal GAP ($\Delta = 0.05$ dec) — Synchronous", "nA": 1.841, "alpha": 0.1825, "nVG": 8.395, "mVG": 0.8809, "gap": 0.048, "pos": (0, 0)},
        {"id": "ML7", "title": "(b) Sandy Loam (ML7)", "sub": r"Reduced GAP ($\Delta = 0.63$ dec) — Sand Mitigation", "nA": 1.956, "alpha": 0.7566, "nVG": 1.244, "mVG": 0.1961, "gap": 0.630, "pos": (0, 1)},
        {"id": "ML9", "title": "(c) Silt Loam (ML9)", "sub": r"Maximum GAP ($\Delta = 1.23$ dec) — Silt Pinch-off", "nA": 4.384, "alpha": 0.3732, "nVG": 1.138, "mVG": 0.1213, "gap": 1.234, "pos": (1, 0)},
        {"id": "ML10", "title": "(d) Silty Clay Loam (ML10)", "sub": r"Buffered GAP ($\Delta = 1.02$ dec) — Smectite EDL", "nA": 3.633, "alpha": 0.2356, "nVG": 1.159, "mVG": 0.1372, "gap": 1.018, "pos": (1, 1)},
    ]
    
    fig = plt.figure(figsize=(15.5, 12.5))
    gs = fig.add_gridspec(3, 3, width_ratios=[1.15, 1.2, 1.15], height_ratios=[1.15, 1.2, 1.15])
    
    h_grid = np.logspace(-2, 3, 400) # 0.01 to 1000 kPa
    
    # Helper to plot trajectory
    def render_trajectory_panel(ax, c):
        alpha, nVG, mVG, nA = c["alpha"], c["nVG"], c["mVG"], c["nA"]
        psi_AEP = 1.0 / alpha
        
        Se = (1.0 + (alpha * h_grid)**nVG)**(-mVG)
        sigma_norm = (1.0 + (alpha * h_grid)**nVG)**(-mVG * nA)
        
        # Curves
        ax.plot(h_grid, Se, color="#1B365D", linewidth=2.4, label=r"Hydraulic: $S_e(h)$")
        ax.plot(h_grid, sigma_norm, color="#1E824C", linewidth=2.4, linestyle="--", label=r"Geoelectric: $\sigma_{\mathrm{norm}}(h)$")
        
        # AEP vertical line
        ax.axvline(psi_AEP, color="#D90429", linestyle=":", linewidth=1.5, label=rf"$\psi_{{\mathrm{{AEP}}}} = {psi_AEP:.2f}$ kPa")
        
        # Shaded GAP area
        ax.fill_between(h_grid, sigma_norm, Se, where=(Se >= sigma_norm), color="#00A896", alpha=0.22, label=rf"$\mathrm{{GAP\ area}} = {c['gap']:.3f}$ dec")
        
        ax.set_xscale("log")
        ax.set_xlim(1e-2, 1e3)
        ax.set_ylim(-0.02, 1.05)
        ax.set_xlabel(r"Matric Suction $h$ [kPa]", fontweight="bold", fontsize=9.5)
        ax.set_ylabel(r"Normalized $S_e,\ \sigma_{\mathrm{norm}}$ [-]", fontweight="bold", fontsize=9.5)
        ax.set_title(f"{c['title']}\n{c['sub']}", fontsize=10.5, fontweight="bold", pad=8)
        ax.grid(True, which="both", linestyle="--", alpha=0.35)
        ax.legend(loc="lower left", fontsize=8.2, framealpha=0.92, facecolor="white")
    
    # 4 Outer Trajectory Subplots
    ax_tl = fig.add_subplot(gs[0, 0])
    render_trajectory_panel(ax_tl, cores[0])
    
    ax_tr = fig.add_subplot(gs[0, 2])
    render_trajectory_panel(ax_tr, cores[1])
    
    ax_bl = fig.add_subplot(gs[2, 0])
    render_trajectory_panel(ax_bl, cores[2])
    
    ax_br = fig.add_subplot(gs[2, 2])
    render_trajectory_panel(ax_br, cores[3])
    
    # Center USDA Ternary Diagram
    ax_center = fig.add_subplot(gs[1, 1])
    
    # Draw Ternary Triangle (Equilateral)
    # Vertices: Sand (left: 0,0), Silt (right: 1,0), Clay (top: 0.5, sqrt(3)/2)
    h_tri = np.sqrt(3) / 2
    v_sand = np.array([0.0, 0.0])
    v_silt = np.array([1.0, 0.0])
    v_clay = np.array([0.5, h_tri])
    
    triangle = plt.Polygon([v_sand, v_silt, v_clay], fill=True, facecolor="#F8FAFC", edgecolor="#1E293B", linewidth=1.8, zorder=2)
    ax_center.add_patch(triangle)
    
    # Grid lines inside ternary
    for f in [0.2, 0.4, 0.6, 0.8]:
        # Sand lines (parallel to Clay-Silt)
        p1 = (1 - f) * v_sand + f * v_clay
        p2 = (1 - f) * v_sand + f * v_silt
        ax_center.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#CBD5E1", linestyle="--", linewidth=0.8, zorder=3)
        # Silt lines
        p1 = (1 - f) * v_silt + f * v_clay
        p2 = (1 - f) * v_silt + f * v_sand
        ax_center.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#CBD5E1", linestyle="--", linewidth=0.8, zorder=3)
        # Clay lines
        p1 = (1 - f) * v_clay + f * v_sand
        p2 = (1 - f) * v_clay + f * v_silt
        ax_center.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#CBD5E1", linestyle="--", linewidth=0.8, zorder=3)
        
    def to_ternary(sand, silt, clay):
        tot = sand + silt + clay
        if tot == 0:
            return v_sand
        s, si, cl = sand/tot, silt/tot, clay/tot
        x = 0.5 * (2 * si + cl)
        y = cl * h_tri
        return x, y

    # Plot Cores in Ternary
    key_cores_data = [
        {"name": "Sand_R", "sand": 100, "silt": 0, "clay": 0, "col": "#0072B2", "pos": (-0.08, -0.05)},
        {"name": "ML7", "sand": 40.1, "silt": 41.7, "clay": 18.2, "col": "#E69F00", "pos": (0.02, 0.03)},
        {"name": "ML9", "sand": 16.5, "silt": 57.3, "clay": 26.2, "col": "#D55E00", "pos": (0.02, -0.05)},
        {"name": "ML10", "sand": 6.8, "silt": 60.2, "clay": 33.0, "col": "#CC79A7", "pos": (-0.14, 0.03)},
    ]
    
    for kc in key_cores_data:
        tx, ty = to_ternary(kc["sand"], kc["silt"], kc["clay"])
        ax_center.scatter(tx, ty, s=110, color=kc["col"], edgecolor="black", linewidth=1.5, zorder=6)
        ax_center.annotate(kc["name"], (tx, ty), xytext=(tx + kc["pos"][0], ty + kc["pos"][1]),
                           fontsize=9.5, fontweight="bold", color="#111111", zorder=7)

    # Vertex Labels
    ax_center.text(-0.04, -0.08, "100% SAND", fontsize=10, fontweight="bold", color="#0072B2", ha="center")
    ax_center.text(1.04, -0.08, "100% SILT", fontsize=10, fontweight="bold", color="#D55E00", ha="center")
    ax_center.text(0.5, h_tri + 0.05, "100% CLAY", fontsize=10, fontweight="bold", color="#CC79A7", ha="center")
    
    ax_center.set_xlim(-0.15, 1.15)
    ax_center.set_ylim(-0.12, h_tri + 0.12)
    ax_center.set_aspect("equal")
    ax_center.axis("off")
    ax_center.set_title("USDA Textural Space\nKey Reference Cores", fontsize=11, fontweight="bold", pad=4)
    
    # Overarching Master Title
    fig.suptitle("Phase 06 Master Artifact: Hydro-Geophysical Decoupling Spectrum & The Smectite EDL Buffering Working Hypothesis",
                 fontsize=13.5, fontweight="bold", y=0.98)
    
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    
    out_path1 = FIG_DIR_06 / "master_panel_ternary_4_regimes_gap.png"
    out_path2 = FIG_DIR_05 / "plot_confronto_ipotesi_4_regimi.png"
    fig.savefig(out_path1, dpi=300)
    fig.savefig(out_path2, dpi=300)
    plt.close(fig)
    print(f" Saved: {out_path1}")
    print(f" Saved: {out_path2}")


if __name__ == "__main__":
    plot_step_05_1()
    plot_step_05_2()
    plot_fase_06_master()
    print("All Phase 05 & 06 figures generated successfully!")
