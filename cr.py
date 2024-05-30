import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Cargar los datos
df = pd.read_excel(r"C:\Users\mauricioalejandro.01\OneDrive - Universidad de Las Américas\Documentos\ASISTENTE DE PROYECTOS\Analisis Carreras\Datos_limpios_CR.xlsx")
st.write("****ELASTICIDAD CR****")
st.write("---")

df['Periodo'] = df['Periodo'].astype(str)
st.write(df)

# Crear una barra lateral para los filtros
st.sidebar.subheader("Filtros")

# Filtro por MARCA
marca = st.sidebar.selectbox('Selecciona Marca', df['MARCA'].unique())

# Filtrar el DataFrame basado en la MARCA seleccionada
filtered_df_marca = df[df['MARCA'] == marca]

# Filtro por SEDE (permitiendo múltiples selecciones)
sede = st.sidebar.multiselect('Selecciona Sede', filtered_df_marca['SEDE'].unique())

# Filtrar el DataFrame basado en la MARCA y las SEDEs seleccionadas
filtered_df_sede = filtered_df_marca[filtered_df_marca['SEDE'].isin(sede)]

# Filtro por LLAVE (Carrera) permitiendo múltiples selecciones
carrera = st.sidebar.multiselect('Selecciona Carrera', filtered_df_sede['LLAVE'].unique())

# Filtrar el DataFrame basado en la MARCA, SEDEs y CARRERAs seleccionadas
filtered_df_carrera = filtered_df_sede[filtered_df_sede['LLAVE'].isin(carrera)]

# Filtro por Periodo
periodo = st.sidebar.multiselect('Selecciona Periodo', filtered_df_carrera['Periodo'].unique())

# Filtrar el DataFrame basado en la MARCA, SEDEs, CARRERAs y Periodo seleccionados
filtered_df = filtered_df_carrera[filtered_df_carrera['Periodo'].isin(periodo)]

# Calcular el valor máximo (absoluto) para los ejes x e y basado en el DataFrame filtrado
max_abs_x_value = max(abs(filtered_df['Delta_Precio'].max()), abs(filtered_df['Delta_Precio'].min()))
max_abs_y_value = max(abs(filtered_df['Delta_Cantidad'].max()), abs(filtered_df['Delta_Cantidad'].min()))

# Obtener el máximo de los valores absolutos de los ejes para garantizar que (0,0) esté en el centro del gráfico
max_range = max(max_abs_x_value, max_abs_y_value)

# Establecer el rango máximo para los ejes x e y en el gráfico, centrado en (0,0)
x_range = [-max_range, max_range]
y_range = [-max_range, max_range]

# Crear el gráfico scatter de Plotly con los datos filtrados y el rango de ejes establecido
fig = px.scatter(filtered_df, x='Delta_Precio', y='Delta_Cantidad', color='Periodo', title=f'Elasticidad ({", ".join(sede)}, {", ".join(carrera)})', size='Valor_total')

fig.update_xaxes(range=x_range)
fig.update_yaxes(range=y_range)

# Agregar líneas verticales y horizontales para el plano cartesiano en (0,0)
fig.add_shape(type="line", x0=0, y0=y_range[0], x1=0, y1=y_range[1], line=dict(color="black", width=1))
fig.add_shape(type="line", x0=x_range[0], y0=0, x1=x_range[1], y1=0, line=dict(color="black", width=1))

# Añadir flechas para mostrar el movimiento de las carreras
for i in range(1, len(filtered_df)):
    x_start = filtered_df.iloc[i - 1]['Delta_Precio']
    y_start = filtered_df.iloc[i - 1]['Delta_Cantidad']
    x_end = filtered_df.iloc[i]['Delta_Precio']
    y_end = filtered_df.iloc[i]['Delta_Cantidad']
    arrow_text = filtered_df.iloc[i]['LLAVE']
    fig.add_trace(go.Scatter(x=[x_start, x_end], y=[y_start, y_end], mode='lines+markers+text', name=arrow_text,
                             line=dict(color='black', width=1),
                             marker=dict(symbol='arrow', color='black', size=10),
                             text=[arrow_text, ''], textposition='top right', textfont=dict(size=8)))

# Configuración del diseño del gráfico
fig.update_layout(
    title=f'Elasticidad ({", ".join(sede)}, {", ".join(carrera)})',
    xaxis=dict(title='Delta_Precio'),
    yaxis=dict(title='Delta_Cantidad'),
    width=1500,  # Ancho del gráfico en píxeles
    height=600   # Alto del gráfico en píxeles
)

# Mostrar el gráfico
st.plotly_chart(fig)

