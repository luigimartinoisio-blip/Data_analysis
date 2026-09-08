# NOTA METODOLOGICA: REGOLE DI VALIDAZIONE E FORMATTAZIONE GRAFICA FASE 03
## Confronto Normalizzato $[0, 1]$ e Master Multipannel ($2 \times 4$) sui Campioni Idonei

**Data di Approvazione**: Settembre 2026  
**Autori**: Pair Programming Team (Ricercatore & Antigravity)  
**Ambito**: Fase 03 — Confronto Petrofisico Normalizzato $[0, 1]$ ($S_e(h)$ vs Boyd 2024 vs Modello Accoppiato vG–Archie)  
**Campioni Selezionati**: 8 campioni idonei (`Sand_R`, `ML9`, `ML1`, `ML4`, `ML6`, `ML7`, `ML8`, `ML10`)  
**Campioni Esclusi**: `ML3` e `ML5` (Opzione A convalidata per violazione dei presupposti fisici del modello accoppiato)

---

## 1. Fondamento Matematico e Spazio Normalizzato $[0, 1]$

Nello spazio adimensionale $[0, 1]$, la curva di ritenzione idraulica funge da benchmark teorico fondamentale di riferimento per la disconnessione della fase fluida conduttiva:

1. **Saturazione Efficace Idraulica (van Genuchten, 1980)**:
   $$S_e(h) = \left[ 1 + (\alpha_{\mathrm{VG}} \cdot h)^{n_{\mathrm{VG}}} \right]^{-m_{\mathrm{VG}}}, \quad m_{\mathrm{VG}} = 1 - \frac{1}{n_{\mathrm{VG}}}$$
   Parametri $(\alpha_{\mathrm{VG}}, n_{\mathrm{VG}})$ rigidamente ancorati alle curve HYPROP2 di laboratorio.

2. **Modello Empirico Geoelettrico Normalizzato (Boyd et al., 2024)**:
   $$\sigma_{\mathrm{norm, Boyd}}(h) = \left[ 1 + (\alpha_{\mathrm{EC}} \cdot h)^{n_{\mathrm{EC}}} \right]^{-m_{\mathrm{EC}}}, \quad m_{\mathrm{EC}} = 1 - \frac{1}{n_{\mathrm{EC}}}$$
   Fornisce la traiettoria empirica libera non vincolata all'aria, determinando la suzione di air-entry geoelettrico $\psi_{\mathrm{EC}} = 1/\alpha_{\mathrm{EC}}$.

3. **Modello Accoppiato van Genuchten – Archie Normalizzato**:
   $$\sigma_{\mathrm{norm, Archie}}(h) = S_e(h)^{n_A} = \left[ 1 + (\alpha_{\mathrm{VG}} \cdot h)^{n_{\mathrm{VG}}} \right]^{-m_{\mathrm{VG}} \cdot n_A}$$
   Vincolato rigidamente alla spalla di air-entry idraulico $\psi_{\mathrm{AEPs}} = 1/\alpha_{\mathrm{VG}}$, con unico grado di libertà $n_A$ (esponente di saturazione apparente).

4. **Dati Sperimentali Normalizzati**:
   $$\sigma_{\mathrm{norm}}(h) = \frac{\sigma_{\mathrm{app}}(h) - \sigma_{\mathrm{res}}}{\sigma_{\mathrm{sat}} - \sigma_{\mathrm{res}}}$$

5. **GAP area (Area Ombreggiata)**:
   L'area compresa tra la curva idraulica $S_e(h)$ e la curva accoppiata di Archie $\sigma_{\mathrm{norm, Archie}}(h)$ quantifica geometricamente il disaccoppiamento idroelettrico ($\Delta(h) = S_e(h) - S_e(h)^{n_A} \ge 0$).

---

## 2. Decisioni Metodologiche e Regole di Filtraggio Convalidate

### 2.1 Convalida dell'Opzione A (Esclusione di ML5 e ML3)
- **Motivazione Fisica per ML5**: Mostra un ritardo colossale nel plateau geoelettrico ($\Lambda_{\mathrm{delay}} = 9.95 \gg 2.50$) e forte attività elettrochimica di superficie (EDL su smectite), violando il postulato di Archie secondo cui la conducibilità deve decadere sincronicamente o più velocemente rispetto all'acqua libera.
- **Motivazione Fisica per ML3**: Nei livelli inferiori presenta unicamente il quadripolo `qp6` validato, il quale esibisce un ritardo sistematico $\Lambda_{\mathrm{delay}} = 7.92 > 2.50$ (classificato come *Scenario B* in Fase 02).
- **Esito**: Entrambi i provini non sono fisicamente parametrizzabili mediante un accoppiamento rigido idraulico-elettrico e vengono esclusi dalla calibrazione comparativa di Fase 03, focalizzando l'analisi sugli **8 campioni fisicamente consistenti**.

### 2.2 Trattamento di Speciale Rigore per ML10: Selezione Esclusiva di `qp5`
- La media geometrica/aritmetica del lower layer di ML10 comprenderebbe `qp6` (Layer 3), che soffre di un ritardo estremo ($\Lambda_{\mathrm{delay}} = 77.1$). Tracciare la media creerebbe una curva artefatta non rappresentativa.
- Viene plottato **esclusivamente il quadripolo profondo `qp5` (Layer 4, matrice indisturbata)**, che scende in piena coerenza fisica con l'$AEP_s$ ($\Lambda_{\mathrm{delay}} = 1.89 \le 2.50, R^2_{\mathrm{Archie}} = 0.890$).
- Viene impresso il Notice Box esplicativo:
  $$\mathbf{\triangle\ Notice:}\ \text{Plotted qp5 (L4, } \Lambda_{\mathrm{delay}}=1.89\text{). L3 qp6 excluded (severe } \Lambda=77.1\text{)}$$

