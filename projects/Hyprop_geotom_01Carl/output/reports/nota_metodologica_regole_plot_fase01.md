# NOTA METODOLOGICA: REGOLE OPERATIVE PER I TRE TIPI DI PLOT (FASE 01 - BOYD ET AL., 2024)

**Progetto**: Studio Idrogeofisico Avanzato (HYPROP2 + GeoTom-16)  
**Ambito**: Fase 01 — Formulazione Empirica Disaccoppiata di Boyd et al. (2024)  
**Destinatari**: Gruppo di Ricerca e Manoscritto per Pubblicazione (Q1)  
**Data di Formalizzazione**: Settembre 2026  

---

## 1. Premessa e Nomenclatura Rigorosa

Nello studio della desaturazione multifase monitorata mediante tomografia di resistività elettrica speditiva ad anelli coassiali (GeoTom-16), ogni singolo canale di misura orizzontale non costituisce un elettrodo o un quadripolo isolato, bensì una **coppia quadrupolare** (*quadrupole pair*, abbreviata tassativamente come **qp**). 

Ciascun valore registrato deriva dall'inversione combinata e dalla verifica di reciprocità ($\epsilon_{\text{rec}} \le 2\%$) tra configurazioni dirette e coniugate a parità di quota $z$ e orientazione azimutale $\theta$.

---

## 2. Formulazione Analitica di Boyd et al. (2024)

Il decadimento empirico della conducibilità elettrica apparente $\sigma_{\text{app}}(h)$ [mS/m] in funzione della suzione matriciale $h$ [kPa] è descritto dall'equazione unimodale a quattro parametri:

$$\sigma_{\text{app}}(h) = \text{EC}_{\text{res}} + \left(\text{EC}_{\text{sat}} - \text{EC}_{\text{res}}\right) \cdot \left[ 1 + \left(\alpha_{\text{EC}} \cdot h\right)^{n_{\text{EC}}} \right]^{-m_{\text{EC}}}$$

con il vincolo di Mualem (1976):
$$m_{\text{EC}} = 1 - \frac{1}{n_{\text{EC}}}$$

- **$\alpha_{\text{EC}}$ [$\text{kPa}^{-1}$]**: inverso della suzione di ingresso aria elettrica ($\psi_{\text{EC}} = 1/\alpha_{\text{EC}}$);
- **$n_{\text{EC}}$ [-]**: esponente di pendenza empirica della disconnessione dei cammini ionici conduttivi;
- **$\text{EC}_{\text{sat}}$ [mS/m]**: conducibilità asintotica a piena saturazione della matrice porosa;
- **$\text{EC}_{\text{res}}$ [mS/m]**: conducibilità residua di interfaccia (conduzione di superficie del doppio strato elettrico EDL).

A differenza del modello accoppiato van Genuchten – Archie (Fase 02), in questa fase preliminare $\alpha_{\text{EC}}$ ed $n_{\text{EC}}$ sono lasciati **completamente liberi e indipendenti dai parametri idraulici** ($\alpha_{\text{VG}}, n_{\text{VG}}$), fornendo la baseline descrittiva pura del segnale geoelettrico.

---

## 3. Regole Operative per i Tre Tipi di Plot

