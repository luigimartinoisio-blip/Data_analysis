"""Interactive Multi-Panel Dashboard for Hydrogeophysical Data Analysis."""

from pathlib import Path
from typing import List

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.visualization.config import (
    ETICHETTE_QP,
    LABEL_VARIABILI,
)
from src.visualization.cross_plots import crea_cross_plot_plotly, ottieni_lista_qp_per_categoria
from src.visualization.cylinder_3d import crea_figura_cilindro_3d
from src.visualization.landslide_profile import (
    SAMPLE_SLOPE_SPECS,
    crea_profilo_versante_plotly,
)

st.set_page_config(
    page_title="Hydrogeophysical Analysis: GeoTom & HYPROP2",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data
def load_sample_list() -> List[str]:
    """Loads available sample IDs from processed data directory."""
    data_dir = Path("projects/Hyprop_geotom_01Carl/data/processed/tabelle_campioni")
    if not data_dir.exists():
        return []
    files = list(data_dir.glob("*_serie_integrata.csv"))
    return sorted([f.name.replace("_serie_integrata.csv", "") for f in files])


@st.cache_data
def load_sample_data(sample_id: str) -> pd.DataFrame:
    """Loads integrated CSV for a given sample ID."""
    p = Path(
        f"projects/Hyprop_geotom_01Carl/data/processed/tabelle_campioni/{sample_id}_serie_integrata.csv"
    )
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)


@st.cache_data
def load_qc_report() -> pd.DataFrame:
    """Loads reciprocal error summary table."""
    p = Path("projects/Hyprop_geotom_01Carl/data/processed/report_qualita_reciproci.csv")
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)


def render_inspection_popover(
    sample_id: str,
    active_category: str,
    key_prefix: str,
) -> None:
    """Renders a popover dialog showing 3D cylinder and Landslide Slope Profile."""
    with st.popover("🔍 Inspect 3D Geometry & Slope Location"):
        c_3d, c_slope = st.columns([1.0, 2.5])

        with c_3d:
            active_qps = ottieni_lista_qp_per_categoria(active_category)
            fig_3d = crea_figura_cilindro_3d(
                quadripoli_attivi=active_qps,
                categoria_attiva=active_category,
            )
            fig_3d.update_layout(height=380)
            st.plotly_chart(fig_3d, use_container_width=True, key=f"{key_prefix}_pop_3d")

        with c_slope:
            fig_slope = crea_profilo_versante_plotly(campione_attivo=sample_id)
            fig_slope.update_layout(height=380)
            st.plotly_chart(fig_slope, use_container_width=True, key=f"{key_prefix}_pop_slope")

        # Sector & Depth notes
        sec_spec = SAMPLE_SLOPE_SPECS.get(sample_id, (0, 0, "Unknown Sector", "Surface", sample_id))
        st.info(
            f"**Field Sample**: `{sample_id}` ({sec_spec[4]}) — **{sec_spec[3]}** | "
            f"**Sector**: **{sec_spec[2]}** (Survey Elevation: {sec_spec[1]:.1f} m a.s.l.)."
        )


