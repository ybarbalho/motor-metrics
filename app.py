import streamlit as st
import pandas as pd
import plotly.express as px

# Importando os dados
data = pd.read_csv('vehicles_us.csv')

# Criando uma coluna de montadoras para observação.
data['manufacturer'] = data['model'].str.split().str[0]

st.title('Motor Metrics: vendas automotivas')

st.header('Visualização dos dados')

# Filtragem dos dados por meio do preço dos automóveis.
filter_view = st.slider('Filtrar o valor do anúncio:', 0,
                        data['price'].max(), (50000, 100000))

data_filtered = data[(data['price'] >= filter_view[0]) &
                     (data['price'] <= filter_view[1])]

st.write(data_filtered)

# Histograma para observação dos dados por 'odometer'.
build_histogram = st.checkbox('Criar um histograma de vendas')

if build_histogram:
    st.write('Histograma por Milhas rodadas')

    fig = px.histogram(data, x='odometer', labels={
                       'odometer': 'Milhas rodadas', 'count': 'Total de veículos'})

    st.plotly_chart(fig, use_container_width=True)

# Gráfico de dispersão para observação dos dados.
build_scatter = st.checkbox('Criar um gráfico de dispersão')

if build_scatter:
    st.write("Gráfico de dispersão de 'Milhas rodadas x Preço'")

    fig = px.scatter(data, x='odometer', y='price', labels={
                     'odometer': 'Milhas rodadas', 'price': 'Preço do automóvel'})

    st.plotly_chart(fig, use_container_width=True)

st.header('Total de veículos por montadora')

# Gráfico de barras para observar a frequência das montadoras.
model_viewer = st.button('Visualizar montadoras')

if model_viewer:
    frequency_df = data['manufacturer'].value_counts().reset_index()
    frequency_df.columns = ['Montadora', 'Frequência']

    fig = px.bar(frequency_df, x='Montadora', y='Frequência')

    st.plotly_chart(fig, use_container_width=True)
