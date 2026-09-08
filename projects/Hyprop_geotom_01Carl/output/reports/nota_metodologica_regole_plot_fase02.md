# NOTA METODOLOGICA: REGOLE DI VALIDAZIONE E FORMATTAZIONE GRAFICA FASE 02
## Modello Accoppiato van Genuchten – Archie nello Spazio Fisico $[\text{mS/m}]$

**Data di Approvazione**: Settembre 2026  
**Autori**: Pair Programming Team (Ricercatore & Antigravity)  
**Ambito**: Fase 02 — Modello Accoppiato Fisico-Petrofisico (van Genuchten, 1980 + Archie, 1942)  
**Campioni Analizzati**: 10 carote (`Sand_R`, `ML9`, `ML1`, `ML3`, `ML4`, `ML5`, `ML6`, `ML7`, `ML8`, `ML10`)

---

## 1. Fondamento Fisico e Formulazione Analitica

A differenza della baseline puramente empirica di Boyd et al. (2024) (Fase 01), nella **Fase 02** la traiettoria di svuotamento geoelettrico viene ancorata alla fisica dello svuotamento idraulico dei pori attraverso l'equazione accoppiata nello spazio fisico $[\text{mS/m}]$:

$$\mathrm{EC}(h) = \mathrm{EC}_{\mathrm{res}} + (\mathrm{EC}_{\mathrm{sat}} - \mathrm{EC}_{\mathrm{res}}) \cdot S_e(h)^{n_A} = \mathrm{EC}_{\mathrm{res}} + (\mathrm{EC}_{\mathrm{sat}} - \mathrm{EC}_{\mathrm{res}}) \cdot \left[1 + (\alpha_{\mathrm{VG}} \cdot h)^{n_{\mathrm{VG}}}\right]^{-m_{\mathrm{VG}} \cdot n_A}$$

dove:
- **Vincolo Rigido Idraulico ("Hard Lock")**: $\alpha_{\mathrm{VG}}$, $n_{\mathrm{VG}}$ e $m_{\mathrm{VG}} = 1 - 1/n_{\mathrm{VG}}$ sono **fissati rigidamente** dai parametri della curva di ritenzione idrica HYPROP2 calibrata in laboratorio;
- **Suzione di Entrata dell'Aria Idraulica**: $\psi_{\mathrm{AEPs}} = 1/\alpha_{\mathrm{VG}}$ costituisce la spalla teorica rigida oltre la quale il modello teorico comincia obbligatoriamente a decadere;
- **Parametri Liberi Ottimizzati**:
  1. $n_A$: esponente di saturazione apparente di Archie (vincolato al limite fisico $n_A \ge 1.00$ per evitare pendenze non fisiche);
  2. $\mathrm{EC}_{\mathrm{sat}}$: conducibilità apparente a piena saturazione, vincolata con un guinzaglio stretto $[0.95, 1.10]$ rispetto al plateau pre-desaturazione misurato;
  3. $\mathrm{EC}_{\mathrm{res}}$: conducibilità residua ancorata al pavimento di fine essiccamento (o vincolata sul minimo asintotico).

---

## 2. Le Regole di Validazione e Diagnostica Concordate

### Regola 1: Quantificazione del Ritardo del Plateau ($\Lambda_{\mathrm{delay}} > 2.50$)
Il rapporto adimensionale di sfasamento microstrutturale tra desaturazione geoelettrica e svuotamento idraulico è definito come:
$$\Lambda_{\mathrm{delay}} = \frac{\psi_{\mathrm{EC}}}{\psi_{\mathrm{AEPs}}} = \frac{\alpha_{\mathrm{VG}}}{\alpha_{\mathrm{EC}}}$$
dove $\psi_{\mathrm{EC}} = 1/\alpha_{\mathrm{EC}}$ proviene dal fit empirico non vincolato di Boyd (Fase 01).
- **Soglia di allerta convalidata**: $\mathbf{\Lambda_{\mathrm{delay}} > 2.50}$.  
  Se la caduta di conducibilità avviene a suzioni oltre 2.5 volte superiori a $\psi_{\mathrm{AEPs}}$, la conducibilità permane piatta sul plateau mentre i pori idraulici sono già svuotati.

### Regola 2: Standard del Warning Box
Quando si verifica un ritardo significativo, sul grafico viene impresso il Warning Box con formulazione puramente geometrico-matematica (senza speculazioni chimiche premature):
$$\mathbf{\triangle\ Warning:}\ \text{Extended Plateau Exceeds}\ \mathit{AEP_s}\ (\Lambda_{\mathrm{delay}} = \dots > 2.50)$$

### Regola 3: Gestione del Plot 2 (Lower Layer Validated qp & Mean)
1. Vengono plottati tutti i qp validati della parte inferiore (L3–L4) con le relative curve accoppiate;
2. Viene calcolata e tracciata la media aritmetica sperimentale pointwise (punti cerchiati in rosso scuro);
3. Viene calcolato e plottato il fit accoppiato della media (linea rossa continua spessa, $n_A, R^2$);
4. **Se la media deriva da qp che eccedono $\Lambda_{\mathrm{delay}} > 2.50$**, viene impresso il Warning Box sul grafico.

