


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
    available_palettes = ["Viridis", "Cividis", "Plasma", "Inferno", "Magma", "Turbo", "Ice"]
    selected_palette = st.selectbox("Choose a color palette", available_palettes, index=0)  # Default: "Viridis"

    # Graficar con Plotly
    fig = px.density_contour(
        filtered_df,
        x="C1",
        color="Semestre",
        marginal_x="histogram",
        title="Density Plot for Selected Semesters",
        template="plotly"
    )

    # Personalización de colores
    fig.update_layout(coloraxis_colorbar=dict(title="Semestre"),
                      title=dict(x=0.5),
                      template="plotly")

    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig)

    # Resumen estadístico de los datos seleccionados
    describe_table = filtered_df.groupby('Semestre')['C1'].describe()
    st.write("### Statistical Summary by Semester")
    st.table(describe_table)
else:
    st.write("Please select at least one semester.")
