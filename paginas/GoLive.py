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

########################################
############---GO LIVE---###############
########################################

st.title('Go Live')

col11, col12 = st.columns(2, gap='large')
col13, col14 = st.columns(2, gap='large')

# --- Filtros / datos GoLive ---
GoLive = percentage_not_completed[percentage_not_completed['Group'] == 'GoLive']

# Pivot GoLive
GoLivePivot = GoLive.pivot(index='Region', columns='CW', values='valor')
GoLivePivot = GoLivePivot.reindex().round(2)
GoLivePivot_style = GoLivePivot.style.format("{:.0%}")

# GoLive not updated
with col12:
    with st.container(border=True):
        figGoLiveNot = px.line(
            GoLivePivot.T,
            markers=True,
            title='Go Live not updated'
        )
        st.plotly_chart(figGoLiveNot)

# GoLive updated
GoLiveUpdated = abs(GoLivePivot - 1).round(2)
GoLiveUpdated_style = GoLiveUpdated.style.format("{:.0%}")

with col11:
    with st.container(border=True):
        figGoLiveU = px.line(
            GoLiveUpdated.T,
            markers=True,
            title='Go Live updated'
        )
        st.plotly_chart(figGoLiveU)

# --- GO / NO GO (heatmaps) ---

GoNoGopivot = gonogo.pivot(index="Region", columns="CW", values="Value")

with col14:
    with st.container(border=True):
        Gofignotupdated = px.imshow(
            GoNoGopivot.T,
            aspect='auto',
            title="Go/NoGo (%) not updated",
            text_auto=".0%"
        )
        st.plotly_chart(Gofignotupdated)

GoUpdated = abs(GoNoGopivot - 1)

with col13:
    with st.container(border=True):
        Gofigupdated = px.imshow(
            GoUpdated.T,
            aspect='auto',
            title="Go/NoGo (%) updated",
            text_auto=".0%"
        )
        st.plotly_chart(Gofigupdated)
