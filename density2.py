


import pandas as pd
import streamlit as st
import plotly.express as px

# Cargar datos
df = pd.read_excel("SiglasVida.xlsx", sheet_name='BASE')

# Semestres seleccionados
semestre_filter = st.multiselect("Select Semesters to Compare", df['Semestre'].unique())

# Filtro por VIDA_HOMOLOGACION (selección de valores específicos)
vida_homologacion_filter = st.multiselect("Select VIDA_HOMOLOGACION values", df['VIDA_HOMOLOGACION'].unique())

if semestre_filter:
    # Filtrar el DataFrame según los semestres seleccionados y los valores de VIDA_HOMOLOGACION
    filtered_df = df[(df['Semestre'].isin(semestre_filter)) & 
                     (df['VIDA_HOMOLOGACION'].isin(vida_homologacion_filter))]

    # Selección de paleta
    available_palettes = ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"]
    selected_palette = st.selectbox("Choose a color palette", available_palettes, index=0)  # Default: "deep"

    # Graficar
    sns.kdeplot(data=filtered_df, x='C1', hue='Semestre', shade=True, palette=selected_palette)
    plt.title(f"Density Plot for Semesters: {', '.join(map(str, semestre_filter))}")
    plt.xlabel("C1")
    plt.ylabel("Density")
    plt.legend(title="Semestre")
    st.pyplot(plt)

    # Resumen estadístico de los datos seleccionados
    describe_table = filtered_df.groupby('Semestre')['C1'].describe()
    st.write("### Statistical Summary by Semester")
    st.table(describe_table)
else:
    st.write("Please select at least one semester.")
