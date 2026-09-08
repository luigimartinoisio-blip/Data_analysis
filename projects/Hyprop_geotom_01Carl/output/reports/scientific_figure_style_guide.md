# Scientific Figure Style Guide & Design System
## High-Impact Visualization Standards for Integrated Hydrogeophysics

**Target Journals:** *Nature Geoscience*, *Water Resources Research*, *Geophysics*, *Vadose Zone Journal*  
**Workflow Scope:** Full Hydrogeophysical Analytical Pipeline (Phases 00 – 06)  
**Implementation Module:** `src/plot_style_config.py`  
**Version:** 1.0 (Final Publication Standard)

---

## 1. Executive Vision & Core Visual Philosophy

Scientific data visualization in top-tier earth science journals serves as both an analytical tool and the primary narrative vehicle for complex physical phenomena. In coupled hydrogeophysical research, where multiphase fluid mechanics (water retention $S_e(h)$) intersect non-linear solid-state electrical conduction ($\sigma(h)$) across heterogeneous pore networks, visual clarity is paramount.

This Design System enforces five non-negotiable principles:

```
                  ┌─────────────────────────────────────────────────────────┐
                  │          CORE VISUAL DESIGN SYSTEM PRINCIPLES           │
                  └─────────────────────────────────────────────────────────┘
                                               │
         ┌───────────────────┬─────────────────┴─────────────────┬───────────────────┐
         ▼                   ▼                                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐                 ┌─────────────────┐ ┌─────────────────┐
│ Visual Hierarchy│ │ Cognitive Load  │                 │    Semantic     │ │   Standalone    │
│ & Non-Redundancy│ │   Decluttering  │                 │ Color palettes  │ │ Interpretability│
├─────────────────┤ ├─────────────────┤                 ├─────────────────┤ ├─────────────────┤
│ • 2-Tier Header │ │ • Subtle Grids  │                 │ • Water (Blue)  │ │ • Explicit Units│
│ • Bold Titles   │ │ • No Overlap    │                 │ • EC (Charcoal) │ │ • Dual Metadata │
│ • Param Subtitle│ │ • Discrete Cards│                 │ • Archie (Green)│ │ • Physical Scale│
│ • No Redundancy │ │ • Inward Ticks  │                 │ • Boyd (Purple) │ │ • Defined Models│
└─────────────────┘ └─────────────────┘                 └─────────────────┘ └─────────────────┘
```

1. **Absolute Clarity & Visual Hierarchy**: A two-tier header system separates qualitative physical process definition (Title) from quantitative parametric context (Subtitle). Redundant text labels and duplicate axis tags are eliminated.
2. **Cognitive Load Reduction (Decluttering)**: Data points, model trajectories, confidence bounds, and asymptotic limits are visually separated using distinct line weights, stroke styles, and fills. Grids are rendered as subtle background guides (`alpha=0.7`, `:`, `color=#E5E5E5`).
3. **Semantic & Accessible Color Palettes**: Colors carry strict physical meaning across all phases. Palettes are colorblind-safe (Okabe-Ito, ColorBrewer 2.0) and maintain contrast in grayscale printing.
4. **Homogeneous Academic Typography**: Standardized font families, hierarchical type sizing, and strict bracket notation for physical units (e.g., $\psi\ [\text{kPa}]$, $\sigma_{\text{app}}\ [\text{mS/m}]$).
5. **Standalone Interpretability**: Every figure contains sufficient intrinsic context—via metadata cards, unit specifications, and parameter strings—to be fully comprehensible without reading the main manuscript text.

---

## 2. Scientific Figure Design System & Standards

### 2.1 Semantic Color Palette Specifications

The color palette establishes rigid chromatic mappings across all physical domains:

