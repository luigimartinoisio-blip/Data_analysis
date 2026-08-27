# Report Metodologico e Matematico: Costruzione del Database Idrogeofisico Integrato (GeoTom-16 & HYPROP2)

**Autore**: Laboratorio di Idrogeofisica Sperimentale  
**Data**: 27 Agosto 2026  
**File Output**: `projects/Hyprop_geotom_01Carl/data/processed/tabelle_campioni/`  

---

## 1. Obiettivo e Quadro Sperimentale

Il presente documento descrive in modo rigoroso e dettagliato la metodologia sperimentale, la formulazione matematica e gli algoritmi adottati per la costruzione del database idrogeofisico integrato.
Il database accoppia le misure idrodinamiche di evaporazione continua (**HYPROP2**, METER Group) con le misure di tomografia di resistività elettrica 3D in cella cilindrica (**GeoTom-16**, Geolog).

Il database comprende **10 campioni di suolo** (9 campioni di versante di frana `ML1`...`ML10` e 1 materiale sabbioso di riferimento `Sand_R`), per un totale di **1.291 time step** sincronizzati e **43 parametri chimico-fisici e idrogeofisici** validati.

---

## 2. Geometria del Portacampione Cilindrico e Posizionamento Sensori

Il provino di terreno è alloggiato in un anello cilindrico isolante in ABS con le seguenti dimensioni standard:

- **Raggio interno ($r$)**: $4.00\text{ cm}$ ($0.040\text{ m}$)
- **Altezza totale ($h$)**: $5.00\text{ cm}$ ($0.050\text{ m}$)
- **Volume nominale ($V$)**: $250.00\text{ cm}^3$ ($2.50 \times 10^{-4}\text{ m}^3$)
- **Area di base ($A$)**: $50.265\text{ cm}^2$

### 2.1 Array di 16 Elettrodi Puntiformi
I 16 elettrodi ad ago in acciaio inossidabile sono disposti sulla superficie laterale del cilindro su 4 corone circolari (anelli) a quote $z$ costanti e con spaziatura angolare di $90^\circ$:

- **Anello 1 (Upper Top)**: $z_1 = 4.0\text{ cm}$ $\rightarrow$ Elettrodi 1 ($0^\circ$), 5 ($90^\circ$), 9 ($180^\circ$), 13 ($270^\circ$)
- **Anello 2 (Upper Bottom)**: $z_2 = 3.0\text{ cm}$ $\rightarrow$ Elettrodi 2 ($0^\circ$), 6 ($90^\circ$), 10 ($180^\circ$), 14 ($270^\circ$)
- **Anello 3 (Lower Top)**: $z_3 = 2.0\text{ cm}$ $\rightarrow$ Elettrodi 3 ($0^\circ$), 7 ($90^\circ$), 11 ($180^\circ$), 15 ($270^\circ$)
- **Anello 4 (Lower Bottom)**: $z_4 = 1.0\text{ cm}$ $\rightarrow$ Elettrodi 4 ($0^\circ$), 8 ($90^\circ$), 12 ($180^\circ$), 16 ($270^\circ$)

### 2.2 Tensiometri HYPROP2
- **Tensiometro Lungo (Upper)**: inserito a quota $z_{\text{up}} = 3.75\text{ cm}$ dalla base (profondità $-1.25\text{ cm}$ dalla superficie evaporante).
- **Tensiometro Corto (Lower)**: inserito a quota $z_{\text{low}} = 1.25\text{ cm}$ dalla base (profondità $-3.75\text{ cm}$ dalla superficie evaporante).

```
                 Superficie Evaporante Superiore (z = 5.0 cm)
  +-------------------------------------------------------------+
  |  o (1)        o (5)         o (9)         o (13)   [z=4.0] | <-- Anello 1 (Upper)
  |       [=== Tensiometro Lungo / Upper (z=3.75 cm) ===]       |
  |  o (2)        o (6)         o (10)        o (14)   [z=3.0] | <-- Anello 2
  + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - + <-- Piano mediano (z = 2.5 cm)
  |  o (3)        o (7)         o (11)        o (15)   [z=2.0] | <-- Anello 3
  |       [=== Tensiometro Corto / Lower (z=1.25 cm) ===]       |
  |  o (4)        o (8)         o (12)        o (16)   [z=1.0] | <-- Anello 4 (Lower)
  +-------------------------------------------------------------+
                 Base Inferiore Sigillata (z = 0.0 cm)
```

