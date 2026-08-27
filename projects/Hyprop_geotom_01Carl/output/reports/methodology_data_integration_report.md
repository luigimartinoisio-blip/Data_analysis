# Technical & Methodological Report: Integrated Hydrogeophysical Database (GeoTom-16 & HYPROP2)

**Author / Project**: Advanced Agentic Hydrogeophysics Lab  
**Date**: August 2026  
**Document Version**: 1.0.0  
**Scope**: Complete mathematical, physical, and algorithmic documentation of the data integration pipeline coupling 1D soil water retention (HYPROP2) with 3D cylindrical electrical resistivity tomography (GeoTom-16).

---

## 1. Executive Summary & Experimental Objectives

The purpose of this pipeline is to establish a rigorous, synchronized hydrogeophysical database for unsaturated soils undergoing continuous laboratory evaporation. The database couples:
1. **Hydraulic State Variables**: Volumetric water content $\theta(t)$, matric suction $\psi_m(t)$, degree of saturation $S_r(t)$, and net weight loss $m(t)$ monitored continuously by **HYPROP2** (METER Group).
2. **Electrical Properties**: High-frequency electrical resistivity measurements across 16 pin electrodes embedded in an ABS cylindrical sample holder, measured via **GeoTom-16** (Geolog).

The integrated database comprises **10 complete experimental series** (9 landslide soil samples `ML1` to `ML10` and 1 lab reference sand `Sand_R`), totaling **1,291 synchronized time steps** and **43 quality-controlled variables**.

---

## 2. Experimental Geometry & Sample Holder Specifications

The sample holder consists of an insulating ABS cylindrical ring with the following standardized geometry:

| Geometric Parameter | Variable | Value | Unit |
| :--- | :---: | :---: | :---: |
| **Inner Radius** | $r$ | $4.00$ | $\text{cm}$ |
| **Total Height** | $h$ | $5.00$ | $\text{cm}$ |
| **Nominal Volume** | $V$ | $250.00$ | $\text{cm}^3$ |
| **Cross-Sectional Area** | $A$ | $50.265$ | $\text{cm}^2$ |

### 2.1 16-Electrode Cylindrical Array Configuration
The 16 stainless steel pin electrodes are arranged in 4 horizontal rings and 4 vertical columns ($90^\circ$ angular spacing):

- **Ring 1 (Top)**: $z = 4.0\text{ cm}$ (Electrodes: 1, 5, 9, 13)
- **Ring 2 (Upper Middle)**: $z = 3.0\text{ cm}$ (Electrodes: 2, 6, 10, 14)
- **Ring 3 (Lower Middle)**: $z = 2.0\text{ cm}$ (Electrodes: 3, 7, 11, 15)
- **Ring 4 (Bottom)**: $z = 1.0\text{ cm}$ (Electrodes: 4, 8, 12, 16)

### 2.2 Tensiometer Positions
- **Upper Tensiometer ($T_1$)**: Installed at height $z_1 = 3.75\text{ cm}$ from base (depth $-1.25\text{ cm}$ from top).
- **Lower Tensiometer ($T_2$)**: Installed at height $z_2 = 1.25\text{ cm}$ from base (depth $-3.75\text{ cm}$ from top).

```
                 Top Surface (Evaporating, z = 5.0 cm)
  +-------------------------------------------------------------+
  |  o (1)        o (5)         o (9)         o (13)   [z=4.0] | <-- Ring 1 (Upper)
  |       [=== Tensiometer 1 (Upper, z=3.75 cm) ===]           |
  |  o (2)        o (6)         o (10)        o (14)   [z=3.0] | <-- Ring 2
  + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - + <-- Mid-plane (z = 2.5 cm)
  |  o (3)        o (7)         o (11)        o (15)   [z=2.0] | <-- Ring 3
  |       [=== Tensiometer 2 (Lower, z=1.25 cm) ===]           |
  |  o (4)        o (8)         o (12)        o (16)   [z=1.0] | <-- Ring 4 (Lower)
  +-------------------------------------------------------------+
                 Insulated Bottom Base (z = 0.0 cm)
```