### 2.3 Trattamento dei Livelli Inferiori per gli Altri Campioni
- **`Sand_R`, `ML9`, `ML4`, `ML6`, `ML7`, `ML8`**: Vengono plottate le medie pointwise dei quadripoli validati della parte inferiore con i rispettivi fit $n_{\mathrm{EC}}$ e $n_A$.
- **`ML1`**: Essendo validato unicamente `qp5` per la parte inferiore, viene tracciato direttamente `qp5`.

### 2.4 Mantenimento dei Warning Box di Diagnostica
- **Low Dynamic Range**: Impresso su **`ML6`** ($\mathbf{\triangle\ Warning:}\ \text{Low Dynamic Range } (DR = 1.19 < 1.30)$).
- **Extended Plateau**: Impresso su **`ML4`** ($\mathbf{\triangle\ Warning:}\ \text{Extended Plateau } (\Lambda_{\mathrm{delay}} = 3.6 > 2.50)$).

---

## 3. Tabella Parametrica Completa Fase 03 (8 Campioni Idonei)

| Pannello | Campione | Modalità Target | $\alpha_{\mathrm{VG}}$ [$\text{kPa}^{-1}$] | $n_{\mathrm{VG}}$ | $\mathit{AEP_s}$ [kPa] | $\alpha_{\mathrm{EC}}$ [$\text{kPa}^{-1}$] | $n_{\mathrm{EC}}$ | $\Lambda_{\mathrm{delay}}$ | $n_A$ | $R^2_{\mathrm{Archie}}$ | $R^2_{\mathrm{Boyd}}$ | Warning / Note |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **(a)** | **Sand_R** | Lower Mean (`qp4, qp6, qp5`) | $0.1825$ | $8.395$ | $5.48$ | $0.2049$ | $7.93$ | $0.89$ | **$1.84$** | $0.889$ | $0.894$ | Nessuno (Canonico Archie, ereditato da Fase 02) |
| **(b)** | **ML9** | Lower Mean (`qp4, qp5`) | $0.3732$ | $1.138$ | $2.68$ | $0.3370$ | $1.65$ | $1.11$ | **$4.38$** | $0.985$ | $0.993$ | Nessuno (Ottimale, ereditato da Fase 02) |
| **(c)** | **ML1** | Solo `qp5` | $0.2539$ | $1.120$ | $3.94$ | $0.1140$ | $1.43$ | $2.23$ | **$2.85$** | $0.966$ | $0.982$ | Nessuno (Transizione L4 valida) |
| **(d)** | **ML4** | Lower Mean (`qp4, qp6, qp5`) | $0.6434$ | $1.163$ | $1.55$ | $0.2392$ | $1.12$ | $2.69$ | **$1.73$** | $0.927$ | $0.987$ | $\triangle$ Warning: Extended Plateau ($\Lambda=2.7$) |
| **(e)** | **ML6** | Lower Mean (`qp4, qp6`) | $0.0643$ | $1.236$ | $15.55$ | $0.1689$ | $1.35$ | $0.38$ | **$4.49$** | $0.871$ | $0.899$ | $\triangle$ Warning: Low Dynamic Range ($DR=1.16$) |
| **(f)** | **ML7** | Lower Mean (`qp4, qp6, qp5`) | $0.7566$ | $1.244$ | $1.32$ | $0.3449$ | $1.34$ | $2.19$ | **$1.96$** | $0.945$ | $1.000$ | Nessuno (Transizione L4 valida) |
| **(g)** | **ML8** | Lower Mean (`qp4, qp6, qp5`) | $0.8555$ | $1.117$ | $1.17$ | $3.9544$ | $1.09$ | $0.22$ | **$2.28$** | $0.955$ | $0.969$ | Nessuno (Canonico Archie, ereditato da Fase 02) |
| **(h)** | **ML10** | Solo `qp5` (Layer 4) | $0.2356$ | $1.159$ | $4.24$ | $0.1244$ | $1.69$ | $1.89$ | **$3.63$** | $0.890$ | $0.899$ | $\triangle$ Notice: `qp5` plotted, `qp6` excluded ($\Lambda=77.1$) |

---

## 4. Architettura Grafica della Figura Multipannello $2 \times 4$

La figura `master_panel_fase03_2x4.png` è strutturata su due righe e quattro colonne:
- **Riga Superiore (4 pannelli)**: `(a) Sand_R` $\rightarrow$ `(b) ML9` $\rightarrow$ `(c) ML1` $\rightarrow$ `(d) ML4`
- **Riga Inferiore (4 pannelli)**: `(e) ML6` $\rightarrow$ `(f) ML7` $\rightarrow$ `(g) ML8` $\rightarrow$ `(h) ML10`
- **Legende Individuali**: Collocate costantemente nell'angolo superiore destro (`loc='upper right'`), dove le curve sono asintotiche a zero ad alte suzioni, azzerando qualsiasi rischio di collisione con le curve o con i box di allerta.
- **Warning Box**: Posizionati nell'angolo inferiore sinistro (`loc='lower left'`) con sfondo semi-trasparente e bordo arrotondato distinto.
- **Linea Universale $\mathit{AEP_s}$**: Tracciata in rosso tratteggiato a $\psi_{\mathrm{AEPs}} = 1/\alpha_{\mathrm{VG}}$ con testo in corsivo rosso su ciascuno degli 8 pannelli.
