# VADEMECUM METODOLOGICO INTEGRATO: PIPELINE IDRO-GEOFISICA `Hyprop_geotom_01Carl`

**Progetto**: Analisi Accoppiata HYPROP2 – GeoTom-16  
**Campagna**: `Hyprop_geotom_01Carl` (Campioni di Frana Carlone: ML1, ML3, ML4, ML5, ML6, ML7, ML8, ML9, ML10, Sand_R)  
**Versione**: 2.0 (Post Ristrutturazione Fasi 05 – 06)  

---

## 1. QUADRO GENERALE E OBIETTIVI SCIENTIFICI

Il presente Vademecum definisce la metodologia analitica, le equazioni matematiche, i criteri di screening e le regole grafiche per l'elaborazione dei dati accoppiati di ritenzione idraulica e tomografia di resistività elettrica 3D in cella cilindrica.

---

## 2. METROLOGIA E GEOMETRIA SPERIMENTALE

* **Portacampione**: Cilindro in ABS ($r = 4.00\ \mathrm{cm}$, $h = 5.00\ \mathrm{cm}$, $V = 250.0\ \mathrm{cm}^3$, $A = 50.265\ \mathrm{cm}^2$).
* **Array 16 Elettrodi**: 4 anelli orizzontali ($z = 4, 3, 2, 1\ \mathrm{cm}$) a spaziatura $90^\circ$ ($0^\circ, 90^\circ, 180^\circ, 270^\circ$).
* **Tensiometri**: Lungo / Upper ($z = 3.75\ \mathrm{cm}$) e Corto / Lower ($z = 1.25\ \mathrm{cm}$).
* **Normalizzazione Termica**: Hayashi (2004) a $T_{\mathrm{ref}} = 25.0^\circ\mathrm{C}$ con $\alpha_T = 0.0210\ ^\circ\mathrm{C}^{-1}$.
* **Sincronizzazione**: Centrata sul baricentro temporale ERT ($t_{\mathrm{bary}} = t_{\mathrm{start}} + \Delta T_{\mathrm{ERT}}/2$).

---

## 3. LE FASI ANALITICHE FONDANTI (FASI 01 – 04)

### 3.1 Fase 01 — Cross-Correlazioni e Controllo Qualità
* Calcolo resistività apparente calibrata $\rho_{25}$ e fit empirico bivariato.
* Controllo errore di reciprocità ($\epsilon_{\mathrm{rec}} < 5.0\%$).

### 3.2 Fase 02 — Inversione Accoppiata van Genuchten – Archie
* Modello idraulico: $S_e(h) = \left[ 1 + (\alpha_{\mathrm{VG}} h)^{n_{\mathrm{VG}}} \right]^{-m_{\mathrm{VG}}}$, con $m_{\mathrm{VG}} = 1 - 1/n_{\mathrm{VG}}$.
* Modello geoelettrico accoppiato: $\sigma_{\mathrm{norm}}(h) = S_e(h)^{n_A} = \left[ 1 + (\alpha_{\mathrm{VG}} h)^{n_{\mathrm{VG}}} \right]^{-m_{\mathrm{VG}} n_A}$.

### 3.3 Fase 03 — Screening di Validità Epistemologica
* Identificazione dei regimi canonici, gradienti verticali ed esclusione formale dei campioni con collasso fisico da EDL (es. `ML6`, $n_A = 1.001$, `FAILED BOUNDS`).

### 3.4 Fase 04 — Total Decluttering e Rappresentazione Continua
* Grafici master puramente teorici nello spazio normalizzato $[0, 1]$ con evidenziazione della `GAP area`.

---

## 4. RISTRUTTURAZIONE FASE 05: DECOUPLING INDEX $D_{EH}$ E SCALING GRANULOMETRICO

### 4.1 Definizione Formale del Decoupling Index
Si elimina l'uso intermedio del fattore $\mathcal{K}$ isolato e si definisce direttamente l'**Electro-Hydraulic Decoupling Index**:

$$D_{EH} = \frac{n_A}{m_{\mathrm{VG}}}$$

* **Significato Fisico**: $D_{EH}$ normalizza l'esponente di sensibilità alla disconnessione elettrica ($n_A$) rispetto all'ampiezza dello spettro capillare del mezzo ($m_{\mathrm{VG}}$).
* **Limite Asintotico a $0\%$ Fini (Sabbia Pulita, Sand_R)**:
  $$\lim_{\% \text{Fines} \to 0} D_{EH} = \frac{n_A}{1.0} = n_A \approx 2.05$$
  L'intercetta recupera esattamente il valore canonico di Archie per mezzi granulari sferici non consolidati ($n_A \approx 2.0$).

### 4.2 I Due Step Analitici di Fase 05
1. **Step 05.1 — Correlazione con le Singole Frazioni Granulometriche**:
   * $\log_{10}(D_{EH})$ vs **Sand %**: $r = -0.956$ ($p = 0.001$) $\longrightarrow$ Lo scheletro sabbioso mitiga il disaccoppiamento.
   * $\log_{10}(D_{EH})$ vs **Silt %**: $r = +0.937$ ($p = 0.002$) $\longrightarrow$ Il limo è il driver primario dello strozzamento dei colli porosi.
   * $\log_{10}(D_{EH})$ vs **Clay %**: $r = +0.932$ ($p = 0.002$) $\longrightarrow$ L'argilla aumenta la tortuosità geometrica.

