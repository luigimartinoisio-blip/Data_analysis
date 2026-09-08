# SPECIALIST REPORT 06: QUALITATIVE WORKING HYPOTHESIS AND FUTURE RESEARCH BLUEPRINT TOWARDS THE 02CARL CAMPAIGN

---

## 1. Scientific Positioning: Purely Qualitative Working Hypothesis

The scientific scope of Phase 06 is formally established **NOT as a numerical calculation or closed parameterization**, but strictly as a:

> ### **QUALITATIVE WORKING HYPOTHESIS AND CONCEPTUAL HOOK TOWARDS THE 02CARL CAMPAIGN**

The quantitative modeling of this paper formally concludes with the **Electro-Hydraulic Decoupling Index ($D_{EH}$)** in Phase 05. Phase 06 provides the **qualitative conceptual framework** that links the observed visual divergence between hydraulic retention and geoelectrical desaturation to clay mineralogy and surface conduction.

---

## 2. The Core Qualitative Hypothesis: Two Decoupled Controls

1. **Textural Scaling Control ($D_{EH}$ — Quantitative Milestone of this Paper)**:
   The **Electro-Hydraulic Decoupling Index** $D_{EH} = \frac{n_A}{m_{\mathrm{VG}}}$ models exclusively how the coupled exponent parameters scale against the **granulometric skeleton** (sand framework vs total fine matrix):
   $$D_{EH} = 2.05 \cdot 10^{0.0124 \cdot (\% \text{Fines})} \quad (r = +0.956,\ p = 0.001)$$
   This governs the theoretical rate of divergence between $S_e(h)$ and $\sigma_{\mathrm{norm}}(h)$ during desaturation.

2. **Mineralogical & Surface Buffering Control ($\text{GAP area}$ — Qualitative Conceptual Hypothesis)**:
   The visual space between the hydraulic retention curve and the electrical desaturation curve (termed **`GAP area`**) is **qualitatively modulated by the presence of expandable clay minerals (mixed-layer Illite/Smectite)**. Expandable smectite layers provide continuous surface conduction along the Electrical Double Layer (EDL), buffering bulk electrical conductivity and preventing it from plunging abruptly as capillary pore necks drain.

---

## 3. Physical Demonstration: The Qualitative Paradox of ML10 vs ML9

The qualitative foundation of this hypothesis is evidenced by comparing cores **ML9** and **ML10**:

| Soil Core | USDA Texture | Clay [%] | Total Phyllosilicates [%] | Smectite in I/S [%] | $D_{EH} = \frac{n_A}{m_{\mathrm{VG}}}$ | Qualitative GAP Observation |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **`ML9`** | Silt Loam | 26.2% | 31.0% | 72% | **36.14** | **Maximum GAP**: Silt-dominated throat pinch-off with segregated clay; sharp geoelectrical drop. |
| **`ML10`** | Silty Clay Loam | 33.0% | 65.5% | 75% | **26.48** | **Buffered GAP**: Visibly compressed gap despite higher clay content, sustained by pervasive smectite EDL. |

- **Qualitative Behavior in ML9**:
  Dominated by silt micro-pores ($57.3\%$) with moderate clay ($26.2\%$). As suction builds, pore necks drain first, severing electrolytic connectivity in bulk water while pore bodies stay full. In the absence of a pervasive smectitic EDL, electrical conductivity collapses vertically, generating a visually maximum GAP.
- **Qualitative Behavior in ML10**:
  Although ML10 has **more clay ($33.0\%$)** and more than **double the phyllosilicates ($65.5\%$)** than ML9, its visual GAP area is **compressed**. The expansive smectite network sustains a continuous ionic conduit along particle surfaces (EDL buffering), keeping relative conductivity higher across the tensiometric domain.

---

## 4. Phase 06 Master Figure: Central USDA Ternary with 4 Angular Normalized Trajectory Panels

The master visual artifact for Phase 06 (`fase06.png` layout) synthesizes the **4 Qualitative Reference Regimes**:

```
+-----------------------------------------------------------------------------------+
|  [ Top-Left Panel ]                                       [ Top-Right Panel ]     |
|  (b) Sandy Loam (ML7) | nA = 1.96                         (d) Silty Clay Loam     |
|  Reduced GAP (Sand Mitigation Effect)                         (ML10) | nA = 3.63  |
|                                                           Buffered GAP: EDL Effect|
|                                                                                   |
|                         +-----------------------+                                 |
|                         |      CENTRAL USDA     |                                 |
|                         |    TERNARY DIAGRAM    |                                 |
|                         |   Sand_R, ML7, ML9,   |                                 |
|                         |          ML10         |                                 |
|                         +-----------------------+                                 |
|                                                                                   |
|  [ Bottom-Left Panel ]                                    [ Bottom-Right Panel ]  |
|  (a) Clean Sand | nA = 1.84                               (c) Silt Loam (ML9)     |
|  Minimal GAP (Synchronous Transition)                         | nA = 4.38         |
|                                                           Maximum GAP: Silt Effect|
+-----------------------------------------------------------------------------------+
```

### The 4 Qualitative Reference Regimes:
1. **(a) Clean Sand (`Sand_R`)**: Minimal GAP due to steep, synchronous gravitational drainage in uniform macropores ($n_A = 1.84$).
2. **(b) Sandy Loam (`ML7`)**: Reduced GAP where the sand skeleton ($40.1\%$) mitigates tortuosity development ($n_A = 1.96$).
3. **(c) Silt Loam (`ML9`)**: Maximum GAP driven by silt throat pinch-off with segregated clay ($n_A = 4.38$).
4. **(d) Silty Clay Loam (`ML10`)**: Buffered GAP where pervasive smectite EDL buffering sustains electrical conduction ($n_A = 3.63$).

---

## 5. Outlook: Conceptual Springboard towards the `02Carl` Campaign

The formal quantitative modeling, numerical isolation, and joint inversion of the **smectite EDL surface buffering mechanism** is the primary objective of the upcoming dedicated publication based on the **`Hyprop_geotom_02Carl`** experimental campaign.

Key advancements planned for `02Carl`:
1. **Explicit Waxman-Smits / Revil Joint Inversion**: Directly incorporating cation exchange capacity ($\mathrm{CEC}$) and surface conductivity ($\sigma_s$).
2. **High-Suction Terminal Resistance Constraint**: Direct physical measurement of $\mathrm{EC}_{\mathrm{res}}$ past tensiometer cavitation ($h > 1500\ \mathrm{kPa}$) using post-evaporation 4-point probe readings.
3. **Validation of Textural vs Mineralogical Decoupling**: Testing the $D_{EH}$ scaling law and EDL buffering function across diverse geological lithofacies.
