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
    
    # --- LA SOLUCIÓN AL ERROR ---
    # 1. Renombramos las columnas del CSV para que coincidan con los filtros y la tabla
    df = df.rename(columns={
        'estudiante': 'Estudiante',
        'sexo': 'Sexo',
        'seccion': 'Sección',
        'asistencia': 'Asistencia (%)'
    })
    
    # 2. Como tu archivo tiene nota_1 y nota_2, calculamos el Promedio
    df['Promedio'] = (df['nota_1'] + df['nota_2']) / 2
    # -----------------------------
    
    # Crear los filtros en la barra lateral
    sexos = st.sidebar.multiselect("Sexo", df['Sexo'].unique(), df['Sexo'].unique())
    secciones = ['Todas'] + list(df['Sección'].unique())
    seccion = st.sidebar.selectbox("Sección", secciones)
    
    # 2. FILTRAR LOS DATOS
    df_filtrado = df[df['Sexo'].isin(sexos)]
    
    if seccion != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Sección'] == seccion]

    # 3. ÁREA PRINCIPAL: MÉTRICAS
    col1, col2, col3 = st.columns(3)
    col1.metric("Estudiantes seleccionados", len(df_filtrado))
    col2.metric("Promedio general", round(df_filtrado['Promedio'].mean(), 2))
    
    aprobados = len(df_filtrado[df_filtrado['Promedio'] >= 4.0])
    col3.metric("Total de Aprobados", aprobados)

    # 4. GRÁFICO Y TABLA
    col_grafico, col_tabla = st.columns(2) 
    
    with col_grafico:
        st.write("**Visualización de notas**")
        fig, ax = plt.subplots()
        ax.bar(df_filtrado['Estudiante'], df_filtrado['Promedio'])
        ax.axhline(y=4.0, color='red', linestyle='--') # Línea roja de corte
        plt.xticks(rotation=45) # Gira los nombres un poco para que se lean mejor
        st.pyplot(fig) 
        
    with col_tabla:
        st.write("**Estudiantes seleccionados**")
        # Mostramos las columnas más importantes para que se vea limpio
        st.dataframe(df_filtrado[['Estudiante', 'Sexo', 'Sección', 'Promedio', 'Asistencia (%)']], hide_index=True)
        
else:
    st.info("Sube tu archivo CSV en la barra de la izquierda para comenzar.")



