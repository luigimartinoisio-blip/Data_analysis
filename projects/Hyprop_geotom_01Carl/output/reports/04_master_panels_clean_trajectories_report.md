# METHODOLOGICAL REPORT 04: MASTER PANELS AND CLEAN THEORETICAL TRAJECTORIES [0, 1]

---

## 1. Objective and Methodological Rationale

Following the exhaustive quadripole screening and mathematical inversion of Phase 03, **Phase 04** implements the transition toward a **decluttered, standardized theoretical representation**.

### Core Principles of Phase 04:
1. **Total Decluttering**: Removal of experimental scatter points and transient measurement fluctuations. Each soil is represented exclusively by its continuous theoretical trajectories in the normalized state space $[0, 1]$.
2. **Hydraulic Hard Lock**: The hydraulic retention curve $S_e(h)$ is rigidly parameterized by the van Genuchten (1980) parameters $(\alpha_{\mathrm{VG}}, n_{\mathrm{VG}}, m_{\mathrm{VG}})$ independently determined and validated from the HYPROP2 evaporation experiment.
3. **Inherited Benchmark Petrophysical Properties**: The coupled relative electrical conductivity $\sigma_{\mathrm{norm}}(h) = [1 + (\alpha_{\mathrm{VG}} h)^{n_{\mathrm{VG}}}]^{-m_{\mathrm{VG}} n_A}$ inherits the saturation exponent $n_A$ derived from the undisturbed basal benchmark (Layer 4 / `qp5` or `geom_lower`), representing the intrinsic soil matrix response free from surface desiccation artifacts.
4. **Air Entry Indication**: Each trajectory clearly marks the air entry suction $\psi_{\mathrm{AEP}} = 1/\alpha_{\mathrm{VG}}$, indicating the onset of capillary macropore drainage.
5. **Nomenclature Mandate**: The displacement between the two curves is designated strictly as the **GAP area** (or **GAP**), representing the integrated topological divergence between hydraulic water retention and electrical current path disconnection.

---

## 2. Sample Classification: Without Warnings vs With Warnings

To ensure absolute scientific transparency, the 8 investigated soil cores are categorized into two distinct operational groups based on the diagnostic screening conducted in Phase 00–03:

### A. Group Without Warnings (Canonical Matrix Response)
These cores exhibit monotonic electrical decay, optimal dynamic range ($\mathrm{EC}_{\mathrm{sat}}/\mathrm{EC}_{\mathrm{res}} > 1.30$), and synchronous or near-synchronous phase transitions ($\Lambda_{\mathrm{delay}} \le 2.50$):
- **`Sand_R`** (Clean Sand): Ideal monodisperse drainage, step-like transition ($n_{\mathrm{VG}} = 8.395$), $\Lambda_{\mathrm{delay}} = 0.88$, minimal GAP area.
- **`ML7`** (Sandy Loam): Balanced quartz skeleton ($40.1\%$ sand), early air entry ($\psi_{\mathrm{AEP}} = 1.32\ \mathrm{kPa}$), $\Lambda_{\mathrm{delay}} = 2.11$, $n_A = 1.96$.
- **`ML9`** (Silt Loam): Severe silt pore-neck constriction ($57.3\%$ silt), $\Lambda_{\mathrm{delay}} = 1.30$, highly amplified saturation exponent ($n_A = 4.38$), maximum GAP area.
- **`ML8`** (Silt Loam): Quarzose silt with smectite presence, $\Lambda_{\mathrm{delay}} = 0.30$, $n_A = 2.28$.

### B. Group With Warnings / Diagnostic Notices (Electrochemical & Boundary Effects)
These cores exhibit operational or boundary phenomena that required explicit diagnostic cards:
- **`ML1`** (Silt Loam): **Warning: Early tensiometer cavitation at $h = 64\ \mathrm{kPa}$ (tail extrapolated)**. HYPROP experiment cavitated prematurely at $64\ \mathrm{kPa}$; the desaturation tail is an uncalibrated van Genuchten mathematical extrapolation ($n_A = 2.85$).
- **`ML4`** (Loam): **Warning: Extended Plateau ($\Lambda_{\mathrm{delay}} = 2.70 > 2.50$)**. Retention of pore water in fine necks delays conductive network breakdown beyond hydraulic air entry ($n_A = 1.73$).
- **`ML10`** (Silty Clay Loam): **Notice: Plotted qp5 (L4, $\Lambda_{\mathrm{delay}}=1.89$, $n_A = 3.6325$); L3 qp6 excluded (severe $\Lambda=77.1$)**. Highly active smectite fabric ($65.5\%$ phyllosilicates) where basal Layer 4 (`qp5`) preserves physical validity while Layer 3 (`qp6`) suffered severe lateral anisotropy.

### C. Excluded Core: Sample ML6
- **`ML6`** (Silty Clay): **Eliminated from Post-Phase 03 Workflows**. Exhibited mathematical collapse onto the lower boundary ($n_A = 1.001$, `FAILED BOUNDS`) driven by dynamic range collapse ($\mathrm{DR} = 1.16 < 1.30$) and continuous smectitic surface conduction across all suctions. Documented via a dedicated exclusion card in the Master Panel.

---

## 3. Master Synthesis Table

