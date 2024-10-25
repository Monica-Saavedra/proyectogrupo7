# Importación de las librerias

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime

# Importar archivo de BD en formato .CSV

df = pd.read_csv('BD_energiasrenovables.csv')

# Obtenemos las 5 primeras líneas para dar una visión inicial al DataFrame

df.head()

# Obtenemos las 5 últimas líneas para dar una visión final al DataFrame

df.tail()

# validamos que la data no posea datos nulos o información faltante Adicionalmente, se vincula otra función df.to_string para visualizar todos los datos en forma de cadena de texto
print(df.info())
print(df.to_string())

df.at[134, 'Municipio'] = 'MONTELÍBANO'
df.at[147, 'Municipio'] = 'OCAÑA'
df.at[152, 'Municipio'] = 'MONTELÍBANO'
df.at[153, 'Municipio'] = 'BUGA'
df.at[154, 'Municipio'] = 'BUGA'
print(df)

print(df.info())
print(df.to_string())

df.to_csv('BD_energiasrenovables1.csv', index=False)
print("Base de datos exportada exitosamente a BD_energiasrenovables1.csv")

#Se procede a describir el contenido de la Base de Datos, específicamente, obtenemos la Estadística Descriptiva para realizar el Análisis Descriptivo

df.describe()

#Se ordena ordena + filtra + uso de la función suma de inversión estimada en $COP

ord_inversion = df.sort_values("Inversión estimada [COP]")
print(ord_inversion.to_string())
suma_inversion = df["Inversión estimada [COP]"].sum()
print(f'La suma total de inversión en Proyectos en $ es: {suma_inversion}')

#Se ordena la columna de Empleos Estimados + eliminación de Filas duplicadas. Anteriormente, eran 158 en total y quedaron 156 registros o filas

ord_empleos = df.sort_values("Empleos estimados")
print(ord_empleos.to_string())
df_clean = df.drop_duplicates()
print(df_clean)

#Se utiliza la función suma para obtener el total de Empleos por la totalidad de los Proyectos

empleos_estimados = df["Empleos estimados"].sum()
print(f'La cuenta total de empleos es: {empleos_estimados}')

#Gráfico de Barras = Eje X = Tipo de Proyecto VS Eje Y = Cantidad
# Agrupar por 'Tipo' y contar la columna 'Capacidad'
df_tipo = df.groupby(["Tipo"]).count()["Capacidad"]
print(df_tipo)


# Crear el gráfico de barras
ax = df_tipo.plot(title="Proyectos de Energías Renovables", xlabel="Tipo", ylabel="Cantidad", kind="bar")

# Agregar etiquetas a cada barra
for i, value in enumerate(df_tipo):
    ax.text(i, value, str(value), ha='center', va='bottom', fontsize=10)

# Mostrar el gráfico
plt.tight_layout()
plt.show()

#Diagrama de Dispersión = Correlación entre Departamento VS Capacidad Instalada en MW (Megavatios) de cada Proyecto

df.plot(xlabel="Capacidad", ylabel="Departamento", kind="scatter", x="Capacidad", y="Departamento")

#Histograma = Cantidad de Usuarios VS Frecuencia

df["Usuarios"].plot(ylabel="Frecuencia", kind="hist")

#Gráfico de Torta = % por Tipo de Proyecto: Solar 91,8% VS Eólica 8,2%

df_tipo = df.groupby(["Tipo"]).count()["Código Departamento"]
print(df_tipo)
df_tipo.plot(kind="pie", title="% por Tipo de Proyecto Renovable", ylabel="",autopct="%1.1f%%")

#Gráfico de Líneas = Fecha de inicio de operación VS Energía estimada que produce la central en kWh/día

df_ordenado = df.sort_values("Fecha estimada FPO")
df_group_fecha = df_ordenado.groupby(["Fecha estimada FPO"]).count()["Energía [kWh/día]"]
print(df_group_fecha.to_string())
df_group_fecha.plot(title="Fecha estimada de operación", xlabel="Fecha", ylabel="Energía [kWh/día]")

#Gráfico de Barras = Eje X = Departamentos VS Eje Y = Empleos generados

# Agrupación por departamento y conteo de empleos estimados
df_tipo = df.groupby(['Departamento']).count()['Empleos estimados']
print(df_tipo)

# Creación del gráfico de barras
df_tipo.plot(title="Empleos estimados por cada Departamento", xlabel='Departamento', ylabel='Empleos estimados', kind='bar')

# Asignación de etiquetas para cada barra
for i in range(len(df_tipo)):
    plt.text(i, df_tipo[i], str(int(df_tipo[i])), ha='center', va='bottom', color='black', fontsize=10)

# Ajuste de diseño y muestra de la figura
plt.tight_layout()
plt.show()

#Gráficas con streamlit
# Título de la aplicación
st.title("Análisis de Proyectos de Energías Renovables")

# Mostrar datos en un DataFrame
st.subheader("Datos de Proyectos")
st.dataframe(df)

# Suma total de inversión
suma_inversion = df["Inversión estimada [COP]"].sum()
st.write(f"La suma total de inversión en Proyectos es: {suma_inversion}")

# Gráfico de barras de Inversión estimada por Tipo de Proyecto

st.subheader("Inversión estimada por Tipo de Proyecto")
inversion_por_tipo = df.groupby("Tipo")["Inversión estimada [COP]"].sum()
fig, ax = plt.subplots()
inversion_por_tipo.plot(kind='bar', ax=ax)
st.pyplot(fig)


# Gráfico de torta de Porcentaje por Tipo de Proyecto
st.subheader("Porcentaje por Tipo de Proyecto")
porcentaje_por_tipo = df["Tipo"].value_counts()
fig, ax = plt.subplots()
ax.pie(porcentaje_por_tipo, labels=porcentaje_por_tipo.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  
st.pyplot(fig)

# Gráfico de barras de Empleos estimados por Departamento
st.subheader("Empleos estimados por Departamento")
empleos_por_departamento = df.groupby("Departamento")["Empleos estimados"].sum()
st.bar_chart(empleos_por_departamento)

#gráfico de dispersion relación inversión vs empleos estimados por Departamento

st.subheader("Relación Inversión vs Empleos por Departamento")
fig, ax = plt.subplots()
df.plot(kind='scatter', x='Empleos estimados', y='Inversión estimada [COP]', ax=ax)
st.pyplot(fig)

# Gráfico de barras de Código Departamento vs Capacidad Instalada en MW

st.subheader("Código Departamento vs Capacidad Instalada en MW")
capacidad_por_departamento = df.groupby("Código Departamento")["Capacidad"].sum()
st.bar_chart(capacidad_por_departamento)