---

## 3. Schemi dei Quadripoli e Fattori Geometrici Numerici $K$

Dalla matrice completa di misure geoelettriche sono estratti 12 quadripoli rappresentativi divisi in 4 categorie geometriche:

| Categoria | Sigla | Quadripolo Diretto $(A, B, M, N)$ | Quadripolo Reciproco $(M, N, A, B)$ | Fattore $K$ [m] | Descrizione Geometrica |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Upper** | `qp1` | $(1, 5, 13, 9)$ | $(13, 9, 1, 5)$ | $0.1580$ | Anello 1 ($z=4.0\text{ cm}, 0^\circ$) |
| **Upper** | `qp2` | $(2, 6, 14, 10)$ | $(14, 10, 2, 6)$ | $0.1580$ | Anello 2 ($z=3.0\text{ cm}, 0^\circ$) |
| **Upper** | `qp3` | $(6, 10, 2, 14)$ | $(2, 14, 6, 10)$ | $0.1580$ | Anello 2 ($z=3.0\text{ cm}, 90^\circ$) |
| **Lower** | `qp4` | $(3, 7, 15, 11)$ | $(15, 11, 3, 7)$ | $0.1580$ | Anello 3 ($z=2.0\text{ cm}, 0^\circ$) |
| **Lower** | `qp5` | $(4, 8, 16, 12)$ | $(16, 12, 4, 8)$ | $0.1580$ | Anello 4 ($z=1.0\text{ cm}, 0^\circ$) |
| **Lower** | `qp6` | $(7, 11, 3, 15)$ | $(3, 15, 7, 11)$ | $0.1580$ | Anello 3 ($z=2.0\text{ cm}, 90^\circ$) |
| **Dipole-dipole** | `qp7` | $(1, 2, 3, 4)$ | $(3, 4, 1, 2)$ | $0.1850$ | Dipolo-Dipolo Verticale ($0^\circ$) |
| **Dipole-dipole** | `qp8` | $(5, 6, 7, 8)$ | $(7, 8, 5, 6)$ | $0.1850$ | Dipolo-Dipolo Verticale ($90^\circ$) |
| **Wenner** | `W1` | $(1, 4, 2, 3)$ | - | $0.2110$ | Wenner Verticale ($0^\circ$, Esterno) |
| **Wenner** | `W3` | $(9, 12, 10, 11)$ | - | $0.2110$ | Wenner Verticale ($0^\circ$, Interno) |
| **Wenner** | `W2` | $(5, 8, 6, 7)$ | - | $0.2110$ | Wenner Verticale ($90^\circ$, Esterno) |
| **Wenner** | `W4` | $(13, 16, 14, 15)$ | - | $0.2110$ | Wenner Verticale ($90^\circ$, Interno) |

La resistenza misurata $R$ e la resistività apparente $\rho_{\text{app}}$ sono calcolate tramite la legge di Ohm generalizzata:
\[
R = \frac{|\Delta V|}{I} \quad [\Omega]
\]
\[
\rho_{\text{app}} = K \cdot R \quad [\Omega\cdot\text{m}]
\]

---

## 4. Correzione Termica a $25^\circ\text{C}$ (Hayashi, 2004)

La conducibilità elettrica della soluzione interstiziale del suolo varia significativamente con la temperatura (circa il $2.1\%\,^\circ\text{C}^{-1}$) a causa della variazione della viscosità dinamica dell'acqua.  
Tutti i valori di resistività sono stati normalizzati alla temperatura di riferimento $T_{\text{ref}} = 25.0^\circ\text{C}$ applicando rigorosamente la relazione di **Hayashi (2004)**:

\[
\rho_{25} = \rho(T) \cdot \left[1 + \alpha_T \cdot (T - 25.0)\right]
\]