def render_single_panel_view(
    sample_list: List[str],
    default_sample: str,
    key_prefix: str,
) -> None:
    """Renders a full-width interactive cross-plot with sidebar controls."""
    col_ctrl, col_plot = st.columns([1.1, 3.9])

    with col_ctrl:
        st.markdown("#### Configuration")
        def_idx = sample_list.index(default_sample) if default_sample in sample_list else 0
        sample_sel = st.selectbox("Sample", sample_list, index=def_idx, key=f"{key_prefix}_sample")
        df_sample = load_sample_data(sample_sel)

        cat_options = ["All", "Upper", "Lower", "Dipole-dipole", "Wenner"] + list(
            ETICHETTE_QP.keys()
        )
        cat_sel = st.selectbox("Category / Pair", cat_options, index=0, key=f"{key_prefix}_cat")

        var_x_opts = {
            "theta_vol_pct": "Volumetric Water Content θ [Vol%]",
            "ore_trascorse_da_t0": "Elapsed Time [hours]",
            "suzione_media_kpa": "Matric Suction [kPa]",
            "suzione_top_estesa_kpa": "Matric Suction Upper [kPa]",
            "suzione_bottom_estesa_kpa": "Matric Suction Lower [kPa]",
            "log10_suzione_kpa": "log₁₀(Suction [kPa])",
            "grado_saturazione_Sr": "Degree of Saturation Sr [-]",
            "peso_netto_g": "Net Weight [g]",
        }
        var_x = st.selectbox(
            "X-Axis",
            list(var_x_opts.keys()),
            format_func=lambda k: var_x_opts[k],
            index=0,
            key=f"{key_prefix}_vx",
        )

        var_y_opts = {
            "rho_25": "Calibrated Resistivity ρ₂₅ [Ω·m]",
            "rho25_geom_upper": "Geometric Mean Upper ρ₂₅ [Ω·m]",
            "rho25_geom_lower": "Geometric Mean Lower ρ₂₅ [Ω·m]",
            "rho25_geom_dipole": "Geometric Mean Dipole-dipole ρ₂₅ [Ω·m]",
            "rho25_geom_wenner": "Geometric Mean Wenner ρ₂₅ [Ω·m]",
            "suzione_media_kpa": "Matric Suction [kPa]",
            "suzione_top_estesa_kpa": "Matric Suction Upper [kPa]",
            "suzione_bottom_estesa_kpa": "Matric Suction Lower [kPa]",
            "theta_vol_pct": "Water Content θ [Vol%]",
            "peso_netto_g": "Net Weight [g]",
            "temperatura_C": "Temperature [°C]",
        }
        var_y = st.selectbox(
            "Y-Axis",
            list(var_y_opts.keys()),
            format_func=lambda k: var_y_opts[k],
            index=0,
            key=f"{key_prefix}_vy",
        )

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            log_x = st.checkbox("Log X", value=("suzione" in var_x), key=f"{key_prefix}_logx")
        with col_c2:
            log_y = st.checkbox("Log Y", value=False, key=f"{key_prefix}_logy")

        filter_qc = st.checkbox("Filter Reciprocal Error", value=False, key=f"{key_prefix}_fqc")
        qc_thresh = (
            st.slider("Max ε_rec (%)", 1.0, 15.0, 5.0, 0.5, key=f"{key_prefix}_qcth")
            if filter_qc
            else 5.0
        )

        # Popover button for 3D and slope inspection
        render_inspection_popover(sample_sel, cat_sel, f"{key_prefix}_insp")

    with col_plot:
        if not df_sample.empty:
            title_text = f"Sample {sample_sel} — {var_y_opts[var_y]} vs {var_x_opts[var_x]}"
            fig_plot = crea_cross_plot_plotly(
                df=df_sample,
                var_x=var_x,
                categoria_o_qp=cat_sel,
                var_y_tipo=var_y,
                filtra_qc=filter_qc,
                soglia_qc_eps=qc_thresh,
                log_x=log_x,
                log_y=log_y,
                titolo_personalizzato=title_text,
            )
            fig_plot.update_layout(height=520)
            st.plotly_chart(fig_plot, use_container_width=True, key=f"{key_prefix}_chart")


