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
) = load_all_data()

########################
# ------WAR Y GR------ #
########################

st.title('Work at Risk & Gate Review')

# Filtros de WAR y GR
regiones = sorted(percentage_not_completed['Region'].unique().tolist())

optionswar = ['WAR not updated', 'WAR updated']
optionsbarras = ['WAR Region', 'Gate Review Region', 'WAR Domain', 'Gate Review Domain']

col7, col8, col9 = st.columns([5, 5, 5], gap='large')
col4, col5, col6 = st.columns([6, 6, 6], gap='large')

# -------- SELECTORES SUPERIORES --------
with col7:
    eleccionwar = st.selectbox(
        'Escoje WAR updated o no updated',
        options=optionswar
    )

with col8:
    elecciongr = st.selectbox(
        'Escoje Gate Review updated o no updated',
        options=['Gate Review not updated', 'Gate Review updated']
    )

with col9:
    eleccionbarras = st.selectbox(
        'Escoje Segmento',
        options=optionsbarras
    )

# -------- WAR (líneas) --------
# Filtros para Pivot, para WAR con percentage_not_completed 
pncwar = percentage_not_completed[percentage_not_completed['Group'] == 'WAR']

# Pivot del WAR
pivotwar = pncwar.pivot(index="Region", columns="CW", values="valor")
pivotwar = pivotwar.reindex().round(2)
pivotwar_style = pivotwar.style.format("{:.0%}")  # Para mostrar % y que sigan siendo float

if eleccionwar == 'WAR not updated':
    with col4:
        with st.container(border=True):
            figWARNU = px.line(
                pivotwar.T,
                markers=True,
                title="WAR not updated (%) por CW"
            )
            st.plotly_chart(figWARNU)

updatedwar = abs(pivotwar - 1).round(2)  # Fórmula para updated
updatedwar_style = updatedwar.style.format("{:.0%}")

if eleccionwar == 'WAR updated':
    with col4:
        with st.container(border=True):
            figWARU = px.line(
                updatedwar.T,
                markers=True,
                title="WAR updated (%) por CW"
            )
            st.plotly_chart(figWARU)

# -------- GATE REVIEW (líneas) --------
pncgr = percentage_not_completed[percentage_not_completed['Group'] == 'Gate Review']

pivotgr = pncgr.pivot(index="Region", columns="CW", values="valor")
pivotgr = pivotgr.reindex().round(2)
pivotgr_style = pivotgr.style.format("{:.0%}")

updatedgr = abs(pivotgr - 1).round(2)
updatedgr_style = updatedgr.style.format("{:.0%}")

if elecciongr == 'Gate Review not updated':
    with col5:
        with st.container(border=True):
            figGR = px.line(
                pivotgr.T,
                markers=True,
                title='Gate Review not updated (%)'
            )
            st.plotly_chart(figGR)

if elecciongr == 'Gate Review updated':
    with col5:
        with st.container(border=True):
            figGRU = px.line(
                updatedgr.T,
                markers=True,
                title='Gate Review updated (%)'
            )
            st.plotly_chart(figGRU)

# -------- BARRAS WAR / GR (Region / Domain) --------

# WAR Region
WARregion = region_domain_data[
    (region_domain_data['Group'] == 'WAR') &
    (region_domain_data['Segment'] == 'Region')
]
warpivotcompleto = WARregion.pivot(index='Row', columns='Column', values='Value')

# GR Region
GRregion = region_domain_data[
    (region_domain_data['Group'] == 'Gate Review (2)') &
    (region_domain_data['Segment'] == 'Region')
]
GRregionpivot = GRregion.pivot(index='Row', columns='Column', values='Value')

# WAR Domain
WARdomain = region_domain_data[
    (region_domain_data['Group'] == 'WAR') &
    (region_domain_data['Segment'] == 'Domain')
]
WARdomainpivot = WARdomain.pivot(index='Row', columns='Column', values='Value')

# GR Domain
GRdomain = region_domain_data[
    (region_domain_data['Group'] == 'Gate Review (2)') &
    (region_domain_data['Segment'] == 'Domain')
]
GRdomainpivot = GRdomain.pivot(index='Row', columns='Column', values='Value')

with col6:
    with st.container(border=True):
        if eleccionbarras == 'WAR Region':
            figWARC = px.bar(warpivotcompleto.T, title='WAR by Region')
            st.plotly_chart(figWARC)

        elif eleccionbarras == 'Gate Review Region':
            figGRregion = px.bar(GRregionpivot.T, title='Gate Review por Region')
            st.plotly_chart(figGRregion)

        elif eleccionbarras == 'WAR Domain':
            figWARdomain = px.bar(WARdomainpivot.T, title='WAR por Domain')
            st.plotly_chart(figWARdomain)

        elif eleccionbarras == 'Gate Review Domain':
            figGRdomain = px.bar(GRdomainpivot.T, title='Gate Review por Domain')
            st.plotly_chart(figGRdomain)



    