| Domain / Variable | Element Type | Color Name | HEX Code | RGB | Sample Usage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hydraulic Retention** | Line (Solid, 1.8pt) | Deep Navy | `#1B365D` | `(27, 54, 93)` | Primary $S_e(h)$ retention curve |
| **Hydraulic Retention** | Fill Area (Shading) | Water Soft Fill | `#E1EEF6` | `(225, 238, 246)` | Lower layer matrix zone / Retention band |
| **Hydraulic Threshold** | Line (Dashed, 1.2pt)| Deep Teal | `#028090` | `(2, 128, 144)` | Air Entry Point $\psi_{\text{AEP}} = 1/\alpha_{\text{VG}}$ |
| **Measured EC ($\sigma_{\text{obs}}$)** | Scatter Marker (`o`)| Dark Charcoal | `#222222` | `(34, 34, 34)` | Experimental quadripole data points |
| **Measured EC (Secondary)** | Scatter Marker (`^`)| Medium Slate | `#555555` | `(85, 85, 85)` | Secondary / Upper quadripole points |
| **EC Asymptotes** | Line (Dash-dot, 1.0pt)| Raw Amber | `#B35806` | `(179, 88, 6)` | $\sigma_{\text{sat}}$ and $\sigma_{\text{res}}$ bounds |
| **Coupled Archie-vG Fit** | Line (Solid, 2.0pt) | Forest Green | `#1E824C` | `(30, 130, 76)` | Coupled Archie $n_A$ inversion curve |
| **Coupled Archie Benchmark** | Line (Solid, 2.2pt) | Emerald Green | `#2CA02C` | `(44, 160, 44)` | Layer 4 (`qp5`) benchmark fit |
| **Boyd (2024) Empirical Fit**| Line (Solid, 1.8pt) | Royal Slate Purple| `#7570B3` | `(117, 112, 179)`| Boyd unconstrained fit curve |
| **Boyd Air Entry** | Line (Dashed, 1.2pt)| Rich Violet | `#8E44AD` | `(142, 68, 173)` | Geoelectrical Air Entry $\psi_{\text{EC}} = 1/\alpha_{\text{EC}}$ |
| **Tortuosity Gap ($\mathcal{A}_{\text{TG}}$)**| Fill Area (`alpha=0.22`)| Muted Teal Fill | `#00A896` | `(0, 168, 150)` | Integral area $[S_e - \text{EC}_{\text{norm}}]$ |
| **Regime 1: Canonical** | Badge / Indicator | Dark Forest Green | `#2E7D32` | `(46, 125, 50)` | Synchronous delay ($\Lambda_{\text{EC}} \le 1.50$) |
| **Regime 2: Transition** | Badge / Indicator | Warm Amber | `#E67E22` | `(230, 126, 34)` | L4 benchmark valid ($1.50 < \Lambda_{\text{EC}} \le 3.00$) |
| **Regime 3: EDL Dominance** | Badge / Indicator | Crimson Red | `#C0392B` | `(192, 57, 43)` | Smectite-delayed ($\Lambda_{\text{EC}} > 3.00$) |
| **Vector $\vec{V}_{\mathcal{K}}$** | Arrow & Annotation | Vermilion / Coral| `#D55E00` | `(213, 94, 0)` | Silt Polydispersity Gradient Vector |
| **Vector $\vec{V}_{\sigma_{res}}$**| Arrow & Annotation | Reddish Purple | `#CC79A7` | `(204, 121, 167)`| Clay / Smectite Conduction Vector |
| **Vector $\vec{V}_{\text{Archie}}$**| Star & Annotation | Deep Sapphire | `#0072B2` | `(0, 114, 178)` | Canonical Sand Anchor Pole |

### 2.2 Quadripole & Spatial Ring Palette

To track desaturation dynamics through the vertical profile of the HYPROP cell, geometric rings are color-coded:

- **Ring 1 / Layer 1 (Top, $z = 4.0$ cm, $0^\circ$)**: `#7F7F7F` (Medium Gray)
- **Ring 2 / Layer 2 (Upper, $z = 3.0$ cm, $0^\circ$)**: `#595959` (Slate Gray)
- **Ring 2 / Layer 2 (Upper, $z = 3.0$ cm, $90^\circ$)**: `#333333` (Charcoal)
- **Ring 3 / Layer 3 (Lower, $z = 2.0$ cm, $0^\circ$)**: `#CD5C5C` (Indian Red)
- **Ring 3 / Layer 3 (Lower, $z = 2.0$ cm, $90^\circ$)**: `#B22222` (Firebrick)
- **Ring 4 / Layer 4 (Basal Benchmark, $z = 1.0$ cm, $0^\circ$)**: `#800000` (Maroon / Burgundy)
- **Macro Upper Geometric Mean ($z = 3.5$ cm)**: `#A0522D` (Sienna)
- **Macro Lower Geometric Mean ($z = 1.5$ cm)**: `#8B0000` (Dark Red)

---