dove:
- $\rho(T)$ è la resistività apparente misurata alla temperatura di prova $T$ [$\Omega\cdot\text{m}$];
- $T$ è la temperatura del provino misurata in continuo dalla sonda termometrica HYPROP2 [$^\circ\text{C}$];
- $\alpha_T = 0.0210\,^\circ\text{C}^{-1}$ è il coefficiente termico per soluzioni acquose naturali ed elettroliti interstiziali.

*Riferimento Bibliografico*:  
**Hayashi, M. (2004)**. *Temperature-electrical conductivity relation of water for environmental investigations and geophysical mapping*. Journal of Hydrology, 296(1-4), 118-128.

---

## 5. Sincronizzazione Temporale al Baricentro ERT

Ogni ciclo di misura geoelettrica GeoTom ha una durata finita $\Delta T_{\text{ERT}} \approx 9 - 16\text{ minuti}$, compresa tra il timestamp iniziale $t_{\text{inizio}}$ e quello finale $t_{\text{fine}}$.  
Per evitare sfasamenti temporali durante l'evaporazione, la sincronizzazione dei dati di peso e suzione è ancorata al **baricentro temporale**:

\[
t_{\text{baricentro}} = t_{\text{inizio}} + \frac{t_{\text{fine}} - t_{\text{inizio}}}{2}
\]

I parametri idrologici (peso netto $m(t)$ e tensioni $\psi(t)$) vengono calcolati al tempo $t_{\text{baricentro}}$ mediante interpolazione spline continua ad alta precisione.

---

## 6. Parametri Idraulici e Calcolo delle Suzioni

Dal peso netto $m(t_{\text{baricentro}})$ [g] e dal peso secco del suolo in stufa $m_{\text{dry}}$ [g]:

### 6.1 Contenuto d'Acqua Volumetrico $\theta(t)$
\[
\theta(t) = \frac{m(t) - m_{\text{dry}}}{\rho_w \cdot V} \times 100\% \quad [\text{Vol}\%]
\]
con $\rho_w = 1.00\text{ g/cm}^3$ e $V = 250.0\text{ cm}^3$.

### 6.2 Grado di Saturazione $S_r(t)$
\[
S_r(t) = \frac{\theta(t) / 100}{\phi} \quad [-]
\]
dove la porosità $\phi = 1 - \frac{\rho_d}{\rho_s}$ è calcolata dal volume e dalla densità dei granuli $\rho_s = 2.65\text{ g/cm}^3$.

### 6.3 Suzione dei Singoli Tensiometri
Le letture dei tensiometri sono espresse rigorosamente in $\text{kPa}$ ($1\text{ kPa} = 10\text{ hPa}$):
- **`Matric Suction Upper [kPa]`** ($\psi_{\text{up}}$): misura del tensiometro lungo a $z = 3.75\text{ cm}$.
- **`Matric Suction Lower [kPa]`** ($\psi_{\text{low}}$): misura del tensiometro corto a $z = 1.25\text{ cm}$.
- **`Matric Suction [kPa]`** ($\psi_{\text{mean}}$): media geometrica delle due letture:
\[
\psi_{\text{mean}}(t) = \sqrt{\psi_{\text{up}}(t) \cdot \psi_{\text{low}}(t)} \quad [\text{kPa}]
\]

---

## 7. Medie Geometriche di Resistività Corretta per Categoria

Poiché la distribuzione della resistività nei mezzi porosi eterogenei presenta una natura log-normale, per ciascuna categoria geometrica viene calcolata punto per punto la **media geometrica**:

\[
\bar{\rho}_{25,\text{geom}} = \left(\prod_{i=1}^N \rho_{25,i}\right)^{1/N} = \exp\left(\frac{1}{N}\sum_{i=1}^N \ln(\rho_{25,i})\right)
\]

1. **Upper (`rho25_geom_upper`)**:
   \[
   \bar{\rho}_{25,\text{Upper}} = \left(\rho_{25,\text{qp1}} \cdot \rho_{25,\text{qp2}} \cdot \rho_{25,\text{qp3}}\right)^{1/3}
   \]
2. **Lower (`rho25_geom_lower`)**:
   \[
   \bar{\rho}_{25,\text{Lower}} = \left(\rho_{25,\text{qp4}} \cdot \rho_{25,\text{qp5}} \cdot \rho_{25,\text{qp6}}\right)^{1/3}
   \]
