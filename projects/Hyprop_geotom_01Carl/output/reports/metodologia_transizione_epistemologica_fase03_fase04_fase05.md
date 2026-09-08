# EPISTEMOLOGICAL AND METHODOLOGICAL TREATISE: THE TRANSITION FROM MATHEMATICAL INVERSION (PHASE 03) TO PHYSICAL-CONCEPTUAL REGIMES (PHASES 04 & 05)

---

## 1. Executive Summary & Epistemological Framework

In coupled hydro-geophysical research, a recurring methodological pitfall is **"epistemic overfitting"**: mistaking the numerical convergence of unconstrained mathematical regressions for genuine physical properties of the porous matrix.

This treatise formally articulates the scientific necessity of transitioning from:
- **Phase 03 (Strict Pointwise Mathematical Inversion)**: Evaluating multi-parameter regressions, empirical formulations (Boyd et al., 2024), coupled van Genuchten–Archie models, azimuthal anisotropy $\lambda(h) = \rho_{90^\circ}/\rho_{0^\circ}$, and boundary collapses across all 80 quadripoles;
to:
- **Phases 04 & 05 (Physical-Conceptual Trajectories and Qualitative Regimes)**: Standardizing clean theoretical trajectories in normalized state space $[0, 1]$, defining the hydraulic **Amplificator Factor** $\mathcal{K} = 1/m_{\mathrm{VG}}$, quantifying the **GAP area**, and establishing the 4 fundamental physical regimes of soil hydro-geophysics.

The bridge between these two paradigms is grounded in a singular, profound physical insight discovered during this project: **the absence of an experimentally measured, independently locked residual electrical conductivity ($\mathrm{EC}_{\mathrm{res}}$) at true residual saturation ($S_e = 0$).**

---

## 2. Phase 03: The Mathematical Frontier and What It Revealed

### 2.1 The Scope of Phase 03
Phase 03 performed exhaustive point-by-point evaluations across 80 horizontal quadripoles (10 cores $\times$ 8 quadripoles/macro-configurations). It tested two competing mathematical formulations:
1. **The Empirical Formulation of Boyd et al. (2024)**:
   $$\sigma_{\mathrm{norm}}(h) = \left[1 + (\alpha_{\mathrm{EC}} h)^{n_{\mathrm{EC}}}\right]^{-m_{\mathrm{EC}}}$$
   where $\alpha_{\mathrm{EC}}$ and $n_{\mathrm{EC}}$ are freely optimized parameters.
2. **The Coupled van Genuchten – Archie – Waxman-Smits Formulation**:
   $$\sigma_{\mathrm{norm}}(h) = \left[1 + (\alpha_{\mathrm{VG}} h)^{n_{\mathrm{VG}}}\right]^{-m_{\mathrm{VG}} n_A}$$
   where hydraulic parameters $(\alpha_{\mathrm{VG}}, n_{\mathrm{VG}}, m_{\mathrm{VG}})$ are hard-locked from HYPROP-FIT, and the saturation exponent $n_A$ is the sole regression variable.

### 2.2 The Diagnostic Screening Criteria
Phase 03 instituted strict mathematical screening filters:
- Monotonicity test: Spearman rank correlation $\rho_s(\rho_{25^\circ\mathrm{C}}, h) > 0.85$ ($\rho_s(\sigma, h) < -0.85$);
- Instrumental noise: Mean reciprocity error $\epsilon_{\mathrm{rec}} < 10\%$;
- Dynamic Range: $\mathrm{DR} = \mathrm{EC}_{\mathrm{sat}} / \mathrm{EC}_{\mathrm{res}} > 1.30$;
- Azimuthal Anisotropy Ratio: $\lambda(h) = \rho_{90^\circ}(h) / \rho_{0^\circ}(h) \approx 1.0$;
- Plateau Delay Index: $\Lambda_{\mathrm{delay}} = \frac{\psi_{\mathrm{EC}}}{\psi_{\mathrm{AEP}}} = \frac{\alpha_{\mathrm{VG}}}{\alpha_{\mathrm{EC}}}$.

