import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title for the Streamlit app
st.title("EVOLUCIÓN CARRERAS HISTÓRICO")

# Load data
@st.cache_data
def load_data():
    dfhc = pd.read_excel(r"C:\Users\mauricioalejandro.01\OneDrive - Universidad de Las Américas\Documentos\ANALISTA DE PROYECTOS\Facu.xlsx", sheet_name='Cabezas')
    dfht = pd.read_excel(r"C:\Users\mauricioalejandro.01\OneDrive - Universidad de Las Américas\Documentos\ANALISTA DE PROYECTOS\Facu.xlsx", sheet_name='Ticket')
    dfhv = pd.read_excel(r"C:\Users\mauricioalejandro.01\OneDrive - Universidad de Las Américas\Documentos\ANALISTA DE PROYECTOS\Facu.xlsx", sheet_name='variacion')
    return dfhc, dfht, dfhv

# Read data
dfhc, dfht, dfhv = load_data()

# Data transformation
dfc = pd.melt(dfhc, id_vars=['Modalidad','Facultad','Carrera'], value_vars=[202010,202110,202210,202310,202410,202510], var_name='Periodo', value_name='Documentados')
dft = pd.melt(dfht, id_vars=['Modalidad','Facultad','Carrera'], value_vars=[202010,202110,202210,202310,202410,202510], var_name='Periodo', value_name='Ticket')
dfv = pd.melt(dfhv, id_vars=['Modalidad','Facultad','Carrera'], value_vars=[202110,202210,202310,202410,202510], var_name='Periodo', value_name='variacion')

# Transform Periodo to str
dfc['Periodo'] = dfc['Periodo'].astype(str)
dft['Periodo'] = dft['Periodo'].astype(str)
dfv['Periodo'] = dfv['Periodo'].astype(str)

# Create 'Llave' column
dfc['Llave'] = dfc['Modalidad'] + dfc['Facultad'] + dfc['Carrera'] + dfc['Periodo']
dft['Llave'] = dft['Modalidad'] + dft['Facultad'] + dft['Carrera'] + dft['Periodo']
dfv['Llave'] = dfv['Modalidad'] + dfv['Facultad'] + dfv['Carrera'] + dfv['Periodo']

# Left join
df = pd.merge(dfc, dft[['Llave', 'Ticket']], how='left', on='Llave')
df = pd.merge(df, dfv[['Llave', 'variacion']], how='left', on='Llave')

# Filters
facultades = df['Facultad'].unique()
carreras = df['Carrera'].unique()
modalidades = df['Modalidad'].unique()
columns = ['Documentados', 'Ticket', 'variacion']

# Select column to view
selected_column = st.selectbox('Select Column to View:', columns)

# Facultad Graph
st.header("Facultad Graph")
selected_facultades = st.multiselect('Select Facultad:', facultades, default=facultades)
selected_modalidades_facultad = st.multiselect('Select Modalidad for Facultad:', modalidades, default=modalidades)

# Filter data based on selected facultades and modalidades
filtered_df_facultad = df[(df['Facultad'].isin(selected_facultades)) & 
                          (df['Modalidad'].isin(selected_modalidades_facultad))]

# Aggregate data to get mean values for Facultad
mean_facultad = filtered_df_facultad.groupby(['Facultad', 'Periodo'])[selected_column].mean().reset_index()

# Display Facultad plot
if not mean_facultad.empty:
    st.write(f"Line Plot of {selected_column} by Periodo for Selected Facultad")
    fig_facultad, ax_facultad = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=mean_facultad, x='Periodo', y=selected_column, hue='Facultad', style='Facultad', markers=True, dashes=False, ax=ax_facultad)
    plt.xticks(rotation=45)
    plt.title(f'{selected_column} by Periodo for Facultad')
    plt.xlabel('Periodo')
    plt.ylabel(selected_column)
    plt.legend(title='Facultad')
    st.pyplot(fig_facultad)

# Carrera Graph
st.header("Carrera Graph")
selected_carreras = st.multiselect('Select Carrera:', carreras, default=carreras)
selected_modalidades_carrera = st.multiselect('Select Modalidad for Carrera:', modalidades, default=modalidades)

# Filter data based on selected carreras and modalidades
filtered_df_carrera = df[(df['Carrera'].isin(selected_carreras)) & 
                          (df['Modalidad'].isin(selected_modalidades_carrera))]

# Aggregate data to get mean values for Carrera
mean_carrera = filtered_df_carrera.groupby(['Carrera', 'Periodo'])[selected_column].mean().reset_index()

# Display Carrera plot
if not mean_carrera.empty:
    st.write(f"Line Plot of {selected_column} by Periodo for Selected Carrera")
    fig_carrera, ax_carrera = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=mean_carrera, x='Periodo', y=selected_column, hue='Carrera', style='Carrera', markers=True, dashes=False, ax=ax_carrera)
    plt.xticks(rotation=45)
    plt.title(f'{selected_column} by Periodo for Carrera')
    plt.xlabel('Periodo')
    plt.ylabel(selected_column)
    plt.legend(title='Carrera')
    st.pyplot(fig_carrera)


# Tables
df_d=pd.read_excel(r"C:\Users\mauricioalejandro.01\OneDrive - Universidad de Las Américas\Documentos\ANALISTA DE PROYECTOS\Documentados.xlsx",sheet_name='Documentados')
df_a=pd.read_excel(r"C:\Users\mauricioalejandro.01\OneDrive - Universidad de Las Américas\Documentos\ANALISTA DE PROYECTOS\Documentados.xlsx",sheet_name='Afluencias')



# Función para formatear todos los valores como porcentaje
def formatear_como_porcentaje(df):
    df_formateado = df.copy()
    for column in df_formateado.columns:
        if df_formateado[column].dtype in ['float64', 'int64']:
            df_formateado[column] = df_formateado[column].apply(lambda x: f"{x * 100:.2f}%")
    return df_formateado

# Función para aplicar el formato condicional a la columna 'Variacion'
def resaltar_variacion(val):
    try:
        val = float(val.rstrip('%'))  # Quitar '%' y convertir a float
        color = 'green' if val > 0 else 'red'
        return f'color: {color}'
    except ValueError:
        return ''

# Filtrar datos por Carrera
def filtrar_por_carrera(df, carrera):
    return df[df['DescPrograma'] == carrera]

# Mostrar el filtro de Carrera
carrera_opciones = df_d['DescPrograma'].unique()  # Obtener opciones únicas de Carrera
carrera_seleccionada = st.selectbox('Selecciona una Carrera', carrera_opciones)

# Filtrar los DataFrames originales
df_d_filtrado = filtrar_por_carrera(df_d, carrera_seleccionada)
df_a_filtrado = filtrar_por_carrera(df_a, carrera_seleccionada)

# Formatear todos los valores como porcentaje después de filtrar
df_d_formateado = formatear_como_porcentaje(df_d_filtrado)
df_a_formateado = formatear_como_porcentaje(df_a_filtrado)

# Aplicar el formato condicional solo a la columna 'Variacion'
df_d_styled = df_d_formateado.style.applymap(resaltar_variacion, subset=['Variacion'])
df_a_styled = df_a_formateado.style.applymap(resaltar_variacion, subset=['Variacion'])

# Mostrar las tablas en Streamlit
st.write(f"Documentados - {carrera_seleccionada}")
st.write(df_d_styled)
st.write(f"Afluencias - {carrera_seleccionada}")
st.write(df_a_styled)