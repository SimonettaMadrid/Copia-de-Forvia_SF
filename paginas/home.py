# Paginas/home.py

import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from utils.data_loader import load_all_data
from utils.data_loader import assign_coords_to_projects

# Paleta tipo FORVIA
PALETTE = ["#0A2342", "#1E3A8A", "#3B82F6", "#60A5FA", "#10B981"]

# =======================
# CARGA DE DATOS
# =======================
(
    projectos_forvia_clean,
    percentage_not_completed,
    region_domain_data,
    gr,
    war,
    gonogo,
    performance_derecho,
    performance_izquierdo,
    regiones,
    time_to_pass,
    data,          # 👈 Faltaba esta
) = load_all_data()

df = projectos_forvia_clean.copy()

# =======================
# PREPARACIÓN
# =======================

# Aseguramos Percent complete numérico
if "Percent complete" in df.columns:
    df["Percent complete"] = pd.to_numeric(df["Percent complete"], errors="coerce")

# Normalizamos Region para usarla como clave
if "Region" in df.columns:
    df["Region_key"] = df["Region"].astype(str).str.lower().str.strip()
else:
    df["Region_key"] = None

# Diccionario de regiones -> coordenadas y macro-región
REGION_COORDS = {
    # claves esperadas en tu CSV de proyectos
    "nao":   {"lat": 40,  "lon": -95, "Region_forvia": "North America"},
    "sao":   {"lat": -15, "lon": -60, "Region_forvia": "South America"},
    "asia":  {"lat": 30,  "lon": 100, "Region_forvia": "Asia"},
    "europa":{"lat": 50,  "lon": 10,  "Region_forvia": "Europe"},
    "vw":    {"lat": 52,  "lon": 10,  "Region_forvia": "Europe"},
    "emea":  {"lat": 48,  "lon": 2,   "Region_forvia": "Europe"},
}

def get_region_forvia(key):
    info = REGION_COORDS.get(key)
    return info["Region_forvia"] if info is not None else None

def get_lat(key):
    info = REGION_COORDS.get(key)
    return info["lat"] if info is not None else None

def get_lon(key):
    info = REGION_COORDS.get(key)
    return info["lon"] if info is not None else None

df["Region_forvia"] = df["Region_key"].apply(get_region_forvia)
df["lat"] = df["Region_key"].apply(get_lat)
df["lon"] = df["Region_key"].apply(get_lon)

# =======================
# HEADER
# =======================
st.title("Dashboard FORVIA – Home")


# =======================
# FILTROS (SIDEBAR)
# =======================
st.sidebar.header("Filtros globales")

# Filtro por macro-región
if "Region_forvia" in df.columns:
    regiones_forvia = sorted(df["Region_forvia"].dropna().unique().tolist())
else:
    regiones_forvia = []

selected_regiones_forvia = st.sidebar.multiselect(
    "Macro-región FORVIA",
    options=regiones_forvia,
    default=regiones_forvia,
)

# Filtro por Region (código original)
if "Region" in df.columns:
    regiones_raw = sorted(df["Region"].dropna().unique().tolist())
else:
    regiones_raw = []

selected_regiones_raw = st.sidebar.multiselect(
    "Región (código original)",
    options=regiones_raw,
    default=regiones_raw,
)

# Filtro por State
if "State" in df.columns:
    estados = sorted(df["State"].dropna().unique().tolist())
else:
    estados = []

selected_estados = st.sidebar.multiselect(
    "Estado (State)",
    options=estados,
    default=estados,
)

# Filtro por Project size
if "Project size" in df.columns:
    sizes = sorted(df["Project size"].dropna().unique().tolist())
else:
    sizes = []

selected_sizes = st.sidebar.multiselect(
    "Project size",
    options=sizes,
    default=sizes,
)

# Filtro por % avance
if "Percent complete" in df.columns and df["Percent complete"].notna().any():
    pc_min = float(df["Percent complete"].min())
    pc_max = float(df["Percent complete"].max())
    pc_range = st.sidebar.slider(
        "Rango de % avance",
        min_value=float(pc_min),
        max_value=float(pc_max),
        value=(float(pc_min), float(pc_max)),
        step=1.0,
    )
else:
    pc_range = None

# =======================
# APLICAR FILTROS
# =======================
mask = pd.Series(True, index=df.index)

if selected_regiones_forvia:
    mask &= df["Region_forvia"].isin(selected_regiones_forvia)

if selected_regiones_raw:
    mask &= df["Region"].isin(selected_regiones_raw)

if selected_estados:
    mask &= df["State"].isin(selected_estados)

if selected_sizes:
    mask &= df["Project size"].isin(selected_sizes)

if pc_range is not None and "Percent complete" in df.columns:
    mask &= df["Percent complete"].between(pc_range[0], pc_range[1])

df_filtrado = df[mask].copy()


# =======================
# KPIs
# =======================
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

# KPI 1: Total proyectos filtrados
with col_kpi1:
    with st.container(border=True):
        total_projects = len(df_filtrado)
        st.markdown("**Total de proyectos (filtrados)**")
        st.markdown(
            f"<h2 style='margin-top:0; color:{PALETTE[2]};'>{total_projects}</h2>",
            unsafe_allow_html=True,
        )

