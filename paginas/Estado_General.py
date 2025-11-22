import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_all_data

# ==========================
# CARGA DE DATOS
# ==========================
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

# ==========================
# TÍTULO DE LA PÁGINA
# ==========================
st.title("Estado General de los Proyectos por Región o Domain")

# ==========================
# PERFORMANCE DERECHO
# ==========================

# Project Health (CW)
project_health = performance_derecho[
    performance_derecho["Tablero"] == "Project Status "
]
project_health_pivot = project_health.pivot(
    index="Status", columns="CW", values="Value"
)

orden_colores = ["Green", "Yellow", "Red", "No Status"]
orden_colores2 = ["Green", "Red"]

project_health_pivot = project_health_pivot.reindex(orden_colores)

# Gate Status (CW)
gate_status = performance_derecho[
    performance_derecho["Tablero"] == "Gate status"
]
gate_status_pivot = gate_status.pivot(
    index="Status", columns="CW", values="Value"
)
gate_status_pivot = gate_status_pivot.reindex(orden_colores2)

# ==========================
# PERFORMANCE IZQUIERDO
# ==========================

project_health_areas = performance_izquierdo[
    performance_izquierdo["Tablero"] == "Project Health"
]
project_health_areas_pivot = project_health_areas.pivot(
    index="Status", columns="Region", values="Value"
)
project_health_areas_pivot = project_health_areas_pivot.reindex(orden_colores)

gate_status_total = performance_izquierdo[
    performance_izquierdo["Tablero"] == "Gate status"
]
totales_gate = (
    gate_status_total.groupby("Status", as_index=False)["Value"].sum()
)

# ==========================
# TIME TO PASS
# ==========================

time_closed = time_to_pass[time_to_pass["Tablero"] == "Closed"].copy()
time_plot = time_closed[
    time_closed["Region"].isin(["WW", "Target"])
].copy()

nombre_series = {
    "WW": "% of projects on time (<= 30 days delay)",
    "Target": "Target 50%",
}

time_plot["Serie"] = time_plot["Region"].map(nombre_series)

# ==========================
# LAYOUT PRINCIPAL
# ==========================

col20, col21 = st.columns([10, 6])
col23, col24 = st.columns([10, 6])
col25, col26, col30 = st.columns([6, 6, 6])
col27, col28, col29 = st.columns([6, 6, 6])

# -------- SELECTORES --------
with col20:
    seleccion_grafico_PH = st.selectbox(
        "Selecciona el tipo de gráfico para Project Health",
        ["Barras", "Area"],
    )

with col21:
    seleccion_region_domain = st.selectbox(
        "Selecciona Domain o Region para Project Health",
        ["Region", "Domain"],
    )

# -------- Project Health (CW) --------
with col23:
    if seleccion_grafico_PH == "Area":
        with st.container(border=True):
            figPH = px.area(
                project_health_pivot.T,
                markers=True,
                title="Overall Project Health",
                color_discrete_map={
                    "Yellow": "yellow",
                    "Red": "red",
                    "Green": "#33bf24",
                    "No Status": "gray",
                },
            )
            st.plotly_chart(figPH)

    if seleccion_grafico_PH == "Barras":
        with st.container(border=True):
            figPH = px.bar(
                project_health_pivot.T,
                title="Overall Project Health",
                color_discrete_map={
                    "Yellow": "yellow",
                    "Red": "red",
                    "Green": "#33bf24",
                    "No Status": "gray",
                },
            )
            st.plotly_chart(figPH)

# -------- Project Health por Region o Domain --------
with col24:
    if seleccion_region_domain == "Region":
        with st.container(border=True):
            figPHRegion = px.bar(
                project_health_areas_pivot.T,
                title="Overall Project Health (Region)",
            )
            st.plotly_chart(figPHRegion)

    if seleccion_region_domain == "Domain":
        st.info("Vista por Domain está pendiente de implementarse.")

# -------- GATE STATUS --------
with col25:
    seleccion_grafico_GS = st.selectbox(
        "Selecciona el tipo de gráfico para Gate Status",
        ["Area", "Barras"],
    )

# Gate status por CW
if seleccion_grafico_GS == "Area":
    with col27:
        with st.container(border=True):
            figGS = px.area(
                gate_status_pivot.T,
                title="Gate Status",
                color_discrete_map={
                    "Red": "red",
                    "Green": "#33bf24",
                },
            )
            st.plotly_chart(figGS)

if seleccion_grafico_GS == "Barras":
    with col27:
        with st.container(border=True):
            figGS = px.bar(
                gate_status_pivot.T,
                title="Gate Status",
                color_discrete_map={
                    "Red": "red",
                    "Green": "#33bf24",
                },
            )
            st.plotly_chart(figGS)

# Totales Gate Review
with col28:
    with st.container(border=True):
        figGST = px.bar(
            totales_gate,
            x="Status",
            y="Value",
            text="Value",
            title="Gate status – Totales",
            color="Status",
        )
        st.plotly_chart(figGST)

# -------- TIME TO PASS --------
with col29:
    with st.container(border=True):
        figTime = px.line(
            time_plot,
            x="CW",
            y="Value",
            color="Serie",
            title="Projects on time %",
            labels={
                "CW": "Calendar Week",
                "Value": "% of projects on time",
                "Serie": "",
            },
            color_discrete_map={
                "% of projects on time (<= 30 days delay)": "blue",
                "Target 50%": "red",
            },
        )
        st.plotly_chart(figTime)

# ===============================================
#               FIN DE LA PÁGINA
# ===============================================



