import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json
import sys

# Agregar backend al path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "backend"))
from config import DATA_PROCESSED


# ============================================================
# CARGA DE DATOS
# ============================================================

@st.cache_data
def cargar_indicadores():
    ruta = DATA_PROCESSED / "indicadores_nacionales.json"
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def cargar_resumen_departamentos():
    return pd.read_parquet(DATA_PROCESSED / "resumen_departamentos.parquet")


@st.cache_data
def cargar_brecha_nivel():
    return pd.read_parquet(DATA_PROCESSED / "brecha_nivel.parquet")


# ============================================================
# COMPONENTES VISUALES
# ============================================================

def mostrar_kpi(titulo: str, valor: str, subtitulo: str = "", color: str = "#1f77b4"):
    """Tarjeta de indicador grande y clara."""
    st.markdown(
        f"""
        <div style="
            background-color: #f8f9fa;
            border-left: 6px solid {color};
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 12px;
        ">
            <div style="font-size: 0.9rem; color: #555; margin-bottom: 4px;">{titulo}</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #222;">{valor}</div>
            <div style="font-size: 0.85rem; color: #666;">{subtitulo}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def mostrar_insight(texto: str, icono: str = "📌"):
    """Caja de insight legible."""
    st.markdown(
        f"""
        <div style="
            background-color: #e8f4fd;
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 12px;
            border: 1px solid #cce0f5;
        ">
            <span style="font-size: 1.1rem;">{icono}</span>
            <span style="font-size: 1rem; color: #222;">{texto}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

def mostrar_home():
    st.title("Panorama de la Educación en Guatemala 2024")
    st.markdown("Datos del ciclo escolar formal · Fuente: Instituto Nacional de Estadística (INE)")
    st.markdown("---")

    # ---- Cargar datos ----
    try:
        data = cargar_indicadores()
        indicadores = data["indicadores"]
        insights = data["insights"]
        por_depto = cargar_resumen_departamentos()
        por_nivel = cargar_brecha_nivel()
    except Exception as e:
        st.error("No se encontraron los datos procesados. Ejecuta primero el pipeline de datos.")
        st.code("python scripts/run_pipeline.py")
        st.stop()

    # ============================================================
    # 1. INDICADORES PRINCIPALES (KPIs)
    # ============================================================
    st.subheader("¿Cómo cerró el ciclo escolar 2024?")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        mostrar_kpi(
            "Total de estudiantes",
            f"{indicadores['total_estudiantes']:,}",
            "Inscripciones registradas",
            color="#2c3e50"
        )

    with col2:
        mostrar_kpi(
            "Promovidos",
            f"{indicadores['tasa_promocion']}%",
            "Aprobaron el grado",
            color="#27ae60"
        )

    with col3:
        mostrar_kpi(
            "No promovidos",
            f"{indicadores['tasa_no_promocion']}%",
            "No aprobaron",
            color="#e67e22"
        )

    with col4:
        mostrar_kpi(
            "Retirados",
            f"{indicadores['tasa_retiro']}%",
            "Abandonaron el ciclo",
            color="#c0392b"
        )

    st.markdown("")

    # ============================================================
    # 2. INSIGHTS (lo más importante para el usuario)
    # ============================================================
    st.subheader("Lo más importante que debes saber")

    iconos = ["📊", "⚠️", "🏫", "🌍"]
    for i, texto in enumerate(insights):
        mostrar_insight(texto, icono=iconos[i % len(iconos)])

    st.markdown("---")

    # ============================================================
    # 3. DISTRIBUCIÓN POR NIVEL
    # ============================================================
    st.subheader("¿En qué niveles estudian los niños y jóvenes?")

    col_izq, col_der = st.columns([1.2, 1])

    with col_izq:
        fig_nivel = px.bar(
            por_nivel,
            x="Nivel",
            y="total",
            text="total",
            color="Nivel",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"total": "Estudiantes", "Nivel": ""},
        )
        fig_nivel.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig_nivel.update_layout(
            showlegend=False,
            height=380,
            margin=dict(t=20, b=40),
            yaxis_title="Cantidad de estudiantes",
        )
        st.plotly_chart(fig_nivel, use_container_width=True)

    with col_der:
        st.markdown("##### ¿Qué nos dice esto?")
        st.markdown("""
        - **Primaria** concentra la mayor cantidad de estudiantes.  
        - La caída hacia **Básico** y **Diversificado** muestra dónde se pierde más población escolar.  
        - Esta “pirámide” es una de las señales más claras de la crisis educativa del país.
        """)

        # Pequeña tabla de tasas por nivel
        st.markdown("##### Resultados por nivel")
        tabla_nivel = por_nivel[["Nivel", "tasa_promocion", "tasa_retiro"]].copy()
        tabla_nivel.columns = ["Nivel", "% Promoción", "% Retiro"]
        st.dataframe(tabla_nivel, hide_index=True, use_container_width=True)

    st.markdown("---")

    # ============================================================
    # 4. DEPARTAMENTOS MÁS CRÍTICOS
    # ============================================================
    st.subheader("¿Dónde está la situación más crítica?")

    st.markdown("Departamentos ordenados por **tasa de retiro** (de mayor a menor):")

    # Top 8 más críticos
    top_criticos = por_depto.head(8).copy()

    fig_retiro = px.bar(
        top_criticos,
        x="tasa_retiro",
        y="Departamento",
        orientation="h",
        text="tasa_retiro",
        color="tasa_retiro",
        color_continuous_scale="Reds",
        labels={"tasa_retiro": "Tasa de retiro (%)", "Departamento": ""},
    )
    fig_retiro.update_traces(texttemplate="%{text}%", textposition="outside")
    fig_retiro.update_layout(
        height=400,
        margin=dict(t=20, b=20),
        coloraxis_showscale=False,
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig_retiro, use_container_width=True)

    # Insight del departamento más crítico
    mas_critico = por_depto.iloc[0]
    st.info(
        f"**Dato clave:** {mas_critico['Departamento']} tiene la tasa de retiro más alta del país "
        f"({mas_critico['tasa_retiro']}%). "
        f"Allí se registraron {mas_critico['total']:,} estudiantes en 2024."
    )

    st.markdown("---")

    # ============================================================
    # 5. PIE DE PÁGINA / CONTEXTO
    # ============================================================
    st.caption(
        "Fuente: Microdatos de Educación Formal 2024 · Instituto Nacional de Estadística (INE). "
        "Los porcentajes se calculan sobre el total de inscripciones registradas en el ciclo."
    )


# Para probar la página de forma independiente
if __name__ == "__main__":
    st.set_page_config(page_title="Panorama Nacional", layout="wide")
    mostrar_home()