import streamlit as st
import pandas as pd
import plotly.express as px

data = pd.read_csv('vehicles_us.csv')

st.header('Motor Metrics: vendas automotivas')

build_histogram = st.checkbox('Criar um histograma de vendas')
build_scatter = st.checkbox('Criar um gráfico de dispersão')

if build_histogram:
    st.write('Histograma por Milhas rodadas')

    fig = px.histogram(data, x='odometer', labels={
                       'odometer': 'Milhas rodadas', 'count': 'Total de veículos'})

    st.plotly_chart(fig, use_container_width=True)

if build_scatter:
    st.write("Gráfico de dispersão de 'Milhas rodadas x Preço'")

    fig = px.scatter(data, x='odometer', y='price', labels={
                     'odometer': 'Milhas rodadas', 'price': 'Preço do automóvel'})

    st.plotly_chart(fig, use_container_width=True)