---

## 3. Representative Quadrupole Schemes & Geometric Factors

To maintain high signal-to-noise ratio and capture spatial anisotropy without electrode polarization artifacts, 12 representative configurations are selected across 4 geometric categories:

| Category | Pair Code | Direct Quadrupole $(A, B, M, N)$ | Reciprocal Quadrupole $(M, N, A, B)$ | Geometric Factor $K$ [m] | Description |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Upper** | `qp1` | $(1, 5, 13, 9)$ | $(13, 9, 1, 5)$ | $0.1580$ | Ring 1 ($z=4.0\text{ cm}, 0^\circ$) |
| **Upper** | `qp2` | $(2, 6, 14, 10)$ | $(14, 10, 2, 6)$ | $0.1580$ | Ring 2 ($z=3.0\text{ cm}, 0^\circ$) |
| **Upper** | `qp3` | $(6, 10, 2, 14)$ | $(2, 14, 6, 10)$ | $0.1580$ | Ring 2 ($z=3.0\text{ cm}, 90^\circ$) |
| **Lower** | `qp4` | $(3, 7, 15, 11)$ | $(15, 11, 3, 7)$ | $0.1580$ | Ring 3 ($z=2.0\text{ cm}, 0^\circ$) |
| **Lower** | `qp5` | $(4, 8, 16, 12)$ | $(16, 12, 4, 8)$ | $0.1580$ | Ring 4 ($z=1.0\text{ cm}, 0^\circ$) |
| **Lower** | `qp6` | $(7, 11, 3, 15)$ | $(3, 15, 7, 11)$ | $0.1580$ | Ring 3 ($z=2.0\text{ cm}, 90^\circ$) |
| **Dipole** | `qp7` | $(1, 2, 3, 4)$ | $(3, 4, 1, 2)$ | $0.1850$ | Vertical Dipole-Dipole ($0^\circ$) |
| **Dipole** | `qp8` | $(5, 6, 7, 8)$ | $(7, 8, 5, 6)$ | $0.1850$ | Vertical Dipole-Dipole ($90^\circ$) |
| **Wenner** | `W1` | $(1, 4, 2, 3)$ | - | $0.2110$ | Vertical Wenner ($0^\circ$, Outer) |
| **Wenner** | `W3` | $(9, 12, 10, 11)$ | - | $0.2110$ | Vertical Wenner ($0^\circ$, Inner) |
| **Wenner** | `W2` | $(5, 8, 6, 7)$ | - | $0.2110$ | Vertical Wenner ($90^\circ$, Outer) |
| **Wenner** | `W4` | $(13, 16, 14, 15)$ | - | $0.2110$ | Vertical Wenner ($90^\circ$, Inner) |

### 3.1 Apparent Resistivity Formulation
For any quadrupole measuring potential difference $\Delta V$ [mV] under injected current $I$ [mA], the resistance $R$ [$\Omega$] and raw apparent resistivity $\rho_{\text{app}}$ [$\Omega\cdot\text{m}$] are given by:
\[
R = \frac{|\Delta V|}{I} \quad [\Omega]
\]
\[
\rho_{\text{app}} = K \cdot R \quad [\Omega\cdot\text{m}]
\]

---

## 4. Temperature Normalization to $25^\circ\text{C}$ (Hayashi, 1990)

Because electrolytic electrical conductivity increases with temperature (~$2\%\,^\circ\text{C}^{-1}$ due to decreasing fluid viscosity), all resistivity values are standardized to the reference temperature $T_{\text{ref}} = 25.0^\circ\text{C}$ using the Hayashi (1990) formulation:

\[
\rho_{25} = \rho(T) \cdot \left[1 + \alpha_T \cdot (T - 25.0)\right]
\]

