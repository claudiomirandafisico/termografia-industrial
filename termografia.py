import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Simulador Termofisico Industrial", layout="wide"
)

# Estilo visual limpio y profesional (fuente tipografica y margenes)
st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main {
        background-color: #f8f9fa;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("Simulador Termofisico Industrial")
st.write(
    "Modelo de temperatura por fases y analisis grafico para equipos"
    " electricos."
)

st.sidebar.header("Parametros de Entrada")

t_amb = st.sidebar.slider(
    "Temperatura Ambiente (C)", min_value=10.0, max_value=50.0, value=25.0
)
equipo = st.sidebar.selectbox(
    "Equipo",
    ["Disyuntor", "Contactor", "Guardamotor", "Rele Termico", "Motor", "Variador"],
)
carga = st.sidebar.slider("Carga Operativa (%)", min_value=10, max_value=120, value=75)

st.sidebar.subheader("Desbalance por Fase")
fase_r = st.sidebar.slider("Fase R (Delta C)", 0.0, 50.0, 2.0)
fase_s = st.sidebar.slider("Fase S (Delta C)", 0.0, 50.0, 15.0)
fase_t = st.sidebar.slider("Fase T (Delta C)", 0.0, 50.0, 2.0)

base = {
    "Disyuntor": 35.0,
    "Contactor": 40.0,
    "Guardamotor": 38.0,
    "Rele Termico": 42.0,
    "Motor": 55.0,
    "Variador": 45.0,
}

t_base = base[equipo] + (carga / 100.0) * 15.0

tr = t_amb + t_base + fase_r
ts = t_amb + t_base + fase_s
tt = t_amb + t_base + fase_t
t_max = max(tr, ts, tt)

st.subheader("Resumen de Lecturas")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Fase R", f"{tr:.1f} C")
c2.metric("Fase S", f"{ts:.1f} C")
c3.metric("Fase T", f"{tt:.1f} C")
c4.metric("Maxima", f"{t_max:.1f} C")

if t_max > 85.0:
    st.error("Estado critico: Temperatura superior al limite admisible.")
elif t_max > 70.0:
    st.warning("Estado moderado: Requiere revision preventiva.")
else:
    st.success("Estado normal.")

st.subheader("Plano Cartesiano de Temperaturas por Fase")

# Grafico de barras estilo plano cartesiano limpio
fases = ["Fase R", "Fase S", "Fase T", "Ambiente"]
temperaturas = [tr, ts, tt, t_amb]
colores = ["#1f77b4", "#d62728", "#2ca02c", "#7f7f7f"]

fig = go.Figure(
    data=[
        go.Bar(
            x=fases,
            y=temperaturas,
            marker_color=colores,
            text=[f"{t:.1f} C" for t in temperaturas],
            textposition="auto",
        )
    ]
)

fig.update_layout(
    xaxis=dict(title="Componentes del Sistema", linecolor="black", linewidth=1),
    yaxis=dict(
        title="Temperatura (°C)",
        range=[0, max(100, t_max + 15)],
        linecolor="black",
        linewidth=1,
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor="black",
    ),
    plot_bgcolor="white",
    paper_bgcolor="white",
    height=450,
    margin=dict(l=40, r=40, t=40, b=40),
)

st.plotly_chart(fig, width="stretch")