3. **Dipolo-Dipolo (`rho25_geom_dipole`)**:
   \[
   \bar{\rho}_{25,\text{Dipole}} = \left(\rho_{25,\text{qp7}} \cdot \rho_{25,\text{qp8}}\right)^{1/2}
   \]
4. **Wenner (`rho25_geom_wenner`)**:
   \[
   \bar{\rho}_{25,\text{Wenner}} = \left(\rho_{25,\text{W1}} \cdot \rho_{25,\text{W2}} \cdot \rho_{25,\text{W3}} \cdot \rho_{25,\text{W4}}\right)^{1/4}
   \]

---

## 8. Controllo Qualità ed Errore di Reciprocità

Per tutti i quadripoli da `qp1` a `qp8` viene acquisita sia la misura diretta $R_{\text{dir}}$ che la misura reciproca $R_{\text{rec}}$. L'errore percentuale di reciprocità $\epsilon_{\text{rec}}$ è calcolato come:

\[
\epsilon_{\text{rec}} = 2 \cdot \frac{|R_{\text{dir}} - R_{\text{rec}}|}{R_{\text{dir}} + R_{\text{rec}}} \times 100\%
\]

La soglia di accettazione di qualità standard è $\epsilon_{\text{rec}} < 5.0\%$.

---

## 9. Struttura del Database Finale e Riepilogo Campioni

| Campione ID | Sigla Campo | Settore di Frana / Posizione | Profondità | Time Step | Range $\theta$ [%] | Range Suzione $\psi$ [kPa] |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| **`ML1`** | 5a | Steep Slope Sector ($108\text{ m}$) | Superficie ($0\text{ cm}$) | 106 | $48.2\% \rightarrow 22.1\%$ | $0.1 \rightarrow 850\text{ kPa}$ |
| **`ML3`** | 1a | Steep Slope Sector ($93\text{ m}$) | Superficie ($0\text{ cm}$) | 141 | $46.5\% \rightarrow 23.9\%$ | $0.2 \rightarrow 1240\text{ kPa}$ |
| **`ML4`** | 1b | Steep Slope Sector ($93\text{ m}$) | Profondità ($-50\text{ cm}$) | 113 | $45.1\% \rightarrow 21.8\%$ | $0.1 \rightarrow 780\text{ kPa}$ |
| **`ML5`** | 2a | Counterslope Sector ($72\text{ m}$) | Superficie ($0\text{ cm}$) | 168 | $49.4\% \rightarrow 24.3\%$ | $0.2 \rightarrow 1150\text{ kPa}$ |
| **`ML6`** | 2b | Counterslope Sector ($72\text{ m}$) | Profondità ($-50\text{ cm}$) | 125 | $47.8\% \rightarrow 23.0\%$ | $0.1 \rightarrow 920\text{ kPa}$ |
| **`ML7`** | 3a | Detachment Sector ($36\text{ m}$) | Superficie ($0\text{ cm}$) | 114 | $44.9\% \rightarrow 20.7\%$ | $0.2 \rightarrow 890\text{ kPa}$ |
| **`ML8`** | 3b | Detachment Sector ($36\text{ m}$) | Profondità ($-50\text{ cm}$) | 112 | $43.8\% \rightarrow 21.2\%$ | $0.2 \rightarrow 940\text{ kPa}$ |
| **`ML9`** | 4b | Detachment Sector ($10\text{ m}$) | Profondità ($-50\text{ cm}$) | 143 | $46.2\% \rightarrow 22.5\%$ | $0.1 \rightarrow 1050\text{ kPa}$ |
| **`ML10`** | 6a | Fuori Frana Indisturbato ($317\text{ m}$) | Superficie ($0\text{ cm}$) | 101 | $52.1\% \rightarrow 26.4\%$ | $0.1 \rightarrow 1320\text{ kPa}$ |
| **`Sand_R`**| Lab Ref | Campione di Taratura Sabbioso | Standard | 168 | $38.5\% \rightarrow 4.1\%$ | $0.05 \rightarrow 18\text{ kPa}$ |
| **TOTALE** | - | - | - | **1.291** | - | - |
