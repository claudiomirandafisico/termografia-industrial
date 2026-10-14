import streamlit as st
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Simulador Termofísico Industrial",
    layout="centered"
)

st.title("Simulador Termofísico Industrial")
st.markdown("Análisis directo de temperaturas por fases desde lectura de cámara térmica.")

# --- BARRA LATERAL: PARÁMETROS DE ENTRADA ---
st.sidebar.header("Parámetros de Entrada")

temp_ambiente = st.sidebar.number_input("Temperatura Ambiente (°C)", value=10.0, step=0.5)
tipo_equipo = st.sidebar.selectbox("Equipo", ["Disyuntor", "Contactor", "Transformador", "Motor"])

# Definir límites de temperatura según el tipo de equipo
limites = {
    "Disyuntor": {"advertencia": 60.0, "critico": 80.0},
    "Contactor": {"advertencia": 65.0, "critico": 85.0},
    "Transformador": {"advertencia": 70.0, "critico": 90.0},
    "Motor": {"advertencia": 75.0, "critico": 95.0}
}

lim_adv = limites[tipo_equipo]["advertencia"]
lim_crit = limites[tipo_equipo]["critico"]

st.sidebar.subheader("Lecturas de la Cámara Térmica (°C)")
temp_r = st.sidebar.number_input("Fase R (°C)", value=40.0, step=0.5)
temp_s = st.sidebar.number_input("Fase S (°C)", value=40.0, step=0.5)
temp_t = st.sidebar.number_input("Fase T (°C)", value=40.0, step=0.5)

# --- RESUMEN DE LECTURAS ---
st.subheader("Resumen de Lecturas")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Fase R", f"{temp_r:.1f} °C")
col2.metric("Fase S", f"{temp_s:.1f} °C")
col3.metric("Fase T", f"{temp_t:.1f} °C")

temp_max = max(temp_r, temp_s, temp_t)
col4.metric("Máxima", f"{temp_max:.1f} °C")

# --- EVALUACIÓN DE ESTADO SEGÚN LÍMITES ---
if temp_max >= lim_crit:
    st.error(f"Estado crítico: La temperatura máxima ({temp_max:.1f} °C) supera el límite crítico de {lim_crit} °C.")
elif temp_max >= lim_adv:
    st.warning(f"Estado de advertencia: La temperatura máxima ({temp_max:.1f} °C) supera el límite de alerta de {lim_adv} °C.")
else:
    st.success("Estado normal: Las temperaturas se encuentran dentro de los rangos admisibles.")

# --- GRÁFICO DE TEMPERATURAS ---
st.subheader("Plano Cartesiano de Temperaturas por Fase")

fases = ['Fase R', 'Fase S', 'Fase T']
temperaturas = [temp_r, temp_s, temp_t]
colores = ['#1f77b4', '#ff7f0e', '#2ca02c']

fig = go.Figure(data=[
    go.Bar(
        x=fases,
        y=temperaturas,
        marker_color=colores,
        text=[f"{t:.1f} °C" for t in temperaturas],
        textposition='auto'
    )
])

# Líneas de referencia de límites
fig.add_hline(y=lim_adv, line_dash="dash", line_color="orange", annotation_text=f"Límite Advertencia ({lim_adv}°C)")
fig.add_hline(y=lim_crit, line_dash="dash", line_color="red", annotation_text=f"Límite Crítico ({lim_crit}°C)")

fig.update_layout(
    yaxis_title="Temperatura (°C)",
    yaxis=dict(range=[0, max(120, temp_max + 20)]),
    template="plotly_white",
    margin=dict(t=30, b=30, l=30, r=30)
)

st.plotly_chart(fig, use_container_width=True)