2. **Step 05.2 — Relazione Principe Unificata vs Frazione Fine Totale (Silt % + Clay %)**:
   $$\log_{10}(D_{EH}) = 0.3120 + 0.0124 \cdot (\% \text{Fines})$$
   $$D_{EH} = 2.05 \cdot 10^{0.0124 \cdot (\% \text{Fines})} \quad (r = +0.956,\ p = 0.001)$$

---

## 5. RISTRUTTURAZIONE FASE 06: IPOTESI DI LAVORO E SVILUPPO VERSO LA CAMPAGNA `02CARL`

### 5.1 Definizione Integrale della GAP Area
La discrepanza energetica complessiva tra desaturazione idraulica e risposta geoelettrica è calcolata come:

$$\Delta_{\mathrm{GAP}} = \int_{\log_{10} h_{\min}}^{\log_{10} h_{\max}} \left[ S_e(\log_{10} h) - \sigma_{\mathrm{norm}}(\log_{10} h) \right] d(\log_{10} h)$$

Integrando su $h \in [10^{-2}, 10^3]\ \mathrm{kPa}$ ($5$ decadi di suzione):

| Campione | Tessitura USDA | Clay [%] | Fillosilicati Tot. [%] | Smectite in I/S [%] | $D_{EH} = \frac{n_A}{m_{\mathrm{VG}}}$ | $\mathbf{\Delta_{\mathrm{GAP}}\ [decadi]}$ | Diagnostica di Regime |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`Sand_R`** | Sand | 0.0 | 0.0 | 0% | 2.09 | **0.048** | *(a) Minimal GAP (Synchronous)* |
| **`ML7`** | Sandy Loam | 18.2 | 24.0 | 69% | 9.97 | **0.630** | *(b) Reduced GAP (Sand Mitigation)* |
| **`ML4`** | Loam | 24.7 | 26.5 | 70% | 12.33 | **0.492** | *Intermediate Loam GAP* |
| **`ML8`** | Silt Loam | 22.8 | 26.0 | 70% | 21.75 | **0.735** | *Active Silt GAP* |
| **`ML1`** | Silt Loam | 26.2 | 34.5 | 68% | 26.63 | **0.776** | *High Tortuosity GAP* |
| **`ML10`** | Silty Clay Loam | 33.0 | 65.5 | 75% | 26.48 | **1.018** | *(d) Buffered GAP (Smectite EDL)* |
| **`ML9`** | Silt Loam | 26.2 | 31.0 | 72% | 36.14 | **1.234** | *(c) Maximum GAP (Silt Pinch-off)* |

---

### 5.2 L'Ipotesi di Lavoro Fondante: Il "Buffering" delle Argille Espandibili
* **$D_{EH}$** esprime come i parametri esponenti elettro-idraulici accoppiati scalano rispetto alla **sola granulometria** (scheletro sabbioso vs matrice fine).
* La **$\text{GAP area}$** è invece modulata dalla **presenza di minerali argillosi espandibili (interstratificati Illite/Smectite)** che forniscono conduzione superficiale lungo il Doppio Strato Elettrico (EDL buffering), sostenendo la conducibilità elettrica e impedendole di precipitare bruscamente.
* **Dimostrazione (ML10 vs ML9)**: ML10, pur avendo più argilla granulometrica ($33.0\%$) e più del doppio di fillosilicati ($65.5\%$) rispetto a ML9 ($26.2\%$ argilla, $31.0\%$ fillosilicati), presenta una $\text{GAP area}$ sensibilmente **più compressa ($\Delta_{\mathrm{GAP}} = 1.018$ vs $1.234\ \text{decadi}$)** grazie all'azione tampone dell'EDL smectitico.

---

### 5.3 Il Layout Master della Fase 06
Pannello composito master:
* **Centro**: Diagramma ternario USDA con i 4 campioni chiave (`Sand_R`, `ML7`, `ML9`, `ML10`).
* **4 Riquadri Angolari**: I 4 grafici normalizzati $[0, 1]$ con campitura `GAP area`:
  * (a) `Clean Sand (Sand_R)` | $\Delta = 0.05$ | *Minimal GAP*;
  * (b) `Sandy Loam (ML7)` | $\Delta = 0.63$ | *Reduced GAP (Sand Mitigation)*;
  * (c) `Silt Loam (ML9)` | $\Delta = 1.23$ | *Maximum GAP (Silt Effect)*;
  * (d) `Silty Clay Loam (ML10)` | $\Delta = 1.02$ | *Buffered GAP (EDL Effect)*.

---

### 5.4 Sviluppo Futuro verso la Campagna `02Carl`
La quantificazione esplicita di questa seconda tematica (conduzione di superficie, Waxman-Smits / Revil e blocco sperimentale di $\mathrm{EC}_{\mathrm{res}}$ post-cavitazione) sarà l'oggetto fondante del successivo articolo scientifico basato sulla campagna `Hyprop_geotom_02Carl`.
