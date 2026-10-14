import streamlit as st
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Simulador Termofísico Industrial",
    layout="centered"
)

st.title("Simulador Termofísico Industrial")
st.markdown("Evaluación térmica y diagnósticos según estándares NETA / IEC.")

# --- BARRA LATERAL: PARÁMETROS DE ENTRADA ---
st.sidebar.header("Parámetros")

temp_ambiente = st.sidebar.number_input("Temperatura Ambiente (°C)", value=10.0, step=0.5)
tipo_equipo = st.sidebar.selectbox("Equipo", ["Disyuntor", "Contactor", "Transformador", "Motor"])

# Límites absolutos según equipo
limites = {
    "Disyuntor": {"advertencia": 60.0, "critico": 80.0},
    "Contactor": {"advertencia": 65.0, "critico": 85.0},
    "Transformador": {"advertencia": 70.0, "critico": 90.0},
    "Motor": {"advertencia": 75.0, "critico": 95.0}
}

lim_adv = limites[tipo_equipo]["advertencia"]
lim_crit = limites[tipo_equipo]["critico"]

st.sidebar.subheader("Lecturas Cámara Térmica")
temp_r = st.sidebar.number_input("Fase R (°C)", value=40.
                                 
