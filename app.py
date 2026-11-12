import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard de Notas", layout="wide")

# Generación de datos de prueba (mock data) para igualar la imagen
@st.cache_data
def load_mock_data():
    data = {
        'ID': ['E01', 'E02', 'E03', 'E04', 'E05', 'E06', 'E07', 'E08', 'E09', 'E10', 'E11', 'E12'],
        'Estudiante': ['Ana', 'Luis', 'Sofia', 'Diego', 'Marta', 'Pedro', 'Julia', 'Juan', 'Lucia', 'Andres', 'Camila', 'Tomas'],
        'Sexo': ['Mujer', 'Hombre', 'Mujer', 'Hombre', 'Mujer', 'Hombre', 'Mujer', 'Hombre', 'Mujer', 'Hombre', 'Mujer', 'Hombre'],
        'Sección': ['A', 'A', 'A', 'B', 'B', 'B', 'A', 'A', 'B', 'B', 'A', 'B'],
        'Promedio': [6.3, 3.2, 4.8, 3.5, 6.6, 5.6, 3.8, 6.1, 4.1, 6.3, 4.6, 6.0],
        'Asistencia (%)': [95, 80, 92, 70, 98, 85, 90, 88, 96, 75, 82, 94]
    }
    return pd.DataFrame(data)

df = load_mock_data()

# 2. Barra lateral (Sidebar)
with st.sidebar:
    st.header("Datos y filtros")
    
    archivo = st.file_uploader("Carga el archivo de estudiantes", type=['csv'])
    
    st.write("Sexo")
    sexo_filtro = st.multiselect(
        "Sexo", 
        options=df['Sexo'].unique(), 
        default=df['Sexo'].unique(),
        label_visibility="collapsed"
    )
    
    seccion_filtro = st.selectbox(
        "Sección", 
        options=['Todas'] + list(df['Sección'].unique())
    )
    
    rango_promedio = st.slider(
        "Rango del promedio", 
        min_value=1.0, 
        max_value=7.0, 
        value=(1.0, 7.0),
        step=0.1
    )
    
    asistencia_min = st.number_input(
        "Asistencia mínima (%)", 
        min_value=0, 
        max_value=100, 
        value=0
    )
    
    st.caption("Los filtros se combinan y aplicarán a los datos de la tabla y los gráficos.")

# 3. Lógica de filtrado
df_filtrado = df[
    (df['Sexo'].isin(sexo_filtro)) &
    (df['Promedio'] >= rango_promedio[0]) & 
    (df['Promedio'] <= rango_promedio[1]) &
    (df['Asistencia (%)'] >= asistencia_min)
]

if seccion_filtro != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Sección'] == seccion_filtro]

# 4. Área Principal
st.title("Dashboard interactivo de notas")
st.write("Explora los resultados de un curso combinando filtros. **Promedio:** 50% de evaluación. **Aprobación de ejercicio:** promedio mayor o igual a 4.0. Datos ficticios.")

st.write(f"Filtros activos: Mujer, Hombre - Sección: {seccion_filtro} - Promedio: {rango_promedio[0]} a {rango_promedio[1]} - Asistencia mínima: {asistencia_min}%")

# Métricas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Estudiantes seleccionados", len(df_filtrado))
with col2:
    promedio_general = df_filtrado['Promedio'].mean() if not df_filtrado.empty else 0
    st.metric("Promedio general", f"{promedio_general:.2f}".replace('.', ','))
with col3:
    aprobados = len(df_filtrado[df_filtrado['Promedio'] >= 4.0])
    tasa_aprobacion = (aprobados / len(df_filtrado) * 100) if not df_filtrado.empty else 0
    st.metric("Aprobación", f"{tasa_aprobacion:.2f}%".replace('.', ','))

# Controles de Gráfico
st.write("Gráfico")
tipo_grafico = st.radio(
    "Tipo de gráfico",
    ["Notas por estudiante", "Promedio por sección"],
    horizontal=True,
    label_visibility="collapsed"
)

# Dos columnas principales para Gráfico y Tabla
col_grafico, col_tabla = st.columns([1.2, 1])

with col_grafico:
    st.subheader("Visualización de notas")
    if not df_filtrado.empty:
        fig, ax = plt.subplots(figsize=(8, 5))
        
        if tipo_grafico == "Notas por estudiante":
            ax.bar(df_filtrado['Estudiante'], df_filtrado['Promedio'], color='#1f77b4')
            ax.set_ylabel('Promedio de notas')
            ax.set_xlabel('Estudiante')
            plt.xticks(rotation=45)
            # Línea de aprobación
            ax.axhline(y=4.0, color='r', linestyle='--', label='Aprobación = 4.0')
            ax.legend()
        else:
            promedios_seccion = df_filtrado.groupby('Sección')['Promedio'].mean()
            ax.bar(promedios_seccion.index, promedios_seccion.values, color='#ff7f0e')
            ax.set_ylabel('Promedio')
            ax.set_xlabel('Sección')
            
        ax.set_ylim(1, 7)
        st.pyplot(fig)
    else:
        st.warning("No hay datos para mostrar con los filtros actuales.")

with col_tabla:
    st.subheader("Estudiantes seleccionados")
    # Configurar el dataframe para que no muestre el índice por defecto
    st.dataframe(df_filtrado, hide_index=True, use_container_width=True)

# Botón de descarga
st.download_button(
    label="Descargar selección CSV",
    data=df_filtrado.to_csv(index=False).encode('utf-8'),
    file_name='estudiantes_filtrados.csv',
    mime='text/csv',
)

st.caption(f"Mostrando {len(df_filtrado)} estudiantes. La línea de corte de aprobación representa un 4.0 de promedio.")

