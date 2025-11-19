import streamlit as st

st.set_page_config(
    page_title= "Selección de Paginas",
    layout = "wide",
    initial_sidebar_state = "expanded"  # collapsed
)

# definir páginas
home_page = st.Page(
    "Paginas/home.py",
    title="Home"
)

EstadoGeneral_page = st.Page(
    "Paginas/Estado_General.py",
    title="Estado General"
)

GoLive_page = st.Page(
    "Paginas/GoLive.py",
    title="Análisis de GoLive"
)

Indicadores_de_Tiempo_page = st.Page(
    "Paginas/Indicadores_de_tiempo.py",
    title="Análisis de Indicadores de Tiempo"
)

workatRisk_page = st.Page(
    "Paginas/Work_at_risk&_Gate_Review.py",
    title="Análisis de Work at Risk & Gate Review"
)

# navegación 
pg = st.navigation({
    "Inicio": [home_page],
    "Análisis": [
        EstadoGeneral_page,
        GoLive_page,
        Indicadores_de_Tiempo_page,
        workatRisk_page
    ]
})

# ejecutar
pg.run()