### 2.3 Typographic Hierarchy & Sizing Rules

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ Figure Super-Title: 13.0 pt Bold (#111111)                                             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ (a) Panel Title: 11.5 pt Bold                                                          │
│ Subtitle: [ML8 - Silty Clay Loam] | HYPROP: n=1.117, α=0.084 | Model: nA=3.63, K=9.55   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ Axis Title: 10.5 pt Semi-Bold (with explicit units [kPa], [mS/m])                      │
│ Axis Tick Labels: 9.0 pt Regular                                                       │
│ Legend Text: 8.5 pt Regular | Inset & Annotations: 8.0 pt                              │
│ Discrete Metadata Cards: 8.0 pt Monospace/Sans-serif                                   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

| Element | Font Size | Weight | Font Style | Color | Matplotlib Placement |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Figure Super-Title** | 13.0 pt | Bold | Normal | `#111111` | `fig.suptitle(..., y=0.98)` |
| **Panel Main Title** | 11.5 pt | Bold | Normal | `#222222` | `ax.set_title(..., pad=16)` |
| **Informative Subtitle**| 9.5 pt | Regular | Italic/Muted | `#444444` | `ax.text(0.5, 1.03, ...)` |
| **Panel Identifier** | 12.0 pt | Bold | Normal | `#111111` | `(a)`, `(b)` at `(-0.10, 1.05)` |
| **Axis Title ($X, Y$)** | 10.5 pt | Semi-bold| Normal | `#222222` | `ax.set_xlabel('... [unit]')` |
| **Tick Labels** | 9.0 pt | Regular | Normal | `#2B2B2B` | `ax.tick_params(labelsize=9.0)` |
| **Legend Text** | 8.5 pt | Regular | Normal | `#222222` | `ax.legend(fontsize=8.5)` |
| **Metadata Cards** | 8.0 pt | Regular | Clean Monospace| `#222222` | `add_texture_mineralogy_box` |
| **Subscripts / Details**| 7.0 pt | Regular | Normal | `#555555` | Secondary callouts |

---

### 2.4 Figure Dimensions, Grid Alignment & Export DPI

Standard dimensions conform to print layout constraints of major scientific publishers:

- **Single Column (1-col)**: Width = **3.54 in (90 mm)**; Aspect ratio 1.33:1 or 1.4:1 (Height = 2.6 – 3.2 in).
- **Intermediate Column (1.5-col)**: Width = **5.51 in (140 mm)**; Height = 3.8 – 4.5 in.
- **Double Column (2-col)**: Width = **7.48 in (190 mm)**; Height = 4.2 – 5.5 in.
- **Full Page / Master Multi-Panel**: Width = **11.50 – 12.50 in**; Height = 7.5 – 8.5 in.
- **Export Resolution**: **300+ DPI** minimum for raster (`.png`, `.tiff`); vector formats (`.pdf`, `.svg`) must preserve editable text paths (`mpl.rcParams['pdf.fonttype'] = 42`).
- **Margin Engine**: `constrained_layout=True` with `pad_inches=0.04` to avoid label clipping.

---

### 2.5 Standard Two-Tier Header Convention

To eliminate floating annotation clutter in the plot area, figures must implement the Two-Tier Header:

```
[Tier 1 - Main Title]:     ML8 (Silty Clay Loam) — Desaturation & Geoelectrical Inversion
[Tier 2 - Subtitle]:       HYPROP: n_VG=1.117, α_VG=0.084 kPa⁻¹, ψ_AEP=11.9 kPa | Model: n_A=3.63, K=9.55, R²=0.988
```

#### Structural Formula:
1. **Tier 1 (Main Title)**: `[Sample ID] ([USDA Texture]) — [Physical Investigation]`
2. **Tier 2 (Informative Subtitle)**: `HYPROP: n_VG=[val], α_VG=[val] kPa⁻¹, ψ_AEP=[val] kPa | Model: n_A=[val], K(n_VG)=[val], Λ_EC=[val], R²=[val]`

---

### 2.6 Standard Metadata Box & Parameter Cards

Metadata cards present essential sample petrophysics in a standardized, discrete box:

```
┌────────────────────────────────────────────────────────┐
│ Textural Breakdown:                                    │
│   • Sand: 12.4% | Silt: 58.2% | Clay: 29.4%            │
│   • USDA Class: Silty Clay Loam                        │
│ Mineralogy & Charge:                                   │
│   • Phyllosilicates: 44.5%                             │
│   • Clay Composition: 42% I/S, 18% Kaolinite           │
│   • Qv = 0.38 meq/cm³ | CEC = 14.8 meq/100g            │
└────────────────────────────────────────────────────────┘
```
- **Styling**: `boxstyle="round,pad=0.4,rounding_size=0.25"`, `facecolor="#FFFFFF"`, `edgecolor="#CCCCCC"`, `alpha=0.92`, `linewidth=0.8`.
- **Default Position**: `loc='lower left'` for desaturation curves (where data descends towards lower right).

---

## 3. Graphical Architecture Across Workflow Phases (00 – 06)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   HYDROGEOPHYSICAL WORKFLOW PIPELINE                                    │
├───────────────────┬───────────────────┬───────────────────┬───────────────────┬─────────────────────────┤
│     Phase 00      │   Phase 01 & 02   │     Phase 03      │     Phase 04      │      Phase 05 & 06      │
├───────────────────┼───────────────────┼───────────────────┼───────────────────┼─────────────────────────┤
│ Lower Benchmark   │ Physical Space    │ Normalized Space  │ Master Panels     │ Theory & Textural       │
│ Validation        │ Empirical & Model │ [0,1] & Screening │ Suitable Benchmark│ Correlations            │
│ • Monotonicity    │ • Boyd (2024)     │ • Se vs EC_norm   │ • Clean Curves    │ • K(n_VG) Trajectory    │
│ • Reciprocity     │ • Archie Inversion│ • Tortuosity Gap  │ • 5 Samples L4    │ • USDA Ternary Vectors  │
│ • Depth Gradient  │ • Ring Comparison │ • Anisotropy Inset│ • Dual Metadata   │ • 95% CI Scatter Plots  │
└───────────────────┴───────────────────┴───────────────────┴───────────────────┴─────────────────────────┘
```

---

### 3.1 Phase 00: Benchmark Validation of Lower Layers (L3 – L4)

**Scientific Objective:** Demonstrate that lower rings (Layer 3 at $z=2$ cm and Layer 4 at $z=1$ cm, specifically `qp4`, `qp5`, `qp6`, `geom_lower`) represent the undisturbed soil matrix, isolated from top boundary evaporative micro-cracking and contact noise.

```
┌──────────────────────────────────────────────┬──────────────────────────────────────────────┐
│ (a) Monotonicity Correlation |ρ_s| vs Depth z │ (b) Reciprocity Error ε_recip across Layers  │
├──────────────────────────────────────────────┼──────────────────────────────────────────────┤
│ 1.00 ────────┬────────────[Benchmark: 0.95]──│ 10.0 % ───[Upper Ring Instability: ε > 5%]── │
│      Lower Matrix (L3-L4)  │   Upper (L1-L2) │                                              │
│ 0.90       ●      ●        │                 │  1.0 % ───[Lower Matrix Fidelity: ε < 1%]─── │
│ 0.80                       │        ▲        │                                              │
│ 0.70                       │                 │  0.1 %                                       │
│    0.0    1.0    2.0      3.0    4.0    5.0  │         L4 (qp5)   L3 (qp4)   L2 (qp2)   L1  │
│              Depth z [cm]                    │                   Quadripole Layer           │
└──────────────────────────────────────────────┴──────────────────────────────────────────────┘
```

#### Graphical Specifications:
1. **Layout**: 2-panel horizontal grid (`figsize=(7.48, 3.8)` inches).
2. **Panel (a) — Monotonicity vs Depth**:
   - $X$-axis: Depth below evaporating surface $z$ [cm] (0.0 to 5.0 cm).
   - $Y$-axis: Spearman rank correlation $|\rho_s(\psi)|$ and $|\rho_s(S_r)|$ (0.70 to 1.02).
   - Visual Zones: Shaded blue background (`#E1EEF6`, `alpha=0.35`) for Lower Matrix ($z = 0.5 - 2.5$ cm); Shaded peach background (`#FDF2E9`, `alpha=0.35`) for Evaporating Boundary ($z = 2.5 - 4.5$ cm).
   - Threshold: Horizontal dashed line at $|\rho_s| = 0.95$ (`#2E7D32`).
3. **Panel (b) — Reciprocity Error Distribution**:
   - $X$-axis: Quadripole Category / Layer ordered from Basal L4 to Top L1.
   - $Y$-axis: Mean Reciprocity Error $\varepsilon_{\text{recip}}$ [%] on **logarithmic scale** ($0.05\%$ to $50\%$).
   - Quality Threshold: Horizontal dotted line at $\varepsilon = 5.0\%$ (`#C0392B`).

---

### 3.2 Phase 01: Boyd et al. (2024) Empirical Formulation

**Scientific Objective:** Fit unconstrained apparent conductivity $\sigma(h)$ across matric suction to estimate geoelectrical air entry $\psi_{\text{EC}} = 1/\alpha_{\text{EC}}$ and slope exponent $n_{\text{EC}}$.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ (a) Boyd et al. (2024) Empirical Formulation — ML8 (Silty Clay Loam)                        │
│ Subtitle: Boyd: α_EC = 0.080 kPa⁻¹, ψ_EC = 12.5 kPa, n_EC = 1.082 | R² = 0.989              │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│   σ [mS/m]                                                                                  │
│     100 ┌───[Asymptotic Upper Bound: σ_sat = 95.4 mS/m]──────────────────────────┐          │
│         │ ○  ○                                                                   │          │
│         │       ○  ○  • Boyd Fit Curve (Solid Slate Purple, #7570B3)             │          │
│      10 │                ○                                                       │          │
│         │                   ○  ○                                                 │          │
│         │      [Geoelectrical Air Entry: ψ_EC = 12.5 kPa]                        │          │
│       1 └───[Asymptotic Lower Bound: σ_res = 1.2 mS/m]───────────────────────────┘          │
│       0.1                       1.0                      10.0                   100.0       │
│                                       Matric Suction ψ [kPa]                                │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Graphical Specifications:
1. **Layout**: Single panel (`figsize=(5.51, 4.0)`) or multi-panel 2x2.
2. **Coordinate Space**: Semi-log ($X$ logarithmic $\psi \in [0.08, 1500]$ kPa; $Y$ linear or log $\sigma \in [\sigma_{\text{res}}, \sigma_{\text{sat}}]$ mS/m).
3. **Data Elements**:
   - Observed Data: Dark charcoal points (`#222222`, `facecolor="#F0F0F0"`, `markersize=5.5`).
   - Boyd Fit Curve: Solid Slate Purple line (`#7570B3`, `linewidth=2.0`).
   - Asymptotic Bands: Dash-dot lines (`#B35806` for $\sigma_{\text{sat}}$, `#7F3B08` for $\sigma_{\text{res}}$).
   - Geoelectrical Air Entry: Vertical dashed line at $\psi_{\text{EC}} = 1/\alpha_{\text{EC}}$ (`#8E44AD`, `linewidth=1.2`).

---

### 3.3 Phase 02: Coupled van Genuchten – Archie – Waxman-Smits Inversion

**Scientific Objective:** Lock hydraulic parameters $(\alpha_{\text{VG}}, n_{\text{VG}}, m_{\text{VG}})$ from HYPROP2 and perform single-degree-of-freedom inversion of apparent saturation exponent $n_A$.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ (a) Coupled van Genuchten–Archie Inversion across Vertical Profile — ML8                   │
│ Subtitle: HYPROP: n_VG=1.117, α_VG=0.084 kPa⁻¹ | Archie Fit: n_A=3.63, R²=0.988            │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│   σ [mS/m]                                                                                  │
│     100 ┌───● L4 (qp5, z=1.0 cm) — Coupled Fit (Solid Emerald Green, #2CA02C)────┐          │
│         │   ■ L3 (qp4, z=2.0 cm) — Lower Matrix Fit                              │          │
│         │   ▲ L2 (qp2, z=3.0 cm) — Cortical Evaporative Detachment               │          │
│      10 │   ▼ L1 (qp1, z=4.0 cm) — Upper Surface Cracking Deviation              │          │
│         │                                                                        │          │
│         │   [Locked Hydraulic Air Entry: ψ_AEP = 11.9 kPa]                       │          │
│       1 └────────────────────────────────────────────────────────────────────────┘          │
│       0.1                       1.0                      10.0                   100.0       │
│                                       Matric Suction ψ [kPa]                                │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Graphical Specifications:
1. **Layout**: Double column (`figsize=(7.48, 4.5)` inches).
2. **Coordinate Space**: Semi-log ($X$ logarithmic $\psi \in [0.08, 1500]$ kPa; $Y$ linear $\sigma$ mS/m).
3. **Data Elements**:
   - Quadripoles colored strictly according to Layer Palette (`qp5` Maroon `#800000`, `qp4` Indian Red `#CD5C5C`, `qp2` Slate `#595959`, `qp1` Gray `#7F7F7F`).
   - Coupled Inversion Fit: Solid Forest/Emerald Green curve (`#1E824C`, `linewidth=2.2`).
   - Hydraulic Air Entry Anchor: Vertical dotted line at $\psi_{\text{AEP}} = 1/\alpha_{\text{VG}}$ (`#028090`).

---

### 3.4 Phase 03: Normalized Comparison [0, 1], Screening & Anisotropy

**Scientific Objective:** Compare normalized hydraulic retention $S_e(h)$ directly against normalized electrical conductivity $\text{EC}_{\text{norm}}(h)$, quantify the Tortuosity Gap $\Delta(h)$, and classify plateau desynchronization via $\Lambda_{\text{EC}} = \psi_{\text{EC}} / \psi_{\text{AEP}}$.

```
┌──────────────────────────────────────────────┬──────────────────────────────────────────────┐
│ (a) Normalized Hydrogeophysical Response     │ (b) Tortuosity Gap Residuals & Anisotropy    │
├──────────────────────────────────────────────┼──────────────────────────────────────────────┤
│ 1.0 ┌──Se(h) Hydraulic Retention (Navy Blue) ─│ 0.6 ┌──Δ(h) = Se - EC_norm (Muted Teal Fill)─┐│
│     │ ──EC_norm Archie Fit (Emerald Green)   │     │                                        ││
│ 0.8 │ ──EC_norm Boyd Fit (Slate Purple)      │ 0.4 │           ┌──────────────────────┐     ││
│     │ ●  EC_norm Observed Data (Charcoal)    │     │           │ Inset: Anisotropy    │     ││
│ 0.6 │                                        │ 0.2 │           │ λ = ρ_90° / ρ_0°     │     ││
│     │                                        │     │           └──────────────────────┘     ││
│ 0.4 │                                        │ 0.0 └───[Baseline: Δ = 0]────────────────────┘│
│ 0.2 │                                        │-0.2                                          │
│ 0.0 └────────────────────────────────────────┘     0.1        1.0        10.0      100.0    │
│     0.1        1.0        10.0      100.0    │                 Matric Suction ψ [kPa]       │
│              Matric Suction ψ [kPa]          │                                              │
└──────────────────────────────────────────────┴──────────────────────────────────────────────┘
```

#### Graphical Specifications:
1. **Layout**: Dual-Panel with Inset (`figsize=(7.48, 4.6)` inches, `gridspec_kw={"width_ratios": [1.15, 1.0]}`).
2. **Panel (a) — Normalized Response $[0, 1]$**:
   - $X$-axis: $\psi$ [kPa] logarithmic; $Y$-axis: Normalized Response $[0, 1]$.
   - Curves: Hydraulic $S_e(h)$ (`#1B365D`, 2.0pt), Archie Fit (`#1E824C`, 1.8pt), Boyd Fit (`#7570B3`, 1.8pt), Observed Data points (`#222222`).
3. **Panel (b) — Tortuosity Gap Residuals**:
   - $X$-axis: $\psi$ [kPa] logarithmic; $Y$-axis: $\Delta(h) = S_e(h) - \text{EC}_{\text{norm}}(h)$.
   - Area Shading: Muted Teal fill (`#00A896`, `alpha=0.25`) between residual curve and $\Delta=0$ baseline.
4. **Diagnostic Inset (Inside Panel b, Top Right)**:
   - Position: `ax_b.inset_axes([0.48, 0.52, 0.48, 0.44])`.
   - Content: Azimuthal anisotropy ratio $\lambda(h) = \rho_{90^\circ}(h) / \rho_{0^\circ}(h)$ across suction, with horizontal reference at $\lambda=1.0$.
   - Plateau Regime Badge: Colored tag indicating Regime 1 (Green), Regime 2 (Amber), or Regime 3 (Crimson).

---

### 3.5 Phase 04: Master Panels of Suitable Samples (Benchmark L4)

**Scientific Objective:** High-impact comparative dashboard presenting pure theoretical curves (without noisy data points) for the five suitable samples (`Sand_R`, `ML8`, `ML9`, `ML1`, `ML7`), ordered strictly by the Pore Geometry Amplification Factor $\mathcal{K}$.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ MASTER BENCHMARK (LAYER 4 / qp5) — COUPLED HYDROGEOPHYSICAL RETENTION & CONDUCTION          │
├──────────────────────────────┬──────────────────────────────┬───────────────────────────────┤
│ (a) Sand_R (Uniform Sand)    │ (b) ML8 (Silty Clay Loam)    │ (c) ML9 (Silt Loam)           │
│ Subtitle: K=1.14, nA=1.95    │ Subtitle: K=9.55, nA=3.63    │ Subtitle: K=8.25, nA=3.12     │
│ ┌──────────────────────────┐ │ ┌──────────────────────────┐ │ ┌───────────────────────────┐ │
│ │ ── Se(h) Hydraulic       │ │ │ ── Se(h) Hydraulic       │ │ │ ── Se(h) Hydraulic        │ │
│ │ ── EC_norm Coupled Archie│ │ │ ── EC_norm Coupled Archie│ │ │ ── EC_norm Coupled Archie │ │
│ │ ┌──────────────────────┐ │ │ │ ┌──────────────────────┐ │ │ │ ┌───────────────────────┐ │ │
│ │ │ Texture: Sa 92%      │ │ │ │ │ Texture: Si 58%      │ │ │ │ │ Texture: Si 62%       │ │ │
│ │ │ Phyllo: 3.2%         │ │ │ │ │ Phyllo: 44.5%        │ │ │ │ │ Phyllo: 38.1%         │ │ │
│ │ └──────────────────────┘ │ │ │ └──────────────────────┘ │ │ │ └───────────────────────┘ │ │
│ └──────────────────────────┘ │ └──────────────────────────┘ │ └───────────────────────────┘ │
├──────────────────────────────┴──────────────────────────────┴───────────────────────────────┤
│ (d) ML1 (Loam)               │ (e) ML7 (Sandy Loam)         │ (f) Textural Spectrum Summary │
│ Subtitle: K=9.01, nA=2.85    │ Subtitle: K=5.21, nA=2.14    │ Subtitle: K vs Textural Fines │
└──────────────────────────────┴──────────────────────────────┴───────────────────────────────┘
```

#### Graphical Specifications:
1. **Layout**: 2x3 Subplot Grid (`figsize=(11.50, 7.5)` inches).
2. **Curve Rendering**: Pure, smooth theoretical lines (no markers). Hydraulic $S_e(h)$ in Navy Blue (`#1B365D`, 2.2pt); Coupled Archie $\text{EC}_{\text{norm}}(h)$ in Emerald Green (`#2CA02C`, 2.2pt).
3. **Tortuosity Gap Shading**: Subtle teal area fill between $S_e(h)$ and $\text{EC}_{\text{norm}}(h)$ (`#00A896`, `alpha=0.18`).
4. **Metadata Annotation**: Every subplot features the standard dual-block Textural & Mineralogical Card pinned to `loc='lower left'`.

---

### 3.6 Phase 05: Pore Geometry Factor $\mathcal{K}(n_{\text{VG}})$ & Tortuosity Gap Area $\mathcal{A}_{\text{TG}}$

**Scientific Objective:** Visualize the non-linear hyperbolic divergence $\mathcal{K}(n_{\text{VG}}) = n_{\text{VG}} / (n_{\text{VG}} - 1) = 1/m_{\text{VG}}$ and its direct mathematical link to the integrated Tortuosity Gap Area $\mathcal{A}_{\text{TG}} = \int [S_e - \text{EC}_{\text{norm}}] d(\log_{10} h)$.

```
┌──────────────────────────────────────────────┬──────────────────────────────────────────────┐
│ (a) Analytical Trajectory of Factor K(n_VG)  │ (b) Tortuosity Gap Area Integration (A_TG)   │
├──────────────────────────────────────────────┼──────────────────────────────────────────────┤
│ 12 ┌── Hyperbolic Divergence: K = n/(n-1) ──┐ │ 1.0 ┌── Se(log h) Hydraulic Retention ───────┐│
│ 10 │    ● ML8 (K=9.55, n=1.117)             │     │   █████████████████████████          ││
│  8 │    ● ML1 (K=9.01, n=1.125)             │ 0.8 │   ██ Tortuosity Gap Area ██          ││
│  6 │    ● ML9 (K=8.25, n=1.138)             │     │   ██ A_TG = ∫[Se - EC] d(log h)      ││
│  4 │         ● ML7 (K=5.21, n=1.237)        │ 0.6 │   █████████████████████████          ││
│  2 │              [Monodisperse Limit: K→1] │     │ ── EC_norm(log h) Coupled Archie     ││
│  0 └───────────────────────★ Sand_R (K=1.14)┘ │ 0.0 └────────────────────────────────────────┘│
│   1.0   1.5   2.0   2.5   3.0   3.5   4.0   │    -1.0        0.0        1.0        2.0    │
│            van Genuchten Exponent n_VG       │                 log10(Suction [kPa])         │
└──────────────────────────────────────────────┴──────────────────────────────────────────────┘
```

#### Graphical Specifications:
1. **Layout**: 2-Panel horizontal grid (`figsize=(7.48, 4.2)` inches).
2. **Panel (a) — Analytical Trajectory $\mathcal{K}(n_{\text{VG}})$**:
   - Continuous theoretical curve: Solid Navy line (`#1B365D`, 2.0pt) over $n_{\text{VG}} \in (1.02, 5.0]$.
   - Experimental samples plotted as labeled points with distinct colors according to texture.
   - Asymptote callout: $n_{\text{VG}} \to 1 \implies \mathcal{K} \to \infty$ (Polydisperse fine-grained soils).
3. **Panel (b) — Area Integration $\mathcal{A}_{\text{TG}}$**:
   - $X$-axis: $\log_{10}(\psi\ [\text{kPa}])$ linear scale $(-1.0$ to $3.0$).
   - Integration Zone: Distinct hatched teal area fill (`#00A896`, `alpha=0.28`, `hatch='//'`) between $S_e$ and $\text{EC}_{\text{norm}}$.
   - Integrated Value Callout: Text box reporting exact numerical area $\mathcal{A}_{\text{TG}} = 0.842\ \text{decades}$.

---

### 3.7 Phase 06: USDA Textural Ternary Diagram & Bivariate Regressions

**Scientific Objective:** High-resolution ternary mapping of soils combined with the three governing physical vectors, paired with bivariate cross-correlations ($95\%$ confidence intervals) linking $\mathcal{K}$ to silt content and soil charge.

```
┌──────────────────────────────────────────────┬──────────────────────────────────────────────┐
│ (a) USDA Ternary & Governing Physical Vectors│ (b) Bivariate Correlation: Factor K vs Silt %│
├──────────────────────────────────────────────┼──────────────────────────────────────────────┤
│                   Clay (100%)                │  12 ┌── Pearson r = +0.944 (p = 0.0047) ─────┐│
│                       /\                     │  10 │   Spearman ρ = +0.900 (p = 0.0160)     ││
│                      /  \                    │     │                   ● ML8                ││
│   Vector EC_res     /    \                   │   8 │             ● ML1                      ││
│   (Smectite Conduc)/      \                  │     │             ● ML9                      ││
│   [Red-Purple]    /   ●ML5 \                 │   6 │                                        ││
│                  /          \                │     │       ● ML7                            ││
│                 /    ●ML8    \               │   4 │                                        ││
│                /              \              │   2 │                                        ││
│  Vector K ───>/────────────────\             │     │ ● Sand_R  [95% CI Shaded Band]         ││
│  [Vermilion] /  ●ML7      ●ML9  \            │   0 └────────────────────────────────────────┘│
│  Sand (100%) ★──────────────────── Silt(100%)│     0        20        40        60        80 │
│             P_Archie (Deep Blue)             │                    Silt Fraction [%]         │
└──────────────────────────────────────────────┴──────────────────────────────────────────────┘
```

#### Graphical Specifications:
1. **Layout**: Dual-panel (`figsize=(7.48, 4.6)` inches, `gridspec_kw={"width_ratios": [1.1, 1.0]}`).
2. **Panel (a) — USDA Ternary Diagram**:
   - Equilateral triangle geometry with internal $20\%$ gridlines (`#E0E0E0`, `:`).
   - **Vector $\vec{V}_{\mathcal{K}}$ (Silt-Driven Amplification)**: Vermilion arrow (`#D55E00`, 2.2pt) from Sand apex along the base toward Silt apex ($r = +0.944$).
   - **Vector $\vec{V}_{\sigma_{res}}$ (Smectite Surface Conduction)**: Reddish purple arrow (`#CC79A7`, 2.2pt) pointing toward Clay apex.
   - **Pole $\mathbf{P}_{\text{Archie}}$ (Canonical Sand Pole)**: Large deep blue star (`#0072B2`, 14pt) at Sand apex ($n_A \approx 1.95, \mathcal{K} \approx 1.14$).
3. **Panel (b) — Bivariate Correlation ($\mathcal{K}$ vs Silt %)**:
   - $X$-axis: Silt Fraction [\%] (0 to 80\%); $Y$-axis: Amplification Factor $\mathcal{K}$ (0 to 12).
   - Regression Line: OLS fit line in solid Vermilion (`#D55E00`, 2.0pt).
   - $95\%$ Confidence Interval: Shaded band (`#FADBD8`, `alpha=0.45`).
   - Statistical Badge: Inset box with Pearson $r$, Spearman $\rho$, and exact $p$-values.

---

## 4. Python Implementation: `src/plot_style_config.py`

The complete styling engine and helper architecture are implemented in `src/plot_style_config.py`.

### 4.1 Module Import & Quick Start

```python
import matplotlib.pyplot as plt
import numpy as np
from src.plot_style_config import (
    set_publication_style,
    create_figure,
    set_hierarchical_header,
    add_panel_label,
    add_texture_mineralogy_box,
    PALETTES,
    FONT_SIZES
)

# 1. Initialize publication style
set_publication_style(font_family="sans-serif")

# 2. Create standardized double-column figure
fig, ax = create_figure(width_type="double_col", height=4.5)

# 3. Apply two-tier hierarchical header
set_hierarchical_header(
    ax,
    title="ML8 (Silty Clay Loam) — Desaturation & Geoelectrical Inversion",
    sample_id="ML8",
    texture="Silty Clay Loam",
    hydraulic_params={"n_vg": 1.117, "alpha_vg": 0.084, "psi_aep": 11.9},
    model_params={"n_a": 3.63, "k_factor": 9.55, "r2": 0.988}
)

# 4. Add standardized panel identifier
add_panel_label(ax, label="a")

# 5. Add discrete metadata card
sample_meta = {
    "sand": 12.4, "silt": 58.2, "clay": 29.4, "usda_class": "Silty Clay Loam",
    "phyllo": 44.5, "is_smectite": 42.0, "kaol": 18.0, "qv": 0.38, "cec": 14.8
}
add_texture_mineralogy_box(ax, sample_meta, loc="lower left")

plt.show()
```

---

## 5. Checklist for Journal Submission Quality Control

Before submitting figures to *Nature Geoscience*, *Water Resources Research*, or *Geophysics*, verify every figure against this checklist:

- [ ] **Resolution**: Raster files exported at $\ge 300\ \text{DPI}$; vector formats contain true text objects (not outlined curves).
- [ ] **Dimensions**: Figure width strictly matches $3.54\ \text{in}$ (1-col), $5.51\ \text{in}$ (1.5-col), or $7.48\ \text{in}$ (2-col).
- [ ] **Two-Tier Header**: Qualitative physical process in Title; quantitative parameters in Subtitle.
- [ ] **No Overlapping Text**: All metadata cards, legends, and axis labels have at least $0.05\ \text{in}$ clearance from data lines.
- [ ] **Explicit Units**: Every physical axis includes bracketed units (e.g., $\psi\ [\text{kPa}]$, $\sigma_{\text{app}}\ [\text{mS/m}]$, $\theta\ [\text{Vol\%}]$).
- [ ] **Color Accessibility**: Primary curves distinguishable in grayscale and by colorblind individuals (Navy vs Green vs Purple vs Orange).
- [ ] **Subtle Grid**: Grids set to `:` dotted lines, `#E5E5E5`, `alpha=0.7`, placed strictly below data elements (`axisbelow=True`).
- [ ] **Inward Ticks**: Major and minor tick marks point inward (`tick.direction='in'`) with top and right spines enabled.