### Regola 4: Gestione del Plot 3 (Best Fit Lower Layer) e "Scenario B"
1. **Criterio Primario**: Tra i qp del layer inferiore, si considerano candidati solo quelli la cui caduta è in linea con l'idraulica ($\Lambda_{\mathrm{delay}} \le 2.50$);
2. **Criterio Secondario**: Tra i candidati ammissibili, si seleziona il qp con il massimo $R^2$;
3. **Scenario B (Tutti i qp inferiori con plateau esteso)**:  
   Se in un campione **tutti** i qp del fondo presentano $\Lambda_{\mathrm{delay}} > 2.50$ (es. `ML5` con $\Lambda = 9.95$ e `ML3` con $\Lambda = 7.92$), **il Plot 3 NON viene generato**.  
   *Razionale scientifico*: Non è ammissibile forzare una parametrizzazione accoppiata rigida laddove l'ipotesi fisica di accoppiamento all'$\mathit{AEP_s}$ è smentita dall'intero volume inferiore del suolo.

### Regola 5: Warning Basso Range Dinamico
Nei provini con escursione limitata di conducibilità ($DR = \text{EC}_{\text{sat}} / \text{EC}_{\text{res}} < 1.30$, come su `ML6` dove $DR = 1.17$), viene stampato il box:
$$\mathbf{\triangle\ Warning:}\ \text{Low Dynamic Range}\ (DR = 1.17 < 1.30)$$

### Regola 6: Benchmark Universale dell'$\mathit{AEP_s}$
Su tutti i grafici (Plot 1, Plot 2 e Plot 3) viene **sempre** tracciata la linea verticale rossa tratteggiata in corrispondenza dell'ascissa $\psi_{\mathrm{AEPs}} = 1/\alpha_{\mathrm{VG}}$, con etichetta adiacente in corsivo $\mathit{AEP_s}$.

---

## 3. Tabella Sinottica di Validazione Fase 02 su Tutto il Dataset

File salvato in: [`summary_fase02_tre_plot_campioni.csv`](file:///projects/Hyprop_geotom_01Carl/output/tables/summary_fase02_tre_plot_campioni.csv).

| Campione | Classe USDA | $\alpha_{\mathrm{VG}}$ [$\text{kPa}^{-1}$] | $n_{\mathrm{VG}}$ | $\psi_{\mathrm{AEPs}}$ [kPa] | $\Lambda_{\text{delay}}$ Max Lower | Plot 1 | Plot 2 (Media) | Plot 3 (Best Fit) | Best qp | $n_A$ Best | $R^2$ Best | Stato Plot 3 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`Sand_R`** | Sabbia | 0.1825 | 8.395 | 5.48 | **0.90** | Generato | Generato | Generato | **`qp4`** | 1.726 | **0.8873** | Canonico sincrono |
| **`ML9`** | Limo franco | 0.3732 | 1.138 | 2.68 | **1.30** | Generato | Generato | Generato | **`qp5`** | 3.185 | **0.9894** | Canonico sincrono |
| **`ML1`** | Limo franco | 0.2539 | 1.120 | 3.94 | **2.23** | Generato | Generato | Generato | **`qp5`** | 2.852 | **0.9661** | In linea ($\Lambda \le 2.50$) |
| **`ML3`** | Franco argilloso | 0.3783 | 1.111 | 2.64 | **7.92** | Generato | Generato ($\triangle$) | **OMESSO** | *Nessuno* | — | — | **Scenario B** (Tutti $\Lambda > 2.5$) |
| **`ML4`** | Franco | 0.6434 | 1.163 | 1.55 | **12.67** | Generato | Generato ($\triangle$) | Generato | **`qp5`** | 1.001 | **0.9702** | Selezionato qp in linea |
| **`ML5`** | Limo f.-argilloso | 0.0524 | 1.239 | 19.08 | **9.95** | Generato | Generato ($\triangle$) | **OMESSO** | *Nessuno* | — | — | **Scenario B** (Tutti $\Lambda > 2.5$) |
| **`ML6`** | Argilla | 0.0643 | 1.236 | 15.54 | **0.91** | Generato | Generato ($\triangle$) | Generato | **`qp6`** | 2.691 | **0.8806** | Warning: Low DR |
| **`ML7`** | Franco | 0.7566 | 1.244 | 1.32 | **2.87** | Generato | Generato ($\triangle$) | Generato | **`qp6`** | 1.001 | **0.9911** | Selezionato qp in linea |
| **`ML8`** | Limo franco | 0.8555 | 1.117 | 1.17 | **0.30** | Generato | Generato | Generato | **`qp5`** | 1.757 | **0.9794** | Desaturazione anticipata |
| **`ML10`** | Limo f.-argilloso | 0.2356 | 1.159 | 4.25 | **77.15** | Generato | Generato ($\triangle$) | Generato | **`qp5`** | 3.632 | **0.8902** | Selezionato **`qp5`** (in linea) |

---

## 4. Totale Figure Prodotte per la Fase 02

- **Plot Tipo 1 (Tutti i qp validati)**: 10 figure (100% del dataset).
- **Plot Tipo 2 (Layer inferiore & Media con diagnostica)**: 10 figure (100% del dataset; warning su `ML3`, `ML4`, `ML5`, `ML7`, `ML10`, `ML6`).
- **Plot Tipo 3 (Best fit lower layer)**: **8 figure** (generato sui soli 8 campioni dotati di almeno un qp in linea con l'idraulica; **omesso per `ML3` e `ML5`** per rigore metodologico).
- **Totale complessivo figure Fase 02**: **28 file PNG** ad alta risoluzione (300 DPI).
