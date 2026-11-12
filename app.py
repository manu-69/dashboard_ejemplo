import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Dashboard interactivo de notas")

# 1. BARRA LATERAL (Para subir el archivo y filtrar)
st.sidebar.header("Datos y filtros")
archivo = st.sidebar.file_uploader("Carga el archivo CSV", type=['csv'])

if archivo is not None:
    # Leer el archivo que subiste
    df = pd.read_csv(archivo)
    
    # Crear los filtros en la barra lateral
    sexos = st.sidebar.multiselect("Sexo", df['Sexo'].unique(), df['Sexo'].unique())
    secciones = ['Todas'] + list(df['Sección'].unique())
    seccion = st.sidebar.selectbox("Sección", secciones)
    
    # 2. FILTRAR LOS DATOS (La lógica)
    # Aquí recortamos la tabla según lo que elijas en los filtros
    df_filtrado = df[df['Sexo'].isin(sexos)]
    
    if seccion != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Sección'] == seccion]

    # 3. ÁREA PRINCIPAL: MÉTRICAS (Los números grandes)
    col1, col2, col3 = st.columns(3)
    col1.metric("Estudiantes seleccionados", len(df_filtrado))
    col2.metric("Promedio general", round(df_filtrado['Promedio'].mean(), 2))
    
    aprobados = len(df_filtrado[df_filtrado['Promedio'] >= 4.0])
    col3.metric("Total de Aprobados", aprobados)

    # 4. GRÁFICO Y TABLA
    col_grafico, col_tabla = st.columns(2) # Divide la pantalla en 2
    
    with col_grafico:
        st.write("**Visualización de notas**")
        # Creamos el gráfico de barras
        fig, ax = plt.subplots()
        ax.bar(df_filtrado['Estudiante'], df_filtrado['Promedio'])
        ax.axhline(y=4.0, color='red', linestyle='--') # Línea roja de corte
        st.pyplot(fig) # Muestra el gráfico
        
    with col_tabla:
        st.write("**Estudiantes seleccionados**")
        # Muestra la tabla
        st.dataframe(df_filtrado, hide_index=True)
        
else:
    st.info("Sube tu archivo CSV en la barra de la izquierda para comenzar.")

