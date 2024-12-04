import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------- Carga y preparación de datos ---------------------
# Panel_df
df3 = pd.read_excel(r"variable_cuali-cuanti.xlsx", sheet_name='PCA Com')
numerical_data = df3[['Cumplimiento %', 'Beca']]
scaler = StandardScaler()
scaled_data = scaler.fit_transform(numerical_data)
pca = PCA(n_components=1)
pca_result = pca.fit_transform(scaled_data)

panel_df = pd.DataFrame({
    'Fecha': pd.to_datetime(df3['Fecha'], errors='coerce'),
    'Correo': df3['Correo'],
    'Modalidad': df3['Modalidad'],
    'Periodo': df3['Periodo'],
    'Vigencia': df3['Vigencia'],
    'PCA1': pca_result.flatten()
})
panel_df['Año-Mes'] = panel_df['Fecha'].dt.to_period('M').astype(str)
panel_df['Mes'] = panel_df['Fecha'].dt.month_name()
panel_df['Año'] = panel_df['Fecha'].dt.year

# df
df = pd.read_excel(r"C:\Users\anthonydaniel.santi\Desktop\variable cuali-cuanti 2.xlsx", sheet_name='PCA Historico')

# --------------------- Configuración de filtros ---------------------
correos_unicos = ['Todos'] + panel_df['Correo'].dropna().unique().tolist()
meses_unicos = ['Todos'] + panel_df['Mes'].dropna().unique().tolist()
años_unicos = ['Todos'] + sorted(panel_df['Año'].dropna().unique().tolist())
vigencias_unicas = ['Todos'] + panel_df['Vigencia'].dropna().unique().tolist()
modalidades_unicas = ['Todos'] + panel_df['Modalidad'].dropna().unique().tolist()

modalidades_df_unicas = ['Todos'] + df['Modalidad'].dropna().unique().tolist()
correos_df_unicos = ['Todos'] + df['correo'].dropna().unique().tolist()
periodos_unicos = ['Todos'] + df['Periodo'].dropna().unique().tolist()

# --------------------- Interfaz de usuario en Streamlit ---------------------
st.title("Análisis Interactivo de Productividad")

# --------------------- Gráfico de Líneas ---------------------
st.header("Gráfico de Líneas - Productividad en el Tiempo")
correos_seleccionados = st.multiselect('Seleccionar Correos:', correos_unicos, default='Todos', key='correos_linea')
mes_seleccionado = st.selectbox('Seleccionar Mes:', meses_unicos, key='mes_linea')
año_seleccionado = st.selectbox('Seleccionar Año:', años_unicos, key='año_linea')
vigencia_seleccionada = st.selectbox('Seleccionar Vigencia:', vigencias_unicas, key='vigencia_linea')
modalidad_seleccionada = st.selectbox('Seleccionar Modalidad:', modalidades_unicas, key='modalidad_linea')

# Filtrar datos para el gráfico de líneas
datos_filtrados_lineas = panel_df.copy()
if modalidad_seleccionada != 'Todos':
    datos_filtrados_lineas = datos_filtrados_lineas[datos_filtrados_lineas['Modalidad'] == modalidad_seleccionada]
if mes_seleccionado != 'Todos':
    datos_filtrados_lineas = datos_filtrados_lineas[datos_filtrados_lineas['Mes'] == mes_seleccionado]
if año_seleccionado != 'Todos':
    datos_filtrados_lineas = datos_filtrados_lineas[datos_filtrados_lineas['Año'] == int(año_seleccionado)]
if vigencia_seleccionada != 'Todos':
    datos_filtrados_lineas = datos_filtrados_lineas[datos_filtrados_lineas['Vigencia'] == vigencia_seleccionada]

# Crear gráfico de líneas
if not datos_filtrados_lineas.empty:
    productividad_promedio = (
        datos_filtrados_lineas.groupby('Año-Mes')['PCA1']
        .mean()
        .reset_index()
        .sort_values(by='Año-Mes')
    )

    plt.figure(figsize=(12, 6))
    plt.plot(productividad_promedio['Año-Mes'], productividad_promedio['PCA1'], label='Productividad Promedio', color='green', linewidth=2)

    if 'Todos' not in correos_seleccionados:
        for correo in correos_seleccionados:
            datos_correo = datos_filtrados_lineas[datos_filtrados_lineas['Correo'] == correo]
            if not datos_correo.empty:
                datos_correo = datos_correo.sort_values(by='Fecha')
                plt.plot(
                    datos_correo['Año-Mes'],
                    datos_correo['PCA1'],
                    label=f'Productividad de {correo}',
                    linewidth=2
                )

    plt.xlabel('Año-Mes')
    plt.ylabel('Productividad (PCA1)')
    plt.title('Productividad: Promedio y Correos Seleccionados')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt.gcf())
else:
    st.write("No hay datos para los filtros seleccionados.")

# --------------------- Diagrama de Gauss ---------------------
st.header("Diagrama de Gauss - Distribución de PCA")
modalidad_df_seleccionada = st.selectbox('Seleccionar Modalidad:', modalidades_df_unicas, key='modalidad_gauss')
correos_df_seleccionados = st.multiselect('Seleccionar Correos:', correos_df_unicos, default='Todos', key='correos_gauss')
periodo_seleccionado = st.selectbox('Seleccionar Periodo:', periodos_unicos, key='periodo_gauss')

# Filtrar datos para el diagrama de Gauss
datos_filtrados_gauss = df.copy()
if modalidad_df_seleccionada != 'Todos':
    datos_filtrados_gauss = datos_filtrados_gauss[datos_filtrados_gauss['Modalidad'] == modalidad_df_seleccionada]
if periodo_seleccionado != 'Todos':
    datos_filtrados_gauss = datos_filtrados_gauss[datos_filtrados_gauss['Periodo'] == periodo_seleccionado]

# Crear gráfico de Gauss
if not datos_filtrados_gauss.empty:
    estadisticas = datos_filtrados_gauss['PCA'].describe()
    media = estadisticas['mean']
    std_dev = estadisticas['std']

    plt.figure(figsize=(14, 8))
    sns.kdeplot(data=datos_filtrados_gauss, x='PCA', fill=True, color='skyblue', alpha=0.7)

    plt.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Media (PCA) = {media:.2f}')
    if not pd.isna(std_dev):
        plt.axvline(media - std_dev, color='white', linestyle='--', linewidth=1.5, label=f'-1 STD = {media - std_dev:.2f}')
        plt.axvline(media + std_dev, color='white', linestyle='--', linewidth=1.5, label=f'+1 STD = {media + std_dev:.2f}')

    if 'Todos' not in correos_df_seleccionados:
        for correo in correos_df_seleccionados:
            datos_correo = datos_filtrados_gauss[datos_filtrados_gauss['correo'] == correo]
            if not datos_correo.empty:
                pca_correo = datos_correo['PCA'].mean()
                plt.axvline(pca_correo, linestyle='-', linewidth=2, label=f'{correo} = {pca_correo:.2f}')

    plt.title('Distribución de PCA')
    plt.xlabel('Valores de PCA')
    plt.ylabel('Densidad')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    st.pyplot(plt.gcf())
else:
    st.write("No hay datos para los filtros seleccionados.")
