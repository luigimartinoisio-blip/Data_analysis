# NOTA METODOLOGICA: REGOLE DI VALIDAZIONE E GRAFICI FASE 04

## 1. Obiettivo della Fase 04
La Fase 04 fornisce la rappresentazione grafica normalizzata pulita $[0, 1]$ delle traiettorie teoriche accoppiate idroelettriche senza punti sperimentali (decluttering totale). I valori di $n_A$ sono rigidamente ereditati dalla Fase 03 come descrittori empirici documentati, ma nei titoli e intestazioni grafiche **l'unico parametro numerico definito è il fattore geometrico $\mathcal{K}$**.

## 2. Separazione dei Gruppi (7 Campioni Validati - ML6 Eliminato)
- **Gruppo Senza Warning**: `Sand_R`, `ML7`, `ML9`, `ML8` ($\Lambda_{\mathrm{delay}} \le 2.50$, desaturazione canonica);
- **Gruppo Con Warning / Note Diagnostiche**: `ML1`, `ML4`, `ML10` (segnalazione di cavitazione precoce, plateau esteso o anisotropia);
- **Campione Escluso**: `ML6` è **eliminato dalle fasi successive alla 03** per collasso matematico della formulazione di Archie sui bordi ($n_A = 1.001$, `FAILED BOUNDS`) e dynamic range insufficiente ($\mathrm{DR} = 1.16 < 1.30$).

## 3. Tabella dei Parametri Ereditati

| Sample   | USDA            |   Sand_pct |   Silt_pct |   Clay_pct |   K_factor |    n_A | Warning_Group    | Warning_Text                                                                                                             |
|:---------|:----------------|-----------:|-----------:|-----------:|-----------:|-------:|:-----------------|:-------------------------------------------------------------------------------------------------------------------------|
| Sand_R   | Sand            |      100   |        0   |        0   |    1.13523 | 1.838  | Without Warnings | nan                                                                                                                      |
| ML7      | Sandy Loam      |       40.1 |       41.7 |       18.2 |    5.09836 | 1.956  | Without Warnings | nan                                                                                                                      |
| ML9      | Silt Loam       |       16.5 |       57.3 |       26.2 |    8.24638 | 4.384  | Without Warnings | nan                                                                                                                      |
| ML8      | Silt Loam       |        7.7 |       69.5 |       22.8 |    9.54701 | 2.277  | Without Warnings | nan                                                                                                                      |
| ML1      | Silt Loam       |       20.7 |       53.1 |       26.2 |    9.33333 | 2.8524 | With Warnings    | $\mathbf{\triangle\ Warning:}$ Early tensiometer cavitation at $h = 64\ \mathrm{kPa}$ (tail extrapolated)                |
| ML4      | Loam            |       28.4 |       46.9 |       24.7 |    7.13497 | 1.728  | With Warnings    | $\mathbf{\triangle\ Warning:}$ Extended Plateau ($\Lambda_{\mathrm{delay}} = 2.7 > 2.50$)                                |
| ML10     | Silty Clay Loam |        6.8 |       60.2 |       33   |    7.28931 | 3.6325 | With Warnings    | $\mathbf{\triangle\ Notice:}$ Plotted qp5 (L4, $\Lambda_{\mathrm{delay}}=1.89$). L3 qp6 excluded (severe $\Lambda=77.1$) |
| *ML6*    | *Silty Clay*    |       10.5 |       46.2 |       43.3 |    5.23729 | 1.001* | *EXCLUDED*       | *Eliminato: Collasso bordi Archie ($n_A=1.001$), Low DR (1.16), EDL dominante*                                          |