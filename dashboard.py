import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.latex(
    r"""
    A \sin[B \left( x + C \right)] + D
"""
)

A = st.sidebar.slider("A", 1.0, 4.0)
B = st.sidebar.slider("B", 1.0, 8.0)
C = st.sidebar.slider("C", 0.0, np.pi)
D = st.sidebar.slider("D", -4.0, 4.0, 0.0)

x = np.linspace(0, 2 * np.pi, 1000)
y = A * np.sin(B * (x + C)) + D

fig = go.Figure(data=go.Scatter(x=x, y=y))
fig.update_xaxes(range=[0.0, 2 * np.pi])
fig.update_yaxes(range=[-4, 4])
st.plotly_chart(fig, use_container_width=True)
