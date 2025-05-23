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
    st.write('Frequência de veículos anunciados por milhas rodadas')

    fig = px.histogram(data, x='odometer', labels={
                       'odometer': 'Milhas rodadas', 'count': 'Total de veículos'})

    st.plotly_chart(fig, use_container_width=True)

# Gráfico de dispersão para observação dos dados.
build_scatter = st.checkbox('Criar um gráfico de dispersão')

if build_scatter:
    st.write('Distribuição dos anúncios de milhas rodadas por preço')

    fig = px.scatter(data, x='odometer', y='price', labels={
                     'odometer': 'Milhas rodadas', 'price': 'Preço do automóvel'})

    st.plotly_chart(fig, use_container_width=True)

st.subheader('Total de veículos por montadora')

# Gráfico de barras para observar a frequência das montadoras.
# Configurando o estado do botão
if 'model_viewer' not in st.session_state:
    st.session_state.model_viewer = False

# Definindo o texto do botão e invertendo o seu estado para ativo.
if st.button('Mostrar/ocultar montadoras'):
    st.session_state.model_viewer = not st.session_state.model_viewer

# Total de anúncios por montadora ordenados pela frequência.
if st.session_state.model_viewer:
    frequency_df = data['manufacturer'].value_counts().reset_index()
    frequency_df.columns = ['Montadoras', 'Frequência']

    fig = px.bar(frequency_df, x='Montadoras', y='Frequência')

    st.plotly_chart(fig, use_container_width=True)

st.subheader('Tipos de veículos por montadora')

# Agrupando as colunas de tipo por montadora e realizando a contagem.
car_data = data.groupby(['manufacturer', 'type'])[
    'price'].count().reset_index()
car_data.rename(columns={'price': 'count'}, inplace=True)

# Imprimindo seu gráfico de barras
fig = px.bar(car_data, x='manufacturer', y='count', color='type',
             barmode='stack', labels={'manufacturer': 'Montadoras'})
st.plotly_chart(fig, use_container_width=True)

st.subheader('Histograma de condição pelo ano do modelo')

# Histograma de condição pelo ano do modelo
fig = px.histogram(data, x='model_year', color='condition',
                   labels={'model_year': 'Ano do modelo'})
st.plotly_chart(fig, use_container_width=True)

st.subheader('Comparação de preço entre duas montadoras')

# Isolando os valores únicos de montadora.
unique_manufact = sorted(data['manufacturer'].unique())

# Criando duas caixas de seleção para comparar as montadoras.
selected_x1 = st.selectbox("Escolha uma montadora",
                           unique_manufact, index=unique_manufact.index('hyundai'))
selected_x2 = st.selectbox("Escolha a outra montadora",
                           unique_manufact, index=unique_manufact.index('volkswagen'))

# Copiando o dataframe de cada montadora selecionada.
data_x1 = data[data['manufacturer'] == selected_x1].copy()
data_x2 = data[data['manufacturer'] == selected_x2].copy()

# Concatenando os dados
data_x = pd.concat([data_x1, data_x2])

histnorm_check = st.checkbox('Histograma normalizado')

# Se ativado o checkbox, o histograma será normalizado por percentual. Caso contrário, será apresentada a frequência dos dados.
if histnorm_check:
    fig = px.histogram(data_x, x='price', color='manufacturer',
                       histnorm='percent', labels={'price': 'Intervalo de preço'})
    st.plotly_chart(fig, use_container_width=True)
else:
    fig = px.histogram(data_x, x='price', color='manufacturer',
                       labels={'price': 'Intervalo de preço'})
    st.plotly_chart(fig, use_container_width=True)
