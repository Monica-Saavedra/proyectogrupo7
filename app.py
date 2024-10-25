import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
df = pd.DataFrame({
'fruta': ['manzana', 'fresa', 'banano'],
'cantidad': [10, 15, 8]
})
st.header('DataFrame')
st.write(df)
st.header('Gráfico de líneas')
st.line_chart(df, x='fruta', y='cantidad')
st.header('Gráfico de barras')
st.bar_chart(df, x='fruta', y='cantidad')

df2 = pd.DataFrame({
'departamento': ['Antioquia', 'Caldas', 'Risaralda'],
'latitud': [6.702, 5.280, 5.240],
'longitud': [-75.504, -75.274, -76.002],
'cantidad': [100, 150, 80]
})
df2['tamano'] = df2.cantidad * 100
st.write(df)
st.map(df2, latitude='latitud', longitude='longitud',
size='tamano')