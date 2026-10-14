import streamlit as st
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="Simulador Termofísico Industrial",
    layout="centered"
)

st.title("Simulador Termofísico Industrial")
st.markdown("Análisis directo de temperaturas por fases con diagnóstico normativo (Estándares NETA / IEC).")

# --- BARRA LATERAL: PARÁMETROS DE ENTRADA ---
st.sidebar.header("Parámetros de Entrada")

temp_ambiente = st.sidebar.number_input("Temperatura Ambiente (°C)", value=10.0, step=0.5)
tipo_equipo = st.sidebar.selectbox("Equipo", ["Disyuntor", "Contactor", "Transformador", "Motor"])

# Definir límites absolutos de temperatura según el tipo de equipo
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

# --- RESUMEN DE LECTURAS Y CÁLCULO DE DELTA T ---
st.subheader("Resumen de Lecturas y Desbalance")

temp_min = min(temp_r, temp_s, temp_t)
temp_max = max(temp_r, temp_s, temp_t)
delta_t_fases = temp_max - temp_min  # Salto térmico entre fases

col1, col2, col3, col4 = st.columns(4)
col1.metric("Fase R", f"{temp_r:.1f} °C")
col2.metric("Fase S", f"{temp_s:.1f} °C")
col3.metric("Fase T", f"{temp_t:.1f} °C")
col4.metric("ΔT Máximo", f"{delta_t_fases:.1f} °C")

# --- EVALUACIÓN NORMATIVA Y ALERTAS ---
st.subheader("Diagnóstico Normativo (Estándares NETA / Termografía)")

# 1. Evaluación por Salto Térmico (Delta T entre fases - Estándar NETA)
diagnostico_neta = ""
color_alerta = "success"

if delta_t_fases <= 3.0:
    diagnostico_neta = "🟢 **Condición Normal (NETA):** Diferencia menor a 3°C. Operación dentro de parámetros habituales."
    color_alerta = "success"
elif 4.0 <= delta_t_fases <= 15.0:
    diagnostico_neta = "🟡 **Anomalía Menor (NETA):** Diferencia entre 4°C y 15°C. Indicar seguimiento y programar revisión."
    color_alerta = "warning"
elif 16.0 <= delta_t_fases <= 40.0:
    diagnostico_neta = "🟠 **Anomalía Grave (NETA):** Diferencia entre 16°C y 40°C. Requiere reparación prioritaria por posible falso contacto."
    color_alerta = "error"
else:
    diagnostico_neta = "🔴 **Anomalía Crítica (NETA):** Diferencia mayor a 40°C. ¡Riesgo inminente de falla! Intervenir de inmediato."
    color_alerta = "error"

# 2. Evaluación por Temperatura Absoluta
diagnostico_abs = ""
if temp_max >= lim_crit:
    diagnostico_abs = f"⚠️ **Alerta Absoluta:** La temperatura máxima ({temp_max:.1f}°C) excede el límite crítico del equipo ({lim_crit}°C)."
elif temp_max >= lim_adv:
    diagnostico_abs = f"⚠️ **Aviso Absoluto:** La temperatura máxima ({temp_max:.1f}°C) supera el umbral de advertencia ({lim_adv}°C)."
else:
    diagnostico_abs = f"✅ **Temperatura Absoluta Normal:** Por debajo de los límites de diseño para un {tipo_equipo.lower()}."

# Mostrar alertas en la interfaz
if color_alerta == "success":
    st.success(diagnostico_neta)
elif color_alerta == "warning":
    st.warning(diagnostico_neta)
else:
    st.error(diagnostico_neta)

st.info(diagnostico_abs)

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

# Líneas de referencia de límites absolutos del equipo
fig.add_hline(y=lim_adv, line_dash="dash", line_color="orange", annotation_text=f"Límite Advertencia Equipo ({lim_adv}°C)")
fig.add_hline(y=lim_crit, line_dash="dash", line_color="red", annotation_text=f"Límite Crítico Equipo ({lim_crit}°C)")

fig.update_layout(
    yaxis_title="Temperatura (°C)",
    yaxis=dict(range=[0, max(120, temp_max + 20)]),
    template="plotly_white",
    margin=dict(t=30, b=30, l=30, r=30)
)

st.plotly_chart(fig, use_container_width=True)
