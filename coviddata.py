import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import pydeck

#@st.cache_data
def cargar_contagios():
    data = pd.read_excel('streamlitcovid.xlsx', sheet_name='contagios')
    return data

#@st.cache_data
def cargar_departamento():
    data = pd.read_excel('streamlitcovid.xlsx', sheet_name='departamento')
    return data

df_contagios = cargar_contagios()
df_departamento = cargar_departamento()

#Creacipn de DataFrame
df_join = df_contagios.join(df_departamento.set_index('departamento'), on='departamento', validate='m:1')
df_join['fecha_diagnostico'] = df_join['fecha_diagnostico'].str[:10]
df_join['fecha_muerte'] = df_join['fecha_muerte'].str[:10]
st.write(df_join)

#KPI
confirmados = df_join.id_de_caso.count()
recuperados = (df_join['recuperado'] ==
'Recuperado').sum()
fallecidos = (df_join['recuperado'] == 'Fallecido').sum()
col1, col2, col3 = st.columns(3)
col1.metric(label="Casos confirmados", value=confirmados)
col2.metric(label="Recuperados", value=recuperados)
col3.metric(label="Fallecidos", value=fallecidos)

#Gráfico de líneas
df_contagios_fecha = df_join.groupby(['fecha_diagnostico']).count()['id_de_caso']
with st.container():
    st.header('Contagios x Fecha')
    st.line_chart(df_contagios_fecha)

#Gráfico de líneas 2
df_fallecidos = df_join[df_join['recuperado'] == 'Fallecido']
df_fallecidos_fecha = df_fallecidos.groupby(['fecha_muerte']).count()['id_de_caso']

with st.container():
    st.header('Fallecidos x Fecha')
    fig, ax = plt.subplots()
    ax.plot(df_fallecidos_fecha)
    ax.set_title('Fallecidos')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Cantidad')
    ax.tick_params(axis='x', labelrotation=90, labelsize=6)
    st.pyplot(fig)

#Gráfico de barras apiladas

df_fallecidos_departamento = df_fallecidos.groupby(['departamento_nom']).count()['id_de_caso']

with st.container():
    st.header('Fallecidos x Departamento')
    fig, ax = plt.subplots()
    df_fallecidos_departamento.sort_values().plot(kind='barh', ax=ax)
    ax.set_xlabel('Cantidad')
    ax.set_ylabel('Departamento')
    st.pyplot(fig)

#Gráfico de Torta
df_contagios_sexo = df_join.groupby(['sexo']).id_de_caso.count()

fig, ax = plt.subplots()
ax.pie(df_contagios_sexo, labels=df_contagios_sexo.index, autopct='%1.1f%%')

with st.container():
    st.header('Contagios por Sexo')

st.pyplot(fig)

#Histograma
fig, ax = plt.subplots()
ax.hist(df_join['edad'])
with st.container(border=True):
    st.header('Histograma por edades')
st.pyplot(fig)


# Mapa de contagios original
df_contagios_departamento_mapa = df_join.groupby(by=['departamento_nom', 'latitud', 'longitud'], as_index=False).id_de_caso.count()

df_contagios_departamento_mapa['size'] = df_contagios_departamento_mapa['id_de_caso'] * 300

with st.container():
    st.header('Mapa de contagios')
    st.map(df_contagios_departamento_mapa, latitude='latitud', longitude='longitud', size='size')


#Mapa de contagios - Pydeck (fondo negro)

# Agrupación de los datos
df_contagios_departamento_mapa = df_join.groupby(
    by=['departamento_nom', 'latitud', 'longitud'], as_index=False).id_de_caso.count()

# Cálculo del tamaño de los puntos en el mapa
df_contagios_departamento_mapa['size'] = df_contagios_departamento_mapa['id_de_caso'] * 300

# Creación de la capa para el mapa
capas = pydeck.Layer(
    "ScatterplotLayer",
    data=df_contagios_departamento_mapa,
    get_position=["longitud", "latitud"],
    get_color=[255, 75, 75],  # Definición correcta del color en formato de lista
    pickable=True,
    auto_highlight=True,
    get_radius="size",
)

# Definición del estado de la vista inicial del mapa
vista_inicial = pydeck.ViewState(
    latitude=4,
    longitude=-74,
    zoom=4.5,
)

# Renderización del mapa en Streamlit
st.pydeck_chart(pydeck.Deck(
    layers=[capas],
    initial_view_state=vista_inicial,
))


#Mapa de Contagios - Pydeck (color original - claro)

with st.container(border=True):
    st.header('Mapa de contagios')
    st.pydeck_chart(
        pydeck.Deck(
            layers=capas,
            map_style=None,
            initial_view_state=vista_inicial, tooltip={"text":"{departamento_nom}\nContagios: {id_de_caso}"}
            ))