where:
- $\rho(T)$ = Apparent resistivity at measurement temperature $T$ [$\Omega\cdot\text{m}$]
- $T$ = Synchronized sample temperature measured by HYPROP2 internal thermistor [$^\circ\text{C}$]
- $\alpha_T = 0.0210\,^\circ\text{C}^{-1}$ = Thermal coefficient for pore water electrolytes.

---

## 5. Temporal Barycenter Synchronization

GeoTom ERT measurements are sequential sweeps taking $\Delta T_{\text{ERT}} \approx 9 - 16\text{ minutes}$, while HYPROP2 logs punctual readings every 10 minutes. To eliminate phase lag, synchronization is performed using the **ERT temporal barycenter**:

\[
t_{\text{bary}} = t_{\text{start}} + \frac{t_{\text{end}} - t_{\text{start}}}{2}
\]

Continuous spline interpolation is applied to the HYPROP time series to evaluate exact hydraulic parameters at $t_{\text{bary}}$:
\[
X(t_{\text{bary}}) = \text{Spline}\left(\{t_{\text{hyprop}, i}, X_i\}\right)(t_{\text{bary}})
\]

---

## 6. Soil Hydraulic State Mathematics

From the synchronized net mass $m(t_{\text{bary}})$ [g] and oven-dry soil mass $m_{\text{dry}}$ [g]:

### 6.1 Volumetric Water Content $\theta(t)$
\[
\theta(t) = \frac{m(t) - m_{\text{dry}}}{\rho_w \cdot V} \times 100\% \quad [\text{Vol}\%]
\]
where $\rho_w = 1.00\text{ g/cm}^3$ and $V = 250.0\text{ cm}^3$.

### 6.2 Gravimetric Water Content $w(t)$
\[
w(t) = \frac{m(t) - m_{\text{dry}}}{m_{\text{dry}}} \times 100\% \quad [\%]
\]

### 6.3 Degree of Saturation $S_r(t)$
\[
S_r(t) = \frac{\theta(t) / 100}{\phi} \quad [-]
\]
where $\phi = 1 - \frac{\rho_d}{\rho_s}$ is soil porosity ($\rho_d = m_{\text{dry}}/V$, $\rho_s = 2.65\text{ g/cm}^3$).

### 6.4 Matric Suction Mean $\psi_m(t)$
From the upper ($\psi_{\text{up}}$) and lower ($\psi_{\text{low}}$) tensiometer readings (expressed strictly in $\text{kPa}$, where $1\text{ kPa} = 10\text{ hPa}$):
\[
\psi_{\text{mean}}(t) = \sqrt{\psi_{\text{up}}(t) \cdot \psi_{\text{low}}(t)} \quad [\text{kPa}]
\]

---

## 7. Geometric Means of Calibrated Resistivity per Category

Because electrical resistivity in heterogeneous porous media follows a log-normal distribution, representative category values are computed using the **geometric mean** across active quadrupoles:

\[
\bar{\rho}_{25,\text{geom}} = \left(\prod_{i=1}^N \rho_{25,i}\right)^{1/N} = \exp\left(\frac{1}{N}\sum_{i=1}^N \ln(\rho_{25,i})\right)
\]

1. **Upper Horizontal Mean**: $\bar{\rho}_{25,\text{up}} = \left(\rho_{25,\text{qp1}} \cdot \rho_{25,\text{qp2}} \cdot \rho_{25,\text{qp3}}\right)^{1/3}$
2. **Lower Horizontal Mean**: $\bar{\rho}_{25,\text{low}} = \left(\rho_{25,\text{qp4}} \cdot \rho_{25,\text{qp5}} \cdot \rho_{25,\text{qp6}}\right)^{1/3}$
3. **Dipole-Dipole Mean**: $\bar{\rho}_{25,\text{dip}} = \left(\rho_{25,\text{qp7}} \cdot \rho_{25,\text{qp8}}\right)^{1/2}$
4. **Wenner Mean**: $\bar{\rho}_{25,\text{wen}} = \left(\rho_{25,\text{W1}} \cdot \rho_{25,\text{W2}} \cdot \rho_{25,\text{W3}} \cdot \rho_{25,\text{W4}}\right)^{1/4}$

