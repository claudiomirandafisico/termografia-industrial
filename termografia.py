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
temp_r = st.sidebar.number_input("Fase R (°C)", value=40.0, step=0.5)
temp_s = st.sidebar.number_input("Fase S (°C)", value=40.0, step=0.5)
temp_t = st.sidebar.number_input("Fase T (°C)", value=40.0, step=0.5)

# --- RESUMEN Y DELTA T ---
st.subheader("Resumen de Lecturas")

temp_min = min(temp_r, temp_s, temp_t)
temp_max = max(temp_r, temp_s, temp_t)
delta_t_fases = temp_max - temp_min

col1, col2, col3, col4 = st.columns(4)
col1.metric("Fase R", f"{temp_r:.1f} °C")
col2.metric("Fase S", f"{temp_s:.1f} °C")
col3.metric("Fase T", f"{temp_t:.1f} °C")
col4.metric("ΔT Máximo", f"{delta_t_fases:.1f} °C")

# --- DIAGNÓSTICO NORMATIVO ---
st.subheader("Diagnóstico Normativo")

if delta_t_fases <= 3.0:
    st.success("Condición Normal (NETA): Diferencia menor a 3 °C. Parámetros habituales de operación.")
elif 4.0 <= delta_t_fases <= 15.0:
    st.warning("Anomalía Menor (NETA): Diferencia entre 4 °C y 15 °C. Programar revisión de seguimiento.")
elif 16.0 <= delta_t_fases <= 40.0:
    st.error("Anomalía Grave (NETA): Diferencia entre 16 °C y 40 °C. Reparación prioritaria recomendada.")
else:
    st.error("Anomalía Crítica (NETA): Diferencia superior a 40 °C. Riesgo inminente de falla.")

if temp_max >= lim_crit:
    st.error(f"Alerta Absoluta: La temperatura máxima ({temp_max:.1f} °C) excede el límite crítico de {lim_crit} °C.")
elif temp_max >= lim_adv:
    st.warning(f"Aviso Absoluto: La temperatura máxima ({temp_max:.1f} °C) supera el umbral de advertencia de {lim_adv} °C.")
else:
    st.info(f"Temperatura Absoluta Normal para {tipo_equipo.lower()}.")

# --- GRÁFICO ---
st.subheader("Gráfico de Temperaturas por Fase")

fases = ['Fase R', 'Fase S', 'Fase T']
temperaturas = [temp_r, temp_s, temp_t]
colores = ['#2b5c8f', '#d95f02', '#1b9e77']

fig = go.Figure(data=[
    go.Bar(
        x=fases,
        y=temperaturas,
        marker_color=colores,
        text=[f"{t:.1f} °C" for t in temperaturas],
        textposition='auto'
    )
])

fig.add_hline(y=lim_adv, line_dash="dash", line_color="#e6ab02", annotation_text=f"Advertencia ({lim_adv}°C)")
fig.add_hline(y=lim_crit, line_dash="dash", line_color="#7570b3", annotation_text=f"Crítico ({lim_crit}°C)")

fig.update_layout(
    yaxis_title="Temperatura (°C)",
    yaxis=dict(range=[0, max(120, temp_max + 20)]),
    template="plotly_white",
    margin=dict(t=30, b=30, l=30, r=30)
)

st.plotly_chart(fig, use_container_width=True)
