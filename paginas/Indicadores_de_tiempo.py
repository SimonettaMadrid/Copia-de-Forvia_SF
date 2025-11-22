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