---

## 8. Quality Assurance & Reciprocal Error Analysis

For all quadrupole pairs (`qp1` to `qp8`), direct ($R_{\text{dir}}$) and reciprocal ($R_{\text{rec}}$) resistances are acquired. The reciprocal error $\epsilon_{\text{rec}}$ is evaluated as:

\[
\epsilon_{\text{rec}} = 2 \cdot \frac{|R_{\text{dir}} - R_{\text{rec}}|}{R_{\text{dir}} + R_{\text{rec}}} \times 100\%
\]

A timestep is flagged as high quality (`qualita_qc_pass = True`) when the average reciprocal error satisfies:
\[
\bar{\epsilon}_{\text{rec}} < 5.0\%
\]

---

## 9. Processed Database Summary

| Sample ID | Field Code | Landslide Sector | Sampling Depth | Timesteps | Moisture Range $\theta$ [%] | Suction Range $\psi_m$ [kPa] |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **`ML1`** | 5a | Steep Slope Sector | Surface ($0\text{ cm}$) | 106 | $48.2\% \rightarrow 22.1\%$ | $0.1 \rightarrow 850\text{ kPa}$ |
| **`ML3`** | 1a | Steep Slope Sector | Surface ($0\text{ cm}$) | 141 | $46.5\% \rightarrow 23.9\%$ | $0.2 \rightarrow 1240\text{ kPa}$ |
| **`ML4`** | 1b | Steep Slope Sector | Depth ($-50\text{ cm}$) | 113 | $45.1\% \rightarrow 21.8\%$ | $0.1 \rightarrow 780\text{ kPa}$ |
| **`ML5`** | 2a | Counterslope Sector | Surface ($0\text{ cm}$) | 168 | $49.4\% \rightarrow 24.3\%$ | $0.2 \rightarrow 1150\text{ kPa}$ |
| **`ML6`** | 2b | Counterslope Sector | Depth ($-50\text{ cm}$) | 125 | $47.8\% \rightarrow 23.0\%$ | $0.1 \rightarrow 920\text{ kPa}$ |
| **`ML7`** | 3a | Detachment Sector | Surface ($0\text{ cm}$) | 114 | $44.9\% \rightarrow 20.7\%$ | $0.2 \rightarrow 890\text{ kPa}$ |
| **`ML8`** | 3b | Detachment Sector | Depth ($-50\text{ cm}$) | 112 | $43.8\% \rightarrow 21.2\%$ | $0.2 \rightarrow 940\text{ kPa}$ |
| **`ML9`** | 4b | Detachment Sector | Depth ($-50\text{ cm}$) | 143 | $46.2\% \rightarrow 22.5\%$ | $0.1 \rightarrow 1050\text{ kPa}$ |
| **`ML10`** | 6a | Undisturbed Outside | Surface ($0\text{ cm}$) | 101 | $52.1\% \rightarrow 26.4\%$ | $0.1 \rightarrow 1320\text{ kPa}$ |
| **`Sand_R`**| Lab Ref | Calibration Outgroup | Standard Cell | 168 | $38.5\% \rightarrow 4.1\%$ | $0.05 \rightarrow 18\text{ kPa}$ |
| **TOTAL** | - | - | - | **1,291** | - | - |

---

## 10. Database File Structure

All integrated CSV tables are versioned and stored under:
- Per-sample tables: `projects/Hyprop_geotom_01Carl/data/processed/tabelle_campioni/{SAMPLE_ID}_serie_integrata.csv`
- Global concatenated matrix: `projects/Hyprop_geotom_01Carl/data/processed/dataset_completo_tutti_campioni.csv`
- Reciprocal QC report: `projects/Hyprop_geotom_01Carl/data/processed/report_qualita_reciproci.csv`