### 2.3 Mathematical Findings: Three Distinct Numerical Regimes
As detailed in [Methodological Report 03](file:///c:/Users/luigi/git/github.com/luigimartinoisio-blip/Data_analysis/projects/Hyprop_geotom_01Carl/output/reports/03_normalized_comparison_and_plateau_screening_report.md), Phase 03 successfully segregated the dataset into three distinct behavioral regimes:
1. **Canonical Synchronous Regime ($\Lambda_{\mathrm{delay}} \le 1.50$)**:
   Observed in `Sand_R`, `ML9`, `ML8`. Hydraulic desaturation and conductive network collapse occur nearly simultaneously.
2. **Stratified / Transition Regime ($1.50 < \Lambda_{\mathrm{delay}} \le 3.00$)**:
   Observed in `ML7`, `ML1`, `ML10`, `ML4`. Upper cortical layers (L1–L2) develop drying microcracks and delayed phase transitions, whereas the basal benchmark (Layer 4 / `qp5`) preserves physical monotonicity.
3. **EDL Dominance / Plateau Delay Regime ($\Lambda_{\mathrm{delay}} > 3.00$)**:
   Observed in `ML5`, `ML6`, and upper layers of `ML10`. Electrical conductivity refuses to decay following hydraulic air entry, forcing the coupled Archie model into mathematical collapse ($n_A = 1.001$, `FAILED BOUNDS`).

---

## 3. The Root Bottleneck: The Missing Constraint on $\mathrm{EC}_{\mathrm{res}}$

### 3.1 The Classical Archie Assumption vs Electrochemical Reality
The classical second Archie relation assumes an electrically inert matrix saturated with a conducting pore electrolyte:
$$\sigma(S_e) = \sigma_{\mathrm{sat}} S_e^{n_A}$$
As suction increases and effective saturation approaches zero ($S_e \to 0$), Archie's law dictates that bulk electrical conductivity must strictly vanish:
$$\lim_{S_e \to 0} \sigma(S_e) = 0$$

In natural clayey and silty soils, however, the matrix is not inert. Mineral surfaces—particularly smectite and mixed-layer illite/smectite (I/S)—host an **Electrical Double Layer (EDL)** characterized by excess hydrated counter-ions (Waxman & Smits, 1968; Revil et al., 1998):
$$\sigma(h) = \sigma_{\mathrm{res}} + (\sigma_{\mathrm{sat}} - \sigma_{\mathrm{res}}) S_e(h)^{n_A}$$
where the residual asymptotic conductivity:
$$\sigma_{\mathrm{res}} = \frac{1}{F} B Q_v$$
is governed by the volumetric cation exchange capacity $Q_v$ and equivalent ionic mobility $B$.

### 3.2 The Experimental Truncation in HYPROP2 Testing
The fundamental experimental reality of the HYPROP2 evaporation protocol is that **the test terminates upon cavitation of the tensiometer ceramic cups**, typically between $h \approx 500\ \mathrm{kPa}$ and $1500\ \mathrm{kPa}$.

At this terminal suction:
- Coarse sands (`Sand_R`) reach true residual saturation ($S_e \approx 0.00 - 0.02$).
- Loams and sandy loams (`ML7`) drain to intermediate saturations ($S_e \approx 0.20$).
- High-surface-area silt and clay soils (`ML9`, `ML8`, `ML10`, `ML6`) stop while retaining substantial liquid water:
  $$S_e(h_{\mathrm{end}}) \approx 0.25 - 0.45$$
  corresponding to volumetric moisture contents $\theta \approx 15\% - 32\%$.

### 3.3 The Mathematical Consequence: Parameter Equifinality
Because $S_e \to 0$ was never reached experimentally:
1. **$\mathrm{EC}_{\mathrm{res}}$ was not an experimentally measured boundary condition**, but an unconstrained extrapolation parameter.
2. In numerical regressions where both $\mathrm{EC}_{\mathrm{res}}$ and $n_A$ are floating:
   - If $\mathrm{EC}_{\mathrm{res}}$ is underestimated by the algorithm, $n_A$ must artificially inflate ($n_A \to 4.38$ in `ML9`) to steepen the curve and reach the low estimated asymptote.
   - If $\mathrm{EC}_{\mathrm{res}}$ is high due to smectite conduction (as in `ML6`, where $\sigma$ varies only from $90.4$ to $66.2\ \mathrm{mS/m}$), the small dynamic range forces the coupled model to collapse onto its mathematical lower bound ($n_A = 1.001$, `FAILED BOUNDS`).
   - The discrepancy in apparent $n_A$ between `ML9` ($n_A = 4.38$) and `ML8` ($n_A = 2.28$), despite both possessing active I/S clay, is primarily an artifact of unconstrained $\mathrm{EC}_{\mathrm{res}}$ optimization absorbing differences in micro-crack formation and sample-electrode contact impedance.

**Scientific Conclusion**: Continuing to perform unconstrained pointwise mathematical regressions in Phase 03 without an independent, experimental lock on $\mathrm{EC}_{\mathrm{res}}$ leads to diminishing scientific returns and spurious physical deductions.

---

## 4. The Methodological Solution: Transition to Phases 04 & 05

### 4.1 Phase 04: Standardized Theoretical Trajectories $[0, 1]$
To transcend the noise of individual electrode contacts and unmeasured residual tails, **Phase 04** transitions from experimental scatter plots to **clean theoretical trajectories**:
1. **Hydraulic Parameters Locked**: The soil water retention curve $S_e(h)$ is hard-locked to the independently validated HYPROP parameters $(\alpha_{\mathrm{VG}}, n_{\mathrm{VG}}, m_{\mathrm{VG}})$.
2. **Matrix Benchmark Representative**: Each soil is assigned a single representative saturation exponent $n_A$ determined from its undisturbed basal layer (Layer 4 / Lower).
3. **Transparent Diagnostic Tagging**: Instead of discarding problematic soils or forcing artificial fits, specimens are cleanly categorized into:
   - **Group Without Warnings**: Validated canonical trajectories (`Sand_R`, `ML7`, `ML9`, `ML1`, `ML8`).
   - **Group With Warnings**: Transparently annotated with diagnostic notes (`ML6` DR collapse, `ML4` plateau delay, `ML10` Layer 3 anisotropy).

### 4.2 Phase 05: Physical Regimes & The Amplificator Factor $\mathcal{K}$
**Phase 05** elevates the analysis from sample-specific curves to a **universal physical-conceptual framework**:

#### 1. The Amplificator Factor $\mathcal{K}$:
$$\mathcal{K} = \frac{1}{m_{\mathrm{VG}}} = \frac{n_{\mathrm{VG}}}{n_{\mathrm{VG}} - 1}$$
$\mathcal{K}$ is **100% rigorous and strictly internal to the validated hydraulic retention measurement**. It does not depend on electrical regression, contact resistance, or unmeasured residual baselines. It mathematically quantifies the slope of the retention curve in log-space and dictates how rapidly capillary water is evacuated from pore throats.

#### 2. The GAP Area:
$$\text{GAP Area} = \int_{\log_{10} h_{\min}}^{\log_{10} h_{\max}} \left[ S_e(h) - \sigma_{\mathrm{norm}}(h) \right] \, d(\log_{10} h) \quad \text{for } S_e \ge \sigma_{\mathrm{norm}}$$
The GAP area measures the integrated topological lag between volumetric water content and the electrical disconnection of percolating pathways.

#### 3. The 5 Qualitative Case Studies:
By pairing Phase 04 clean trajectories with USDA ternary diagrams and bulk/clay mineralogical analyses, Phase 05 establishes how grain size and mineralogy govern the tug-of-war between geometric pore pinch-off and electrochemical surface conduction:
- **Case 1 (`Sand_R`)**: Coarse Quartz Skeleton $\implies$ Step-like drainage $\implies$ $\mathcal{K} \to 1.14$ $\implies$ **Minimal GAP**.
- **Case 2 (`ML9`)**: Silt Dominance $\implies$ Fine pore necks with severe pinch-off $\implies$ $\mathcal{K} = 8.25$ $\implies$ **Maximum GAP**.
- **Case 3 (`ML8`)**: Silt Loam $\implies$ Silt framework with active I/S clay $\implies$ Partial buffering.
- **Case 4 (`ML7`)**: Balanced Sandy Loam $\implies$ Sand fraction ($40.1\%$) mitigates tortuosity $\implies$ $\mathcal{K} = 5.10$ $\implies$ **Reduced GAP (Sand Mitigation Effect)**.
- **Case 5 (`ML6` & `ML10`)**: Pervasive Active Clay Matrix $\implies$ Smectite EDL sustains conduction $\implies$ **Buffered GAP / Dynamic Range Collapse**.

---

## 5. Comparative Paradigm Matrix

| Dimension | Phase 03 (Mathematical Inversion) | Phases 04 & 05 (Physical-Conceptual Regimes) |
|:---|:---|:---|
| **Primary Goal** | Pointwise numerical fitting across 80 quadripoles | Establishing universal physical soil regimes |
| **Input Data** | Raw experimental points, transient desaturation curves | Hard-locked hydraulic parameters + Basal benchmark |
| **Handling of Noise** | Filtered via reciprocity, monotonicity, anisotropy ratios | Decoupled through clean theoretical trajectories $[0, 1]$ |
| **Status of $\mathrm{EC}_{\mathrm{res}}$** | Free mathematical optimization parameter (ill-posed) | Identified as missing boundary condition; isolated |
| **Coupling Parameter** | Floating unconstrained $n_A$ absorbing artifacts | Geometric Amplificator Factor $\mathcal{K} = 1/m_{\mathrm{VG}}$ + GAP area |
| **Output Representation** | 80 quadripole curves with error bars and residuals | Standardized master panels, ternary plots, mineralogy |
| **Scientific Role** | Diagnostic audit revealing experimental limits | Predictive foundation for future experimental design |

---

## 6. Synthesis and Epistemological Conclusion

The progression from Phase 03 to Phases 04 and 05 represents the mature evolution of a scientific workflow:
1. Phase 03 pushed the mathematical inversion of raw experimental data to its absolute limit, exhaustively diagnosing noise, anisotropy, and numerical bounds.
2. In doing so, Phase 03 revealed that **the mathematical collapse of Archie's law is not a failure of soil physics, but the mathematical symptom of an experimentally unconstrained $\mathrm{EC}_{\mathrm{res}}$.**
3. Phases 04 and 05 synthesize these findings into an elegant, robust conceptual framework where geometric pore-size distribution ($\mathcal{K}$) and electrochemical mineralogy (EDL) are clearly disentangled.

This synthesis directly establishes the roadmap for the **Final Theoretical Hypothesis** and the design of the next generation of coupled hydro-geophysical experiments.
