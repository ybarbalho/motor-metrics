import streamlit as st
import pandas as pd
import plotly.express as px

data = pd.read_csv('vehicles_us.csv')

st.header('Motor Metrics: vendas automotivas')

build_histogram = st.checkbox('Criar um histograma')
build_scatter = st.checkbox('Criar um gráfico de dispersão')

if build_histogram:
    st.write('Histograma por valor de Hodômetro')

    fig = px.histogram(data, x='odometer')

    st.plotly_chart(fig, use_container_width=True)

if build_scatter:
    st.write("Gráfico de dispersão para 'Hodômetro x Preço'")

    fig = px.scatter(data, x='odometer', y='price')

    st.plotly_chart(fig, use_container_width=True)