def render_grid_cell(
    cell_id: int,
    sample_list: List[str],
    default_sample: str,
    key_prefix: str,
) -> None:
    """Renders a single cell in the multi-panel comparison grid."""
    with st.container():
        st.markdown(f"**Plot #{cell_id}**")

        # Inline compact controls
        c_s, c_cat, c_x, c_y = st.columns([1.2, 1.2, 1.2, 1.2])
        with c_s:
            def_idx = sample_list.index(default_sample) if default_sample in sample_list else 0
            sample_sel = st.selectbox("Sample", sample_list, index=def_idx, key=f"{key_prefix}_s")
        with c_cat:
            cat_options = ["All", "Upper", "Lower", "Dipole-dipole", "Wenner"] + list(
                ETICHETTE_QP.keys()
            )
            cat_sel = st.selectbox("Category", cat_options, index=0, key=f"{key_prefix}_c")
        with c_x:
            var_x_opts = {
                "theta_vol_pct": "θ [Vol%]",
                "suzione_media_kpa": "ψ [kPa]",
                "suzione_top_estesa_kpa": "ψ_up [kPa]",
                "suzione_bottom_estesa_kpa": "ψ_low [kPa]",
                "ore_trascorse_da_t0": "Time [h]",
                "grado_saturazione_Sr": "Sr [-]",
            }
            var_x = st.selectbox(
                "X-Axis",
                list(var_x_opts.keys()),
                format_func=lambda k: var_x_opts[k],
                index=0,
                key=f"{key_prefix}_x",
            )
        with c_y:
            var_y_opts = {
                "rho_25": "ρ₂₅ [Ω·m]",
                "rho25_geom_upper": "ρ₂₅,up [Ω·m]",
                "rho25_geom_lower": "ρ₂₅,low [Ω·m]",
                "rho25_geom_dipole": "ρ₂₅,dip [Ω·m]",
                "rho25_geom_wenner": "ρ₂₅,wen [Ω·m]",
                "suzione_media_kpa": "ψ [kPa]",
                "suzione_top_estesa_kpa": "ψ_up [kPa]",
                "suzione_bottom_estesa_kpa": "ψ_low [kPa]",
                "theta_vol_pct": "θ [Vol%]",
            }
            var_y = st.selectbox(
                "Y-Axis",
                list(var_y_opts.keys()),
                format_func=lambda k: var_y_opts[k],
                index=0,
                key=f"{key_prefix}_y",
            )

        c_opt1, c_opt2, c_qc = st.columns([1, 1, 2])
        with c_opt1:
            log_x = st.checkbox(
                "Log X",
                value=("suzione" in var_x),
                key=f"{key_prefix}_lx",
            )
        with c_opt2:
            log_y = st.checkbox("Log Y", value=False, key=f"{key_prefix}_ly")
        with c_qc:
            filter_qc = st.checkbox(
                "Filter ε_rec < 5%",
                value=False,
                key=f"{key_prefix}_fqc",
            )
            qc_thresh = 5.0

        render_inspection_popover(sample_sel, cat_sel, f"{key_prefix}_grid_insp")

        df_sample = load_sample_data(sample_sel)
        if not df_sample.empty:
            title_text = f"Sample {sample_sel} ({cat_sel})"
            fig_plot = crea_cross_plot_plotly(
                df=df_sample,
                var_x=var_x,
                categoria_o_qp=cat_sel,
                var_y_tipo=var_y,
                filtra_qc=filter_qc,
                soglia_qc_eps=qc_thresh,
                log_x=log_x,
                log_y=log_y,
                titolo_personalizzato=title_text,
            )
            fig_plot.update_layout(height=420, margin=dict(l=40, r=20, t=40, b=60))
            st.plotly_chart(fig_plot, use_container_width=True, key=f"{key_prefix}_fig")


