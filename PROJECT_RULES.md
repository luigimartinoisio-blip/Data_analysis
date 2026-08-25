# Regole di Progetto (PROJECT_RULES.md)

## 1. Contesto Scientifico e Obiettivi del Progetto

Questo repository è dedicato all'**analisi dati integrata per la geofisica, geoelettrica e idrogeofisica**, a supporto della ricerca e della redazione di **articoli scientifici**.

### 1.1 Obiettivo Primario
- Elaborazione, pulizia, controllo qualità e analisi di dati geoelettrici di campagna e laboratorio (misure di corrente iniettata $I$, differenze di potenziale $\Delta V$, resistività apparente $\rho_a$, fattori geometrici $K$, ecc.).
- Integrazione multivariata con dati idrologici (contenuto d'acqua volumetrico $\theta$, potenziale idrico/suzione matriciale $\psi$, conducibilità elettrica dei fluidi, temperatura, dati piezometrici e meteorologici) e geotecnici (granulometrie, carotaggi).
- Calcolo di statistiche avanzate, cross-correlazioni, calibrazione di relazioni petrofisiche (es. leggi di Archie, Waxman-Smits, modelli empirici conducibilità/resistività-umidità-suzione).

### 1.2 Regola di Esclusione Categorica (No Inversion Software)
> [!IMPORTANT]
> **I software e gli algoritmi di inversione tomografica (2D/3D ERT/IP) sono ESCLUSI dal perimetro del progetto.**  
> Salvo esplicita e straordinaria richiesta dell'utente, **non** implementare forward modeling complessi, mesh ad elementi finiti per inversione, né moduli di inversione numerica (es. PyGIMLi Inversion, Res2DInv/Res3DInv wrapper, SimPEG inversion routines).

---

## 2. Stack Tecnologico e Ambiente di Lavoro

- **Linguaggio**: Python **3.11+**
- **Gestione Ambiente e Pacchetti**: `pip` + `venv`
- **Data Science Core**: `numpy`, `scipy`, `pandas`
- **Visualizzazione**:
  - 2D: `matplotlib`, `seaborn`
  - 3D & Interattività: `plotly`, `pyvista`
  - UI / Dashboard esplorative: `streamlit` o Jupyter Widgets (se richiesto)
- **Librerie Geofisiche Open Source**: Utilizzo ammesso solo per compiti specifici e circoscritti (es. utilità geometriche o I/O), evitando dipendenze pesanti non necessarie.

---

## 3. Architettura e Organizzazione del Repository

La struttura separa rigidamente la logica computazionale riutilizzabile e testata dall'analisi esplorativa:

```text
Data_analysis/
├── src/                        # Moduli Python stabili e riutilizzabili
│   ├── io/                     # Parser per formati raw (Syscal, .dat, .csv, ecc.)
│   ├── core/                   # Matematica certificata (fattori geometrici, relazioni petrofisiche)
│   ├── hydro/                  # Modelli e conversioni idrogeofisiche / geotecniche
│   ├── stats/                  # Cross-correlazioni, fitting e statistiche
│   └── viz/                    # Template e funzioni per grafici publication-ready
├── notebooks/                  # Jupyter Notebooks per analisi esplorativa e cross-correlazioni
├── data/                       # Dati raw, intermedi ed esportazioni (strutturati)
│   ├── raw/
│   ├── processed/
│   └── external/
├── tests/                      # Suite di test pytest mirata (I/O e Core Math)
├── .cursorrules                # Regole operative rapide per l'assistente AI
├── pyproject.toml / ruff.toml  # Configurazione unificata per Ruff
├── requirements.txt            # Dipendenze pip
└── PROJECT_RULES.md            # Questo documento
```

---

## 4. Standard di Qualità del Codice

### 4.1 Stile e Linting: Esclusivamente Ruff
- **Ruff** è l'unico strumento ammesso per linting e formattazione (compatibile Black e PEP 8).
- Tutti i file di codice devono essere formattati e validati con Ruff.
- Nessuna discussione manuale su indentazione, lunghezza riga o stile: la macchina formatta in automatico.

### 4.2 Type Hinting Flessibile
- I Type Hints vanno usati **esclusivamente come documentazione nelle firme delle funzioni principali** (es. parametri essenziali e tipo restituito: `def calcola_rho_apparente(k: float, v: float, i: float) -> float:`).
- **Nessun controllo bloccante o vincolante con Mypy**: la priorità è la velocità nell'esplorazione e nella manipolazione dei DataFrame Pandas.

### 4.3 Testing con Pytest: Focus Ristretto e Non Negoziabile
La suite di test con `pytest` è concentrata **unicamente** su due pilastri critici:
1. **Parsing I/O**: Test di regressione e validazione sull'estrazione esatta delle colonne e dei metadati dai formati strumentali grezzi (es. formati Syscal/Iris Instruments, file tabulari).
2. **Matematica Core**: Test unitari rigorosi sul calcolo dei fattori geometrici $K$, conversioni di potenziale/corrente in resistività apparente e formule petrofisiche custom.
- **Nessun test** su grafici, interfacce o chiamate standard a metodi Pandas/NumPy.

---

## 5. Lingua e Convenzioni

- **Tutto in ITALIANO**: Codice, nomi di variabili esplicative, commenti, docstring, messaggi di commit, notebook, report e output per le figure scientifiche.