Per ogni campione del dataset ($N = 10$, da `ML1` a `ML10` e `Sand_R`) vengono generati sistematicamente tre grafici standardizzati a 300 DPI:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ARCHITETTURA GRAFICA FASE 01                       │
├──────────────────────────┬──────────────────────────┬───────────────────────┤
│    PLOT 1 (Tipo 1.1)     │    PLOT 2 (Tipo 1.2)     │   PLOT 3 (Tipo 1.3)   │
│  Validated qp (Overall)  │ Lower Validated qp & Mean│  Best Fit Lower Layer │
├──────────────────────────┼──────────────────────────┼───────────────────────┤
│ Tutti i qp validati      │ Solo qp basali (L3-L4)   │ Singolo qp inferiore  │
│ lungo la colonna (L1-L4) │ validati + Fit della     │ con massimo R²        │
│ con decluttering         │ loro media analitica     │ + asintoti ECsat/res  │
└──────────────────────────┴──────────────────────────┴───────────────────────┘
```

---

### 3.1 Regola per il Plot 1: `Validated qp`

**Titolo Standard**: `{Sample} empirical model (Boyd et al., 2024) | Validated qp`

#### Criteri di Validazione e Filtraggio:
Un qp viene considerato **VALIDATO** e inserito nel grafico se e solo se soddisfa simultaneamente quattro requisiti fisici e statistici:
1. **Stato di Ottimizzazione**: `Status == 'VALID'` (convergenza dell'algoritmo non-lineare di Levenberg-Marquardt entro i bound fisici).
2. **Monotonicità Idrogeofisica**: Coefficiente di correlazione per ranghi di Spearman $\rho_s(h, \sigma_{\text{app}}) \le -0.60$. Quadripoli con pendenza invertita o incoerente ($d\sigma/dh > 0$, es. `qp1` in `ML3` o `qp2` in `ML4`) vengono rigettati.
3. **Qualità del Fitting**: Coefficiente di determinazione $R^2_{\text{Boyd}} \ge 0.60$.
4. **Filtraggio dell'Anisotropia Azimutale e Artefatti 2D**:
   Nelle celle GeoTom-16, i livelli L2 e L3 dispongono di coppie ortogonali ($0^\circ$ vs $90^\circ$). Qualora una delle due orientazioni evidenzi distacco di contatto dagli aghi perimetrali, spikes di condensa o appiattimento anomalo (es. `qp3` e `qp6` a $90^\circ$ in `ML9`, `qp6` in `ML1`), essa viene esclusa, ritenendo rappresentativa la corrispondente orientazione a $0^\circ$.

#### Standard di Layout:
- **Punti e Linee**: Ciascun qp validato presenta i suoi dati scatter e la curva continua di modello con palette semantica differenziata per layer (L1: arancio, L2: indaco/rosa, L3: verde, L4: blu).
- **Legenda Compatta (`HandlerTuple`)**: Punto e linea sono fusi in un'unica chiave grafica per risparmiare spazio verticale.
- **Etichettatura dei Parametri a Capo**: 
  $$(L\# - \text{qp}X)$$
  $$(\alpha_{\mathrm{EC}} = \dots\ \mathrm{kPa^{-1}},\ n_{\mathrm{EC}} = \dots,\ R^2 = \dots)$$
  con pedici espliciti $\alpha_{\mathrm{EC}}$ e $n_{\mathrm{EC}}$.

---

### 3.2 Regola per il Plot 2: `Lower layer validated qp & mean`

**Titolo Standard**: `{Sample} empirical model (Boyd et al., 2024) | Lower layer validated qp & mean`

#### Motivazione Fisica del Benchmark Basale:
La letteratura idrogeofisica e la geometria della cella HYPROP (flusso evaporativo libero sommitale a $z = 5.0\text{ cm}$, fondo sigillato a $z = 0.0\text{ cm}$) impongono che i livelli inferiori (Layer 3 a $z = 2.0\text{ cm}$ e Layer 4 a $z = 1.0\text{ cm}$) costituiscano il benchmark rappresentativo della matrice indisturbata di versante. Essi sono adiacenti alla ceramica del tensiometro inferiore ($z_{\text{low}} = 1.25\text{ cm}$) e beneficiano del confinamento meccanico della piastra basale in ABS, che impedisce il ritiro volumetrico e le fessurazioni da essiccamento (*desiccation cracking*).

#### Criteri di Calcolo e Fitting:
1. **Selezione dei soli qp basali validati**: Vengono estratti i qp validati appartenenti a Layer 3 (`qp4`, `qp6`) e Layer 4 (`qp5`).
2. **Calcolo della Serie Media**: Si calcola la media punto a punto della conducibilità apparente dei soli qp basali validati:
   $$\overline{\sigma}_{\text{app, lower}}(h_i) = \frac{1}{K}\sum_{k=1}^K \sigma_{\text{app}, k}(h_i)$$
3. **Fitting Non-Lineare sulla Media**:
   - Si applica il modello di Boyd (2024) sulla serie media;
   - $\text{EC}_{\text{sat}}$ è vincolata mediante *bounded leash* $[0.95, 1.10] \cdot \overline{\text{EC}}_{\text{pre-AEP}}$;
   - $\text{EC}_{\text{res}}$ è ancorata al limite fisico del campione (es. Step 147 a $0.446\text{ mS/m}$ per `Sand_R`, o la media dei residui misurati a fine evaporazione).
4. **Rappresentazione Grafica**:
   - I singoli qp basali validati sono rappresentati con tratti sottili tratteggiati (`linewidth=1.8`, trasparenza `alpha=0.85`);
   - La media osservata è evidenziata con marcatori cerchiati in nero e la curva di fit della media è tracciata in **rosso bordeaux spesso (`linewidth=2.8`)**;
   - Se è presente un solo qp inferiore validato (es. `qp5` in `ML1` o `ML5`, `qp6` in `ML3`), il grafico riporta tale qp come *Benchmark Unico*.

---

### 3.3 Regola per il Plot 3: `Best fit lower layer`

**Titolo Standard**: `{Sample} empirical model (Boyd et al., 2024) | Best fit lower layer ({best_qp})`

#### Criterio di Selezione e Diagnostica Avanzata:
- Tra i soli qp validati del layer inferiore (L3–L4), si individua il qp che esibisce il massimo coefficiente di determinazione ($R^2_{\text{Boyd}}$):
  $$\text{qp}_{\text{best}} = \arg\max_{\text{qp} \in \text{Lower Validated}} R^2_{\text{Boyd}}(\text{qp})$$
- **Standard di Layout**:
  - Dati Osservati: Punti neri semitrasparenti (`color='#222222', alpha=0.75`).
  - Curva di Best Fit: Linea continua spessa viola/indaco (`linewidth=2.6`).
  - Asintoti Orizzontali Puntinati: $\text{EC}_{\text{sat}}$ e $\text{EC}_{\text{res}}$ (linee ambra/marrone).
  - Parametri del fit disposti a capo:
    $$\text{Boyd (2024) fit} \quad (\alpha_{\mathrm{EC}} = \dots\ \mathrm{kPa^{-1}},\ n_{\mathrm{EC}} = \dots,\ R^2 = \dots)$$
  - **Linea di Suzione di Entrata dell'Aria Idraulica ($\psi_{\mathrm{AEPs}}$)**:
    Nei campioni che manifestano un ritardo anomalo del decadimento geoelettrico con estensione del plateau oltre la soglia di desaturazione dei macropori ($\psi_{\mathrm{EC}} = 1/\alpha_{\mathrm{EC}} > 1.5 \cdot \psi_{\mathrm{AEPs}}$), viene tracciata una **linea verticale tratteggiata rossa** (`linestyle='--'`, `color='red'`) in corrispondenza del valore idraulico $\psi_{\mathrm{AEPs}} = 1/\alpha_{\mathrm{VG}}$ (misurato con HYPROP), affiancata dall'etichetta in corsivo $\mathit{AEP_s}$ in rosso.
  - **Box di Allerta per Basso Range Dinamico**:
    Nei provini in cui il rapporto di variazione della conducibilità nel layer inferiore è insufficiente ($DR = \text{EC}_{\text{sat}} / \text{EC}_{\text{res}} < 1.30$, come su ML6 dove $DR = 1.17$), viene impresso nel quadrante inferiore sinistro un box di allerta visibile:
    $$\mathbf{\triangle\ Warning:}\ \text{Low Dynamic Range}\ (DR < 1.30)$$

---

## 4. Tabella Sinottica di Validazione su Tutto il Dataset

La seguente tabella riassume i risultati della batch generation per tutti i 10 provini analizzati, evidenziando il ritardo del plateau $\Lambda_{\text{delay}} = \psi_{\mathrm{EC}} / \psi_{\mathrm{AEPs}}$ e la presenza di allerta per basso range dinamico:

| Campione | Classe USDA | qp Validati Totali | qp Inferiori Validati | Best qp (Plot 3) | $R^2_{\text{Boyd}}$ | $\alpha_{\mathrm{EC}}$ [$\text{kPa}^{-1}$] | $n_{\mathrm{EC}}$ | $\text{EC}_{\text{sat}}$ [mS/m] | $\text{EC}_{\text{res}}$ [mS/m] | $\psi_{\mathrm{AEPs}}$ [kPa] | $\psi_{\mathrm{EC}}$ [kPa] | $\Lambda_{\text{delay}}$ | Note Diagnostiche |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`Sand_R`** | Sabbia | 6/6 | `qp4, qp6, qp5` | **`qp4`** | **0.8964** | 0.2028 | 7.857 | 12.12 | 0.450 | 5.48 | 4.93 | 0.90 | Sincrono |
| **`ML9`** | Limo franco | 4/6 | `qp4, qp5` | **`qp5`** | **0.9971** | 0.2870 | 1.579 | 24.61 | 1.246 | 2.68 | 3.48 | 1.30 | Sincrono |
| **`ML1`** | Limo franco | 2/6 | `qp5` | **`qp5`** | **0.9820** | 0.1140 | 1.428 | 59.64 | 0.000 | 3.94 | 8.77 | 2.23 | Plateau esteso |
| **`ML3`** | Franco argilloso | 3/6 | `qp6` | **`qp6`** | **0.9940** | 0.0478 | 1.552 | 57.95 | 26.351 | 2.64 | 20.91 | 7.92 | Plateau esteso |
| **`ML4`** | Franco | 4/6 | `qp4, qp6, qp5` | **`qp5`** | **0.9890** | 0.2835 | 1.104 | 20.38 | 0.000 | 1.55 | 3.53 | 2.28 | Plateau esteso |
| **`ML5`** | Limo f.-argilloso | 2/6 | `qp5` | **`qp5`** | **0.9763** | 0.0053 | 7.734 | 92.52 | 5.689 | 19.08 | 189.75 | 9.95 | Plateau esteso |
| **`ML6`** | Argilla | 3/6 | `qp4, qp6` | **`qp6`** | **0.8827** | 0.0708 | 1.639 | 115.28 | 103.153 | 15.54 | 14.11 | 0.91 | Warning: Low DR |
| **`ML7`** | Franco | 6/6 | `qp4, qp6, qp5` | **`qp5`** | **0.9996** | 0.3603 | 1.421 | 19.38 | 1.661 | 1.32 | 2.78 | 2.10 | Plateau esteso |
| **`ML8`** | Limo franco | 6/6 | `qp4, qp6, qp5` | **`qp5`** | **0.9821** | 2.8280 | 1.126 | 20.58 | 4.765 | 1.17 | 0.35 | 0.30 | Desat. anticipata |
| **`ML10`** | Limo f.-argilloso | 6/6 | `qp4, qp6, qp5` | **`qp6`** | **0.9565** | 0.0031 | 7.659 | 87.32 | 23.798 | 4.25 | 327.87 | 77.15 | Plateau esteso |

---

## 5. Conclusioni Metodologiche per il Manoscritto

1. **Robustezza dell'Isolamento del Benchmark**: 
   In tutti i 10 campioni, il best fit del layer inferiore si attesta su livelli di eccellenza analitica ($R^2 \ge 0.88 - 1.00$). L'adozione del layer inferiore sigillato (L3 o L4) isola il segnale reale della matrice da qualsiasi disturbo evaporativo corticale.
2. **Diagnostica dell'Anisotropia Confermata**:
   I campioni sedimentari isotropi (`Sand_R`, `ML7`, `ML8`, `ML10`) presentano coerenza galvanica totale su tutti i 6 qp. Nei campioni con distacco elettrodico a $90^\circ$ (`ML9`, `ML1`), il filtraggio dell'azimuth anomalo ripristina la perfetta monotonicità dei rimanenti qp a $0^\circ$.
3. **Efficacia Descrittiva di Boyd (2024) e Rilevazione del Plateau Delay**:
   La formulazione di Boyd si conferma indispensabile per mappare la traiettoria empirica di svuotamento elettrico, ponendo le basi quantitative oggettive per calcolare il *Plateau Delay Index* $\Lambda_{\text{delay}} = \psi_{\mathrm{EC}}/\psi_{\mathrm{AEPs}}$. L'inserimento della linea verticale $\mathit{AEP_s}$ nei grafici dimostra graficamente come nei suoli a matrice fine (es. ML5, ML10) la conduzione superficiale mantenga la conducibilità elevata ben oltre la suzione di entrata dell'aria idraulica, costringendo il modello di Boyd non vincolato ad arrampicarsi su parametri $n_{\mathrm{EC}} \approx 7.7$ e $\psi_{\mathrm{EC}} > 180\text{ kPa}$.