def main() -> None:
    st.title("⚡ Hydrogeophysical Dashboard: GeoTom & HYPROP2")
    st.markdown(
        "**Level 1 Analysis: 1-to-1 Cross-Correlations** | "
        "Calibrated $\\rho_{25}$, Water Content $\\theta(t)$, and Matric Suction $\\psi_m(t)$"
    )

    sample_list = load_sample_list()
    if not sample_list:
        st.error("No processed datasets found in `data/processed/tabelle_campioni/`!")
        return

    # --- MAIN NAVIGATION TABS ---
    tab_single, tab_grid, tab_overlay, tab_data, tab_qc = st.tabs(
        [
            "📈 Single Panel View",
            "🔲 Grid Comparison (Quadro 2x2)",
            "🌐 Multi-Sample Overlay",
            "📋 Data Tables",
            "🛡️ Reciprocal QC Report",
        ]
    )

    # 1. SINGLE PANEL VIEW
    with tab_single:
        st.subheader("📊 Single Sample Detailed Analysis")
        render_single_panel_view(sample_list, default_sample="ML3", key_prefix="single")

    # 2. MULTI-PANEL GRID
    with tab_grid:
        st.subheader("🔲 Multi-Panel Comparative Grid")
        n_plots = st.radio(
            "Select Number of Concurrent Panels",
            [2, 3, 4],
            index=2,
            horizontal=True,
            help="Compare 2, 3, or 4 independent plots simultaneously.",
        )

        samples_def = ["ML3", "ML7", "ML5", "ML1"]

        if n_plots == 2:
            col1, col2 = st.columns(2)
            with col1:
                render_grid_cell(1, sample_list, samples_def[0], "grid_p1")
            with col2:
                render_grid_cell(2, sample_list, samples_def[1], "grid_p2")

        elif n_plots == 3:
            col1, col2 = st.columns(2)
            with col1:
                render_grid_cell(1, sample_list, samples_def[0], "grid_p1")
            with col2:
                render_grid_cell(2, sample_list, samples_def[1], "grid_p2")

            st.markdown("---")
            col3, col4 = st.columns(2)
            with col3:
                render_grid_cell(3, sample_list, samples_def[2], "grid_p3")
            with col4:
                fig_slope_full = crea_profilo_versante_plotly(campione_attivo=samples_def[2])
                fig_slope_full.update_layout(height=420)
                st.plotly_chart(fig_slope_full, use_container_width=True)

        elif n_plots == 4:
            col1, col2 = st.columns(2)
            with col1:
                render_grid_cell(1, sample_list, samples_def[0], "grid_p1")
            with col2:
                render_grid_cell(2, sample_list, samples_def[1], "grid_p2")

            st.markdown("---")
            col3, col4 = st.columns(2)
            with col3:
                render_grid_cell(3, sample_list, samples_def[2], "grid_p3")
            with col4:
                render_grid_cell(4, sample_list, samples_def[3], "grid_p4")

    # 3. MULTI-SAMPLE OVERLAY
    with tab_overlay:
        st.subheader("🌐 Multi-Sample Overlay Comparison")
        st.markdown("Overlay curves from multiple samples on a single unified chart.")

        col_ov_ctrl, col_ov_plot = st.columns([1.2, 3.8])
        with col_ov_ctrl:
            selected_samples = st.multiselect(
                "Select Samples to Overlay",
                sample_list,
                default=["ML3", "ML7", "Sand_R"]
                if all(s in sample_list for s in ["ML3", "ML7", "Sand_R"])
                else sample_list[:3],
            )
            target_opts = {
                **ETICHETTE_QP,
                "rho25_geom_upper": "Geometric Mean Upper ρ₂₅",
                "rho25_geom_lower": "Geometric Mean Lower ρ₂₅",
                "rho25_geom_dipole": "Geometric Mean Dipole-dipole ρ₂₅",
                "rho25_geom_wenner": "Geometric Mean Wenner ρ₂₅",
                "suzione_top_estesa_kpa": "Matric Suction Upper [kPa]",
                "suzione_bottom_estesa_kpa": "Matric Suction Lower [kPa]",
                "suzione_media_kpa": "Matric Suction [kPa]",
            }
            target_var = st.selectbox(
                "Variable / Quadrupole to Overlay",
                list(target_opts.keys()),
                index=0,
                format_func=lambda k: target_opts[k],
            )
            ov_var_x = st.selectbox(
                "X-Axis",
                [
                    "theta_vol_pct",
                    "suzione_media_kpa",
                    "suzione_top_estesa_kpa",
                    "suzione_bottom_estesa_kpa",
                    "ore_trascorse_da_t0",
                    "grado_saturazione_Sr",
                ],
                format_func=lambda k: LABEL_VARIABILI.get(k, k),
                index=0,
            )
            ov_log_x = st.checkbox("Log X", value=("suzione" in ov_var_x), key="ov_logx")
            ov_log_y = st.checkbox("Log Y", value=False, key="ov_logy")
            ov_filtra_qc = st.checkbox(
                "Filter Reciprocal Error (ε_rec < 5%)", value=False, key="ov_fqc"
            )

        with col_ov_plot:
            if selected_samples:
                fig_ov = go.Figure()
                palette_samples = [
                    "#1f77b4",
                    "#ff7f0e",
                    "#2ca02c",
                    "#d62728",
                    "#9467bd",
                    "#8c564b",
                    "#e377c2",
                    "#7f7f7f",
                    "#bcbd22",
                    "#17becf",
                ]

                for s_idx, s_id in enumerate(selected_samples):
                    df_s = load_sample_data(s_id)
                    col_target = (
                        target_var
                        if target_var.startswith(("rho25_geom_", "suzione_"))
                        else f"rho25_{target_var}"
                    )
                    col_eps = (
                        f"eps_{target_var}"
                        if not target_var.startswith(("rho25_geom_", "suzione_"))
                        else None
                    )
                    if col_target in df_s.columns:
                        df_s_filt = df_s.copy()
                        if ov_filtra_qc and col_eps and col_eps in df_s_filt.columns:
                            df_s_filt = df_s_filt[
                                (df_s_filt[col_eps] < 5.0) | (df_s_filt[col_eps].isna())
                            ]

                        df_s_valid = df_s_filt.dropna(subset=[ov_var_x, col_target])
                        fig_ov.add_trace(
                            go.Scatter(
                                x=df_s_valid[ov_var_x],
                                y=df_s_valid[col_target],
                                mode="lines+markers",
                                name=f"{s_id} ({target_opts.get(target_var, target_var)})",
                                marker=dict(size=7),
                                line=dict(
                                    width=2, color=palette_samples[s_idx % len(palette_samples)]
                                ),
                            )
                        )
                x_name = LABEL_VARIABILI.get(ov_var_x, ov_var_x)
                y_name = target_opts.get(target_var, target_var)
                ov_title = f"Multi-Sample Overlay — {y_name} vs {x_name}"
                fig_ov.update_layout(
                    title=dict(text=ov_title, x=0.5, font=dict(size=15)),
                    xaxis=dict(title=x_name, type="log" if ov_log_x else "linear", showgrid=True),
                    yaxis=dict(title=y_name, type="log" if ov_log_y else "linear", showgrid=True),
                    template="plotly_white",
                    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
                    margin=dict(l=60, r=40, t=50, b=80),
                )
                st.plotly_chart(fig_ov, use_container_width=True)

    # 4. DATA TABLES
    with tab_data:
        st.subheader("📋 Integrated Data Tables")
        s_sel = st.selectbox(
            "Select Sample to View Table", sample_list, index=0, key="tab_data_sel"
        )
        df_tab = load_sample_data(s_sel)
        st.dataframe(df_tab, use_container_width=True)
        csv_data = df_tab.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"📥 Download {s_sel}_serie_integrata.csv",
            data=csv_data,
            file_name=f"{s_sel}_serie_integrata.csv",
            mime="text/csv",
        )

    # 5. QC REPORT
    with tab_qc:
        st.subheader("🛡️ Reciprocal Error QC Summary Across All Samples")
        df_qc_rep = load_qc_report()
        if not df_qc_rep.empty:
            st.dataframe(df_qc_rep, use_container_width=True)
        else:
            st.info("QC report is not available.")


if __name__ == "__main__":
    main()