| Sample | USDA Texture | Sand [%] | Silt [%] | Clay [%] | $\alpha_{\mathrm{VG}}$ [$\mathrm{kPa}^{-1}$] | $n_{\mathrm{VG}}$ [-] | $\psi_{\mathrm{AEP}}$ [$\mathrm{kPa}$] | $\mathcal{K} = 1/m_{\mathrm{VG}}$ | $n_A$ [-] | Warning Status | Diagnostic Note |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|:---|
| **`Sand_R`** | Sand | 100.0 | 0.0 | 0.0 | 0.1825 | 8.395 | 5.48 | 1.14 | 1.84 | Without Warnings | Canonical step-like drainage |
| **`ML7`** | Sandy Loam | 40.1 | 41.7 | 18.2 | 0.7566 | 1.244 | 1.32 | 5.10 | 1.96 | Without Warnings | Sand mitigation effect |
| **`ML9`** | Silt Loam | 16.5 | 57.3 | 26.2 | 0.3732 | 1.138 | 2.68 | 8.25 | 4.38 | Without Warnings | Maximum geometric pinch-off |
| **`ML8`** | Silt Loam | 7.7 | 69.5 | 22.8 | 0.8555 | 1.117 | 1.17 | 9.55 | 2.28 | Without Warnings | High silt fraction |
| **`ML1`** | Silt Loam | 20.7 | 53.1 | 26.2 | 0.2539 | 1.120 | 3.94 | 9.33 | 2.85 | With Warnings | Early tensiometer cavitation at $h = 64\ \mathrm{kPa}$ |
| **`ML4`** | Loam | 28.4 | 46.9 | 24.7 | 0.6434 | 1.163 | 1.55 | 7.13 | 1.73 | With Warnings | Extended Plateau ($\Lambda_{\mathrm{delay}} = 2.70$) |
| **`ML10`** | Silty Clay Loam | 6.8 | 60.2 | 33.0 | 0.2356 | 1.159 | 4.24 | 7.29 | 3.63 | With Warnings | Plotted qp5 (L4, $n_A = 3.63$); L3 qp6 excluded |
| *`ML6`* | *Silty Clay* | *10.5* | *46.2* | *43.3* | *0.0643* | *1.236* | *15.55* | *5.24* | *1.001* | **EXCLUDED** | *Archie collapse ($n_A=1.001$), low DR ($1.16$), smectite EDL* |

---

## 4. Output Figures and Artifacts

### A. Multi-Panel Composite Figures:
1. **Master Panel ($2 \times 4$ Grid)**:
   - [master_panel_fase04_clean_2x4.png](file:///c:/Users/luigi/git/github.com/luigimartinoisio-blip/Data_analysis/projects/Hyprop_geotom_01Carl/output/figures/fase04/master_panel_fase04_clean_2x4.png)
   - Displays 7 validated soils side-by-side in normalized $[0, 1]$ space ordered by $\mathcal{K}$, plus the dedicated 8th panel documenting the exclusion of `ML6`.
2. **Sub-Panel: Without Warnings ($2 \times 2$ Grid)**:
   - [panel_fase04_senza_warning_2x2.png](file:///c:/Users/luigi/git/github.com/luigimartinoisio-blip/Data_analysis/projects/Hyprop_geotom_01Carl/output/figures/fase04/panel_fase04_senza_warning_2x2.png)
   - Features `Sand_R`, `ML7`, `ML8`, `ML9`.
3. **Sub-Panel: With Warnings / Diagnostic Notes ($1 \times 3$ Grid)**:
   - [panel_fase04_con_warning_2x2.png](file:///c:/Users/luigi/git/github.com/luigimartinoisio-blip/Data_analysis/projects/Hyprop_geotom_01Carl/output/figures/fase04/panel_fase04_con_warning_2x2.png)
   - Features `ML1`, `ML4`, `ML10`, complete with explicit diagnostic warning boxes.

### B. Individual High-Resolution Trajectory Figures:
- `Sand_R`: [plot_fase04_clean_trajectory_Sand_R.png](file:///c:/Users/luigi/git/github.com/luigimartinoisio-blip/Data_analysis/projects/Hyprop_geotom_01Carl/output/figures/fase04/plot_fase04_clean_trajectory_Sand_R.png)
- `ML7`: [plot_fase04_clean_trajectory_ML7.png](file:///c:/Users/luigi/git/github.com/luigimartinoisio-blip/Data_analysis/projects/Hyprop_geotom_01Carl/output/figures/fase04/plot_fase04_clean_trajectory_ML7.png)
- `ML9`: [plot_fase04_clean_trajectory_ML9.png](file:///c:/Users/luigi/git/github.com/luigimartinoisio-blip/Data_analysis/projects/Hyprop_geotom_01Carl/output/figures/fase04/plot_fase04_clean_trajectory_ML9.png)
- `ML8`: [plot_fase04_clean_trajectory_ML8.png](file:///c:/Users/luigi/git/github.com/luigimartinoisio-blip/Data_analysis/projects/Hyprop_geotom_01Carl/output/figures/fase04/plot_fase04_clean_trajectory_ML8.png)
- `ML1`: [plot_fase04_clean_trajectory_ML1.png](file:///c:/Users/luigi/git/github.com/luigimartinoisio-blip/Data_analysis/projects/Hyprop_geotom_01Carl/output/figures/fase04/plot_fase04_clean_trajectory_ML1.png)
- `ML4`: [plot_fase04_clean_trajectory_ML4.png](file:///c:/Users/luigi/git/github.com/luigimartinoisio-blip/Data_analysis/projects/Hyprop_geotom_01Carl/output/figures/fase04/plot_fase04_clean_trajectory_ML4.png)
- `ML10`: [plot_fase04_clean_trajectory_ML10.png](file:///c:/Users/luigi/git/github.com/luigimartinoisio-blip/Data_analysis/projects/Hyprop_geotom_01Carl/output/figures/fase04/plot_fase04_clean_trajectory_ML10.png)
*(Note: `plot_fase04_clean_trajectory_ML6.png` has been removed following its methodological exclusion).*
