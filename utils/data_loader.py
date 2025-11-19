import streamlit as st
import pandas as pd

@st.cache_resource
def load_all_data():
    projectos_forvia_clean = pd.read_csv('/Users/simomadrid/Desktop/Analitica/Forvia_SF/data/projectos_forvia_clean.csv')
    percentage_not_completed = pd.read_csv('/Users/simomadrid/Desktop/Analitica/Forvia_SF/data/percentage_not_completed.csv')
    region_domain_data = pd.read_csv('/Users/simomadrid/Desktop/Analitica/Forvia_SF/data/region_domain_data.csv')
    gr = pd.read_csv('/Users/simomadrid/Desktop/Analitica/Forvia_SF/data/GR.csv')
    war = pd.read_csv('/Users/simomadrid/Desktop/Analitica/Forvia_SF/data/WAR.csv')
    gonogo = pd.read_csv('/Users/simomadrid/Desktop/Analitica/Forvia_SF/data/go_nogo.csv')
    performance_derecho=pd.read_csv('/Users/simomadrid/Desktop/Analitica/Forvia_SF/data/performance_derecho.csv')
    performance_izquierdo= pd.read_csv('/Users/simomadrid/Desktop/Analitica/Forvia_SF/data/performance_izquierdo.csv')
    regiones= pd.read_csv('/Users/simomadrid/Desktop/Analitica/Forvia_SF/data/regions_coordinates.csv')
    time_to_pass= pd.read_csv('/Users/simomadrid/Desktop/Analitica/Forvia_SF/data/time_to_pass.csv')
    data= pd.read_csv('/Users/simomadrid/Desktop/Analitica/Forvia_SF/data/data.csv')
    return (
        projectos_forvia_clean,
        percentage_not_completed,
        region_domain_data,
        gr,
        war,
        gonogo,
        performance_derecho,
        performance_izquierdo, 
        regiones,time_to_pass,data

    )

def assign_coords_to_projects(df, region_col='Geographical scope'):
    region_coords = {
        'EMEA':{'lat': 50.1109, 'lon': 8.6820},
        'ASIA':{'lat': 35.6895, 'lon': 139.6917},
        'NAO':{'lat': 41.3314, 'lon': -83.0458},
        'SAO':{'lat': -23.5505, 'lon': -46.6333},
    }

    df=df.copy()
    df['lat']=df[region_col].map(lambda x: region_coords.get(x,{}).get('lat',None))
    df['lon']=df[region_col].map(lambda x: region_coords.get(x,{}).get('lon',None))
    return df.dropna(subset=['lat','lon'])