# KPI 2: Avance promedio
with col_kpi2:
    with st.container(border=True):
        st.markdown("**Avance promedio**")
        if "Percent complete" in df_filtrado.columns and not df_filtrado.empty:
            avg_percent = df_filtrado["Percent complete"].mean()
            st.markdown(
                f"<h2 style='margin-top:0; color:{PALETTE[3]};'>{avg_percent:.1f}%</h2>",
                unsafe_allow_html=True,
            )
        else:
            st.write("Sin datos de `Percent complete` en el filtro actual.")

# KPI 3: Regiones monitoreadas
with col_kpi3:
    with st.container(border=True):
        st.markdown("**Regiones monitoreadas**")
        if "Region_forvia" in df_filtrado.columns and not df_filtrado.empty:
            n_regiones = df_filtrado["Region_forvia"].nunique()
        else:
            n_regiones = 0

        st.markdown(
            f"<h2 style='margin-top:0; color:{PALETTE[4]};'>{n_regiones}</h2>",
            unsafe_allow_html=True,
        )

st.divider()

# =======================
# FILA 1: BARRA POR STATE + MAPA
# =======================
col_left, col_right = st.columns([2, 3])

# --- IZQUIERDA: Barra por State ---
with col_left:
    st.subheader("Distribución de proyectos por estado")

    if "State" in df_filtrado.columns and not df_filtrado.empty:
        state_counts = (
            df_filtrado["State"]
            .value_counts(dropna=False)
            .reset_index()
        )
        if state_counts.shape[1] == 2:
            state_counts.columns = ["State", "Count"]

            fig_state = px.bar(
                state_counts,
                x="State",
                y="Count",
                title="Proyectos por estado",
                text="Count",
                color="State",
                color_discrete_sequence=PALETTE,
            )
            fig_state.update_layout(
                xaxis_title="",
                yaxis_title="Número de proyectos",
                margin=dict(t=60, l=10, r=10, b=40),
            )
            st.plotly_chart(fig_state, use_container_width=True)
        else:
            st.write("Formato inesperado para `State`.")
    else:
        st.info("No hay datos de `State` después de aplicar los filtros.")

# --- DERECHA: Mapa de círculos por macro-región FORVIA ---
with col_right:
    st.subheader("Mapa de avance por macro-región FORVIA")
    df_coords = assign_coords_to_projects (projectos_forvia_clean,'Geographical scope')
    st.map(df_coords[['lat','lon']],color='#38303086', zoom=1, size=300000)

    map_center=[df_coords['lat'].mean(),df_coords['lon'].mean()]
    m=folium.Map(location=map_center, zoom_start=2)

    for _, row in df_coords.iterrows():
        folium.Marker(
        [row['lat'],row['lon']]
        ,popup=f"{row['Project Name']}- {row['Geographical scope']}"
        ).add_to(m)
   

st.divider()

# =======================
# FILA 2: DISTRIBUCIONES EXTRA
# =======================
st.subheader("Distribuciones clave de los proyectos")

col_a, col_b = st.columns(2)

# --- A: Proyectos por macro-región FORVIA ---
with col_a:
    if "Region_forvia" in df_filtrado.columns and not df_filtrado.empty:
        region_counts = (
            df_filtrado["Region_forvia"]
            .value_counts(dropna=False)
            .reset_index()
        )
        if region_counts.shape[1] == 2:
            region_counts.columns = ["Region_forvia", "Count"]

            fig_region = px.bar(
                region_counts,
                x="Region_forvia",
                y="Count",
                title="Proyectos por macro-región FORVIA",
                text="Count",
                color="Region_forvia",
                color_discrete_sequence=PALETTE,
            )
            fig_region.update_layout(
                xaxis_title="",
                yaxis_title="Número de proyectos",
                margin=dict(t=60, l=10, r=10, b=40),
            )
            st.plotly_chart(fig_region, use_container_width=True)
        else:
            st.write("Formato inesperado para `Region_forvia`.")
    else:
        st.info("No hay datos de `Region_forvia` después de aplicar los filtros.")

# --- B: Avance promedio por macro-región FORVIA ---
with col_b:
    if (
        "Region_forvia" in df_filtrado.columns
        and "Percent complete" in df_filtrado.columns
        and not df_filtrado.empty
    ):
        avg_by_region = (
            df_filtrado.groupby("Region_forvia", dropna=False)["Percent complete"]
            .mean()
            .reset_index()
        )
        avg_by_region.rename(columns={"Percent complete": "AvgPercent"}, inplace=True)

        fig_avg_reg = px.bar(
            avg_by_region,
            x="Region_forvia",
            y="AvgPercent",
            title="Avance promedio por macro-región FORVIA",
            text="AvgPercent",
            color="Region_forvia",
            color_discrete_sequence=PALETTE,
        )
        fig_avg_reg.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_avg_reg.update_layout(
            xaxis_title="",
            yaxis_title="% avance promedio",
            margin=dict(t=60, l=10, r=10, b=40),
        )
        st.plotly_chart(fig_avg_reg, use_container_width=True)
    else:
        st.info("No se puede calcular el avance promedio por región con el filtro actual.")

st.divider()
st.caption("Home – tablero general del portafolio de proyectos FORVIA.")













